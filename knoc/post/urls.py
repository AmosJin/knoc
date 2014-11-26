from django.conf.urls import *

urlpatterns = patterns(
    'post.views',
    url(r'^$', 'home', name="home"), 
)

