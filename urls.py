from django.conf.urls.defaults import *
from ets.waybill.views import *

from django.contrib.auth.views import login, logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^ets/media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/tobias/projects/epic/ets/media'}),
    (r'^ets/', include('ets.waybill.urls')),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': 'ets/select-action'}),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^dojango/', include('dojango.urls')),
    #(r'^accounts/login/$',login),
)
