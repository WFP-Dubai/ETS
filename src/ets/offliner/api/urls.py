import datetime

from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required

from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication, OAuthAuthentication

from ets.api.urls import expand_response
from .handlers import JSONOfflineHandler

auth = HttpBasicAuthentication(realm='My sample API')

JSON_OFFLINE_HEADERS = {'Content-Disposition': 'attachment; filename=server-export-%s.json' % datetime.date.today() }
FORMAT_JSON = {'emitter_format': 'json'}
#offline_resource = login_required(expand_response(Resource(handler=JSONOfflineHandler, authentication=auth), JSON_OFFLINE_HEADERS))
offline_resource = login_required(expand_response(Resource(JSONOfflineHandler), JSON_OFFLINE_HEADERS))

urlpatterns = patterns('',
                       
    # For offline client in JSON
    (r'^(?P<warehouse_pk>[-\w]+)/(?P<start_date>[-\w]+)/$', offline_resource, FORMAT_JSON, "api_offline"),
    (r'^(?P<warehouse_pk>[-\w]+)/$', offline_resource, FORMAT_JSON, "api_offline"),
)    

urlpatterns += patterns(
    'piston.authentication',
    (r'^oauth/request_token/$','oauth_request_token'),
    (r'^oauth/authorize/$','oauth_user_auth'),
    (r'^oauth/access_token/$','oauth_access_token'),
)
