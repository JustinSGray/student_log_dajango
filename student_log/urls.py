from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from log.views import v1_api
from log.forms import AuthenticationForm

urlpatterns = patterns('',
    url(r'^login/','log.views.user_login'),
    url(r'^logout/$','log.views.user_logout'),
    url(r'loadroster/(?P<classId>\d+)/$','log.views.load_roster'),
    url(r'^api/',include(v1_api.urls)),
)
