from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

urlpatterns = patterns('',
    #url(r'^profiler/', include('profiler.urls')),
    (r'^', include('log.urls')),
)
