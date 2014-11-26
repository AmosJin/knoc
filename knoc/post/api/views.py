import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.db import transaction, IntegrityError
from django.db.transaction import TransactionManagementError
from django.conf import settings
from django.template import loader, RequestContext
from django.core.cache import cache

from api.response import SuccessResult, FailedResult, ForbiddenResult
from api.views import APIView, api_permission_required

from post.models import Item, Link

class TestView(APIView):
    http_method_name = ('get',)

    def get(self, request):
        link = Link.objects.all()[0]
        data = self.serialize(link)
        return SuccessResult(data=data)
