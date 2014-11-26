import re
from functools import wraps

from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.utils import six
from django.shortcuts import render_to_response as render, get_object_or_404

from rest_framework import exceptions
from rest_framework.views import Request, APIView as RestView
from rest_framework.renderers import UnicodeJSONRenderer
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.serializers import Serializer

from api.response import Result, FailedResult, ForbiddenResult, NotFoundResult, BadRequestResult
from api.exceptions import Result404, DataFormatError
from api.throttling import UserRateThrottle, ClientRateThrottle
from api.authentication import CSRFexemptSessionAuthentication
from api import status

METHODS = re.compile(r'(?:get|post|put|delete)\(\)')

class IgnoreClientContentNegotiation(DefaultContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix):
        """
        Select the first renderer in the `.renderer_classes` list.
        """
        return (renderers[0], renderers[0].media_type)
        
def api_permission_required(perm, msg=_('permission required')):
    """
    add Django permission check to specify view method
    usage:
        @api_permission_required('read.add_article')
        def create(self, request, *args, **kwargs):
    
    """
    def decorator(method):
        @wraps(method)
        def _wrapped_method(self, request, *args, **kwargs):
            if perm == 'auth':
                if not request.user.is_authenticated():
                    raise exceptions.NotAuthenticated()
                else:
                    return method(self, request, *args, **kwargs)
            elif perm == 'staff':
                if not request.user.is_staff:
                    raise exceptions.NotAuthenticated()
                else:
                    return method(self, request, *args, **kwargs)
                
            if request.user.has_perm(perm):
                return method(self, request, *args, **kwargs)
            else:
                return ForbiddenResult(msg=msg)

        return _wrapped_method
        
    return decorator
    
def exception_handler(exc):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's builtin `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause Result with status=status.FAILED.
    """
    if isinstance(exc, Http404):
        msg = getattr(exc, 'msg', 'Not Found')
        return NotFoundResult(msg=msg)

    elif isinstance(exc, DataFormatError):
        msg = getattr(exc, 'msg', 'data format error')
        return FailedResult(msg=msg)
        
    elif isinstance(exc, TypeError):
        # user request an API with unexpected keyword argument
        # this happend when 'GET' and 'POST' method has different arguments
        # and user reqeust a 'GET' url with 'POST', or conversely 
        msg = str(exc)
        if METHODS.match(msg):
            return FailedResult(msg=_('Bad Request. API got an unexpected argument'))

        raise

    elif isinstance(exc, PermissionDenied) or isinstance(exc, exceptions.PermissionDenied):
        return ForbiddenResult()
        
    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['X-Throttle-Wait-Seconds'] = '%d' % exc.wait

        return Response({'msg':exc.detail},
                      status=exc.status_code,
                      headers=headers)

    # Note: Unhandled exceptions will raise a 500 error.
    return None

def get_view_name(cls):
    name = cls.__name__
    return  re.sub(r"([A-Z])", lambda mo: "_" + mo.group(0).lower(), name)[1:]

class APIView(RestView):
    content_negotiation_class = IgnoreClientContentNegotiation
    render_classes = (UnicodeJSONRenderer,)
    permission_classes = (IsAuthenticated, )
    authentication_classes = (CSRFexemptSessionAuthentication, )
    authentication_oauth = False
    # parser_classes = (JSONParser, FormParser, MultiPartParser) 
    max_ids_length = 50
    max_page_num = 100
    max_page_items = 50
    item_per_page = 10
    perms = {'allowany': (AllowAny, )}
    
    def get_permissions(self):
        """
        custom this method for setting AllowAny conveniently 
        """
        if isinstance(self.permission_classes, six.string_types):
            key = self.permission_classes.lower()
            self.permission_classes = self.perms[key]
            
        return super(APIView, self).get_permissions()

    def initialize_request(self, request, *args, **kwargs):
        """
        Returns the initial request object.
        """
        if 'api.shanbay.com' in request.get_host():
            if self.authentication_oauth:
                authenticators = (OAuth2Authentication(), )
                #self.throttle_classes = (UserRateThrottle, ClientRateThrottle)
            else:
                # force auth fail
                request._user = None
                authenticators = (CSRFexemptSessionAuthentication(), )
            
        else:
            authenticators = (CSRFexemptSessionAuthentication(), )
            #self.throttle_classes = (UserRateThrottle, )

        parser_context = self.get_parser_context(request)

        return Request(request,
                       parsers=self.get_parsers(),
                       authenticators=authenticators,
                       negotiator=self.get_content_negotiator(),
                       parser_context=parser_context)

    def serialize(self, data):
        return Serializer(data).data
    
    def data(self, request):
        if request.method == 'GET':
            data = request.GET
        else:
            data = request.DATA
            
        return data or {}
        
    def get_page(self, request):
        try:
            page = int(request.GET.get('page',1))
            if page > self.max_page_num or page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1

        self.page = page
        return page

    def get_ipp(self, request):
        if not request.GET.has_key('ipp'):
            return self.item_per_page
            
        try:
            ipp = int(request.GET.get('ipp'))
            if ipp > self.max_page_items or ipp < 0:
                ipp = self.max_page_items
        except (TypeError, ValueError):
            ipp = self.item_per_page

        return ipp

    def paginate(self, objects, serialize=True):
        """
        this is a shortcut method for self.pagination
        for most of time ,we will call `return Result(data:{'total':total, 'ipp':ipp, 'data':data})`
        """
        #Now I'm just a wrapper for `pagination`
        total, ipp, objects = self.pagination(objects)
        if serialize:
            objects = self.serialize(objects)
        return Result(data={'total':total, 'ipp':ipp, 'objects':objects})
    
    def pagination(self, contents):
        reverse = self.request.GET.has_key('reverse')
        page = self.get_page(self.request)
        ipp = self.get_ipp(self.request)
        
        try:
            total = contents.count()
            if reverse:
                # queyrset.reverse return a new queryset
                contents = contents.reverse()
        except (AttributeError, TypeError):
            total = len(contents)
            # list.reverse modify content in-place
            reverse and contents.reverse()

        contents = list(contents[ipp*(page-1):ipp*page])
        if reverse:
            # only reverse `page`, the content in page keep original order
            contents.reverse()
            
        return total, ipp, contents

    def validate_ids(self, ids=None, seperator=','):
        if not ids:
            ids = self.request.GET.get('ids')
            
        try:
            ids = [int(i) for i in ids.split(seperator)]
        except (TypeError, ValueError, AttributeError):
            raise DataFormatError(msg=_('ids format error'))

        if len(ids) > self.max_ids_length:
            raise DataFormatError(msg=_('ids too long'))

        return ids
        
    @classmethod
    def get_view_name(cls):
        name = cls.__name__
        return  re.sub(r"([A-Z])", lambda mo: "_" + mo.group(0).lower(), name)[1:]

    # this is almost same with django's get_object_or_404,
    # which will call `get` with a `queryset` (queryset.get)
    # but if we custom the `get` method like in Learning, the customed method will not be called
    # so this function is still needed
    @staticmethod
    def get_model_or_404(Model, msg=_('Not Found'), serialize=False, **kwargs):
        try:
            model = Model.objects.get(**kwargs)
            if serialize:
                return self.serialize(model)
            else:
                return model
        except ObjectDoesNotExist:
            raise Result404(msg=msg)

