import datetime
import requests
from io import StringIO
from requests.exceptions import Timeout, ConnectionError, RequestException
from lxml import etree

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.db import transaction, IntegrityError
from django.db.transaction import TransactionManagementError
from django.conf import settings
from django.template import loader, RequestContext
from django.core.cache import cache

from api.response import Result, SuccessResult, FailedResult, ForbiddenResult
from api.views import APIView, api_permission_required

from post.models import Group, Item, Link
from post.forms import  LinkForm, LinkURLForm, NoteForm
from post import core

class TestView(APIView):
    http_method_name = ('get',)

    def get(self, request):
        link = Link.objects.all()[0]
        data = self.serialize(link)
        return SuccessResult(data=data)

class GroupView(APIView):
    http_method_name = ('get',)
    def get(self, request):
        groups = Group.objects.all()
        return SuccessResult(data=self.serialize(groups))

class ItemView(APIView):
    http_method_name = ('get', 'post',)

    def get(self, request, group_id):
        total, ipp,  items = self.pagination(Item.objects.filter(group__id=group_id))
        items = [self.serialize(item) for item in items]
        return SuccessResult(data={'total':total, 'ipp':ipp, 'items':items})

    def post(self, request, item_type, group_id):
        forms = {
                "link": LinkForm,
                "note": NoteForm
        }
        data = self.data(request)
        tags = data["tags"]
        user = request.user
        form = forms.get(item_type)(data)
        if form.is_valid():
            link = form.save()
            item = core.update_item(link, user_id=user.pk, group_id=group_id, tags=tags)
            return SuccessResult(data=self.serialize(item))

        return FailedResult(msg=form.errors)


class LinkView(APIView):
    http_method_name = ('post')

    def post(self, request, group_id):
        data = self.data(request)
        user = request.user
        link = data.get("link")
        try:
            r = requests.get(link, timeout=6)
        except (Timeout, ConnectionError, RequestException):
            return FailedResult(msg="connection error")

        content = r.content
        encoding = core.get_encoding(content)
        encoding = encoding or "utf8"
        data = core.get_link_info(link, content, encoding)
        form = LinkForm(data)
        if form.is_valid:
            link = form.save()
        else:
            return FailedResult(msg=form.errors)

        item = core.update_item(link, user_id=user.pk, group_id=group_id)

        return Result(data=self.serialize(link))
