from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from log.views import v1_api
from log.forms import AuthenticationForm

urlpatterns = patterns('',
    url(r'^$','log.views.root'),
    url(r'^login/','log.views.login_user'),
    url(r'^logout/$','log.views.logout_user'),
    url(r'loadroster/(?P<classId>\d+)/$','log.views.load_roster'),
    url(r'^api/',include(v1_api.urls)),
)
