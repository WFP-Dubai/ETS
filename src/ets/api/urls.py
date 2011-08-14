### -*- coding: utf-8 -*- ####################################################
from django.conf.urls.defaults import patterns
#from django.conf import settings

#from django.core.urlresolvers import reverse

#import piston.authentication
from piston.resource import Resource
from piston.doc import documentation_view

from .handlers import NewWaybillHandler, InformedWaybillHandler , ReadCSVLoadingDetailHandler
from .handlers import DeliveredWaybillHandler, ReceivingWaybillHandler, ReadCSVWaybillHandler
#from cj.authenticators import PermissibleHttpBasicAuthentication


#permhttpauth = PermissibleHttpBasicAuthentication(realm='eTVnet mall API http')

#AUTHENTICATORS = [permhttpauth, ]

waybills_resource = Resource(ReadCSVWaybillHandler)
loading_details_resource = Resource(ReadCSVLoadingDetailHandler)

new_waybill_resource = Resource(NewWaybillHandler)
informed_waybill_resource = Resource(InformedWaybillHandler)
delivered_waybill_resource = Resource(DeliveredWaybillHandler)

receiving_waybill_resource = Resource(ReceivingWaybillHandler)

#history_id = Resource(HistoryIdHandler, authentication=AUTHENTICATORS)
#history_date = Resource(HistoryDateHandler, authentication=AUTHENTICATORS)
#history_user = Resource(HistoryUserHandler, authentication=AUTHENTICATORS)


urlpatterns = patterns('',

    (r'^waybills/$', waybills_resource, { 'emitter_format': 'csv' }, "api_waybills"),
    (r'^loading-details/$', loading_details_resource, { 'emitter_format': 'csv' }, "api_loading_details"),
    
    (r'^new/$', new_waybill_resource, { 'emitter_format': 'django_json' }, "api_new_waybill"),
    (r'^receiving/(?P<destination>[-\w]+)/$', receiving_waybill_resource, { 
        'emitter_format': 'django_json' 
    }, "api_receiving_waybill"),
                       
    (r'^informed/(?P<slug>[-\w]+)/$', informed_waybill_resource, { 'emitter_format': 'json' }, "api_informed_waybill"),
    (r'^informed/$', informed_waybill_resource, { 'emitter_format': 'json' }, "api_informed_waybill"),
    
    (r'^delivered/(?P<slug>[-\w]+)/$', delivered_waybill_resource, { 
        'emitter_format': 'django_json' 
    }, "api_delivered_waybill"),
    (r'^delivered/$', delivered_waybill_resource, { 'emitter_format': 'django_json' }, "api_delivered_waybill"),
    
    (r'^docs/$', documentation_view),

)
