from django.conf.urls.defaults import *
from ets.waybill.views import hello, homepage

from django.contrib.auth.views import login,logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^ets/', include('ets.waybill.urls')),
    (r'^hello/$',hello),
    (r'^accounts/login/$',login),
    (r'^accounts/logout/$',logout),
    (r'^$',homepage),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^dojango/', include('dojango.urls')),
)
