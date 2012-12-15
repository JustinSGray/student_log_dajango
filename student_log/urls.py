from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    (r'^%s'%settings.FORCE_SCRIPT_NAME,include('log.urls')),

)
