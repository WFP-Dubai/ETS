### -*- coding: utf-8 -*- ####################################################
from django.conf.urls.defaults import patterns
#from django.conf import settings

#from django.core.urlresolvers import reverse

import piston.authentication
from piston.resource import Resource
from piston.doc import documentation_view

from .handlers import WaybillHandler, NewWaybillHandler, InformedWaybillHandler
#from cj.authenticators import PermissibleHttpBasicAuthentication


#permhttpauth = PermissibleHttpBasicAuthentication(realm='eTVnet mall API http')

#AUTHENTICATORS = [permhttpauth, ]

waybill_resource = Resource(WaybillHandler)
new_waybill_resource = Resource(NewWaybillHandler)
informed_waybill_resource = Resource(InformedWaybillHandler)


#history_id = Resource(HistoryIdHandler, authentication=AUTHENTICATORS)
#history_date = Resource(HistoryDateHandler, authentication=AUTHENTICATORS)
#history_user = Resource(HistoryUserHandler, authentication=AUTHENTICATORS)


urlpatterns = patterns('',
    
    (r'^waybill/$', waybill_resource, { 'emitter_format': 'json' }, "api_waybill"),
    (r'^waybill/(?P<id>\d+)/$', waybill_resource, { 'emitter_format': 'json' }, "api_waybill"),
    
    (r'^new/$', new_waybill_resource, { 'emitter_format': 'django' }, "api_new_waybill"),
    (r'^informed/(?P<id>\d+)/$', informed_waybill_resource, { 'emitter_format': 'json' }, "api_informed_waybill"),
    #===================================================================================================================
    # url(r'^api/history/id/(?P<object_id>\d+)/$', history_id, name="history_id"),
    # url(r'^api/history/date/(?P<date>\d{4}-\d{2}-\d{2})/$', history_date, name="history_date"),
    # url(r'^api/history/user/(?P<username>[\w.@+-]+)/$', history_user, name="history_user"),
    #===================================================================================================================

    (r'^docs/$', documentation_view),

)
