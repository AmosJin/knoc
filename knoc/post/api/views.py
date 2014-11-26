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
from post.forms import  LinkForm, NoteForm
from post import core

class TestView(APIView):
    http_method_name = ('get',)

    def get(self, request):
        link = Link.objects.all()[0]
        data = self.serialize(link)
        return SuccessResult(data=data)

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

