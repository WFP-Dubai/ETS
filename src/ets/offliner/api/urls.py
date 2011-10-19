import datetime

from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication

from ets.api.urls import expand_response
from .handlers import JSONOfflineHandler
from ..utils import DjangoAuthentication

auth = OAuthAuthentication(realm='API')
auth1 = DjangoAuthentication()

JSON_OFFLINE_HEADERS = {'Content-Disposition': 'attachment; filename=server-export-%s.json' % datetime.date.today() }
FORMAT_JSON = {'emitter_format': 'json'}
offline_resource_oauth = login_required(expand_response(Resource(handler=JSONOfflineHandler, authentication=auth), JSON_OFFLINE_HEADERS))
offline_resource = login_required(expand_response(Resource(JSONOfflineHandler), JSON_OFFLINE_HEADERS))

urlpatterns = patterns('',
                       
    # For offline client in JSON
    (r'^oauth/(?P<warehouse_pk>[-\w]+)/$', offline_resource_oauth, FORMAT_JSON, "api_offline_oauth"),
    (r'^(?P<warehouse_pk>[-\w]+)/(?P<start_date>[-\w]+)/$', offline_resource, FORMAT_JSON, "api_offline"),
    (r'^(?P<warehouse_pk>[-\w]+)/$', offline_resource, FORMAT_JSON, "api_offline"),
)    
