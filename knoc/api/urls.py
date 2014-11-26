import inspect
import os
from django.conf.urls import *
from django.conf import settings


# urls = [(r'^%s/' % app, include('%s.api.urls' % app)) for app in settings.APPS if os.path.exists('%s/%s/api/urls.py' %(settings.BASE_DIR, app))]
urls = [(r'^%s/' % app, include('%s.api.urls' % app)) for app in settings.APPS if os.path.exists('%s/%s/api/urls.py' %(settings.BASE_DIR, app))]


print "urls", urls




urlpatterns = patterns('', *urls)

