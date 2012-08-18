from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from log.views import v1_api

urlpatterns = patterns('',
	url(r'^classes/$',"django.views.generic.simple.direct_to_template",{"template":"log/class.html"}),
    url(r'^api/',include(v1_api.urls)),
)
