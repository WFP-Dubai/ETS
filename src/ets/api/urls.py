### -*- coding: utf-8 -*- ####################################################
import datetime

from django.utils.functional import wraps

from django.conf.urls.defaults import patterns
#from django.conf import settings

#from django.core.urlresolvers import reverse

#import piston.authentication
from piston.resource import Resource
from piston.doc import documentation_view

from .handlers import NewWaybillHandler, InformedWaybillHandler , ReadCSVLoadingDetailHandler
from .handlers import DeliveredWaybillHandler, ReceivingWaybillHandler, ReadCSVWaybillHandler
from .handlers import ReadCSVOrdersHandler, ReadCSVOrderItemsHandler
#from cj.authenticators import PermissibleHttpBasicAuthentication


#permhttpauth = PermissibleHttpBasicAuthentication(realm='eTVnet mall API http')

#AUTHENTICATORS = [permhttpauth, ]
def expand_response(view, headers):
    #@wraps(view)
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        for header, value in headers.items():
            response[header] = value
        return response
    return wrapper

CSV_WAYBILLS_HEADERS = {'Content-Disposition': 'attachment; filename=waybills-%s.csv' % datetime.date.today() }
CSV_LOADING_DETAILS_HEADERS = {'Content-Disposition': 'attachment; filename=loading-details-%s.csv' % datetime.date.today() }
CSV_ORDERS_HEADERS = {'Content-Disposition': 'attachment; filename=orders-%s.csv' % datetime.date.today() }
CSV_ORDER_ITEMS_HEADERS = {'Content-Disposition': 'attachment; filename=order-items-%s.csv' % datetime.date.today() }
FORMAT_CSV = {'emitter_format': 'csv'}

waybills_resource = Resource(ReadCSVWaybillHandler)
loading_details_resource = Resource(ReadCSVLoadingDetailHandler)
orders_resource = Resource(ReadCSVOrdersHandler)
order_items_resource = Resource(ReadCSVOrderItemsHandler)

new_waybill_resource = Resource(NewWaybillHandler)
informed_waybill_resource = Resource(InformedWaybillHandler)
delivered_waybill_resource = Resource(DeliveredWaybillHandler)

receiving_waybill_resource = Resource(ReceivingWaybillHandler)

#history_id = Resource(HistoryIdHandler, authentication=AUTHENTICATORS)
#history_date = Resource(HistoryDateHandler, authentication=AUTHENTICATORS)
#history_user = Resource(HistoryUserHandler, authentication=AUTHENTICATORS)


urlpatterns = patterns('',
                       
    # For Waybills CSV API
    (r'^waybills/warehouse_destination_waybill/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/(?P<slug>[-\w]+)/$', 
        expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, "api_waybills"),
    (r'^waybills/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$',  
        expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, "api_waybills"),
    (r'^waybills/warehouse_waybill/(?P<warehouse>[-\w]+)/(?P<slug>[-\w]+)/$',  
        expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, "api_waybills"),
    (r'^waybills/destination_waybill/(?P<destination>[-\w]+)/(?P<slug>[-\w]+)/$', 
        expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, "api_waybills"), 
    (r'^waybills/warehouse/(?P<warehouse>[-\w]+)/$',  expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), 
        FORMAT_CSV, "api_waybills"),
    (r'^waybills/destination/(?P<destination>[-\w]+)/$', expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), 
        FORMAT_CSV, "api_waybills"),                 
    (r'^waybills/(?P<slug>[-\w]+)/$', expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, 
        "api_waybills"),
    (r'^waybills/$', expand_response(waybills_resource, CSV_WAYBILLS_HEADERS), FORMAT_CSV, "api_waybills"),
    
    # For LoadingDetails CSV API
    (r'^loading_details/warehouse_destination_waybill/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/(?P<waybill>[-\w]+)/$', 
        expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$', 
        expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/warehouse_waybill/(?P<warehouse>[-\w]+)/(?P<waybill>[-\w]+)/$', 
        expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/destination_waybill/(?P<destination>[-\w]+)/(?P<waybill>[-\w]+)/$', 
        expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"), 
    (r'^loading_details/warehouse/(?P<warehouse>[-\w]+)/$', expand_response(loading_details_resource, 
        CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/destination/(?P<destination>[-\w]+)/$', expand_response(loading_details_resource, 
        CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, "api_loading_details"),                 
    (r'^loading_details/(?P<waybill>[-\w]+)/$', expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), 
        FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/$', expand_response(loading_details_resource, CSV_LOADING_DETAILS_HEADERS), FORMAT_CSV, 
        "api_loading_details"),
    
    # For Order CSV API
    (r'^orders/warehouse_destination_order/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/(?P<code>[-\w]+)/$', 
        expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, "api_orders"),
    (r'^orders/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$',  
        expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, "api_orders"),
    (r'^orders/warehouse_order/(?P<warehouse>[-\w]+)/(?P<code>[-\w]+)/$',  
        expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, "api_orders"),
    (r'^orders/destination_order/(?P<destination>[-\w]+)/(?P<code>[-\w]+)/$', 
        expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, "api_orders"), 
    (r'^orders/warehouse/(?P<warehouse>[-\w]+)/$',  expand_response(orders_resource, CSV_ORDERS_HEADERS), 
        FORMAT_CSV, "api_orders"),
    (r'^orders/destination/(?P<destination>[-\w]+)/$', expand_response(orders_resource, CSV_ORDERS_HEADERS), 
        FORMAT_CSV, "api_orders"),                 
    (r'^orders/(?P<code>[-\w]+)/$', expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, 
        "api_orders"),
    (r'^orders/$', expand_response(orders_resource, CSV_ORDERS_HEADERS), FORMAT_CSV, "api_orders"),
    
    # For OrderItem CSV API
    (r'^order_items/warehouse_destination_order/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/(?P<order>[-\w]+)/$', 
        expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"),
    (r'^order_items/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$', 
        expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"),
    (r'^order_items/warehouse_order/(?P<warehouse>[-\w]+)/(?P<order>[-\w]+)/$', 
        expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"),
    (r'^order_items/destination_order/(?P<destination>[-\w]+)/(?P<order>[-\w]+)/$', 
        expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"), 
    (r'^order_items/warehouse/(?P<warehouse>[-\w]+)/$', expand_response(order_items_resource, 
        CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"),
    (r'^order_items/destination/(?P<destination>[-\w]+)/$', expand_response(order_items_resource, 
        CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, "api_order_items"),                 
    (r'^order_items/(?P<order>[-\w]+)/$', expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), 
        FORMAT_CSV, "api_order_items"),
    (r'^order_items/$', expand_response(order_items_resource, CSV_ORDER_ITEMS_HEADERS), FORMAT_CSV, 
        "api_order_items"),
    
    
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
