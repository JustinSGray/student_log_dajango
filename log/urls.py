from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from views import v1_api

urlpatterns = patterns('log',
    url(r'^$','views.root'),
    url(r'^login/$','views.login_user'),
    url(r'^logout/$','views.logout_user'),
    url(r'^loadroster/(?P<classId>\d+)/$','views.load_roster'),
    url(r'^api/',include(v1_api.urls)),
)
