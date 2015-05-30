import inspect

from django.conf.urls import *
from api.views import APIView
from post.api import views
for name,value in inspect.getmembers(views, predicate=lambda x:isinstance(x, type) and issubclass(x, APIView)):
    name = value.get_view_name()
    locals()[name] = value.as_view()
    
urlpatterns = patterns(
    '',
    url(r'^test/$', test_view),
    url(r'^group/$', group_view),
    url(r'^link/(?P<group_id>[\d]+)/$', link_view),
    url(r'^note/(?P<group_id>[\d]+)/$', note_view),
    url(r'^items/$', items_view),
    url(r'^item/(?P<group_id>[\d]+)/$', item_view),
)

