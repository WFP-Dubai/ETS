### -*- coding: utf-8 -*- ####################################################
import datetime

from django.conf.urls.defaults import patterns
#from django.conf import settings
from django.contrib.auth.decorators import login_required
#from django.core.urlresolvers import reverse

#import piston.authentication
from piston.resource import Resource
from piston.doc import documentation_view
from piston.authentication import HttpBasicAuthentication


from .handlers import ReadCSVLoadingDetailHandler, ReadCSVStockItemsHandler, ReadCSVWarehouseHandler
from .handlers import ReadCSVOrdersHandler, ReadCSVOrderItemsHandler, ReadCSVWaybillHandler
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
CSV_STOCK_ITEMS_HEADERS = {'Content-Disposition': 'attachment; filename=stock-items-%s.csv' % datetime.date.today() }
CSV_WH_HEADERS = {'Content-Disposition': 'attachment; filename=warehouses-%s.csv' % datetime.date.today() }

FORMAT_CSV = {'emitter_format': 'csv'}

authentication = HttpBasicAuthentication(realm='ETS API HTTP')

#Waybills
waybills_resource = login_required(expand_response(Resource(ReadCSVWaybillHandler), CSV_WAYBILLS_HEADERS))
loading_details_resource = login_required(expand_response(Resource(ReadCSVLoadingDetailHandler), CSV_LOADING_DETAILS_HEADERS))
loading_details_resource_basic = expand_response(Resource(ReadCSVLoadingDetailHandler, authentication=authentication), 
                                                 CSV_LOADING_DETAILS_HEADERS)

#Orders
orders_resource = login_required(expand_response(Resource(ReadCSVOrdersHandler), CSV_ORDERS_HEADERS))
order_items_resource = login_required(expand_response(Resource(ReadCSVOrderItemsHandler), CSV_ORDER_ITEMS_HEADERS))

stock_items_resource = login_required(expand_response(Resource(ReadCSVStockItemsHandler), CSV_STOCK_ITEMS_HEADERS))
stock_items_resource_basic = expand_response(Resource(ReadCSVStockItemsHandler, authentication=authentication), 
                                             CSV_STOCK_ITEMS_HEADERS)

warehouses_resource = login_required(expand_response(Resource(ReadCSVWarehouseHandler), CSV_WH_HEADERS))


urlpatterns = patterns('',
                       
    # For Waybills CSV API
    (r'^waybills/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$',  
        waybills_resource, FORMAT_CSV, "api_waybills"),
    (r'^waybills/warehouse/(?P<warehouse>[-\w]+)/$',  waybills_resource, 
        FORMAT_CSV, "api_waybills"),
    (r'^waybills/destination/(?P<destination>[-\w]+)/$', waybills_resource, 
        FORMAT_CSV, "api_waybills"),                 
    (r'^waybills/(?P<slug>[-\w]+)/$', waybills_resource, FORMAT_CSV, 
        "api_waybills"),
    (r'^waybills/$', waybills_resource, FORMAT_CSV, "api_waybills"),
    
    # For LoadingDetails CSV API
    (r'^loading_details/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$', 
        loading_details_resource, FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/warehouse/(?P<warehouse>[-\w]+)/$', loading_details_resource, 
        FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/destination/(?P<destination>[-\w]+)/$', loading_details_resource, 
        FORMAT_CSV, "api_loading_details"),                 
    (r'^loading_details/$', loading_details_resource, FORMAT_CSV, "api_loading_details"),
    (r'^loading_details/basic/$', loading_details_resource_basic, FORMAT_CSV, "api_loading_details_basic_auth"),
    (r'^loading_details/(?P<waybill>[-\w]+)/$', loading_details_resource, FORMAT_CSV, "api_loading_details"),
    
    # For Order CSV API
    (r'^orders/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$', orders_resource, 
        FORMAT_CSV, "api_orders"),
    (r'^orders/warehouse_consignee/(?P<warehouse>[-\w]+)/(?P<consignee>[-\w]+)/$', orders_resource, 
        FORMAT_CSV, "api_orders"),
    (r'^orders/consignee/(?P<consignee>[-\w]+)/$', orders_resource, FORMAT_CSV, "api_orders"), 
    (r'^orders/warehouse/(?P<warehouse>[-\w]+)/$', orders_resource, FORMAT_CSV, "api_orders"),
    (r'^orders/destination/(?P<destination>[-\w]+)/$', orders_resource, FORMAT_CSV, "api_orders"),                 
    (r'^orders/(?P<code>[-\w]+)/$', orders_resource, FORMAT_CSV, "api_orders"),
    (r'^orders/$', orders_resource, FORMAT_CSV, "api_orders"),
    
    # For OrderItem CSV API
    (r'^order_items/warehouse_consignee/(?P<warehouse>[-\w]+)/(?P<consignee>[-\w]+)/$', 
        order_items_resource, FORMAT_CSV, "api_order_items"),
    (r'^order_items/warehouse_destination/(?P<warehouse>[-\w]+)/(?P<destination>[-\w]+)/$', 
        order_items_resource, FORMAT_CSV, "api_order_items"),
    (r'^order_items/warehouse/(?P<warehouse>[-\w]+)/$', order_items_resource, FORMAT_CSV, "api_order_items"),
    (r'^order_items/destination/(?P<destination>[-\w]+)/$', order_items_resource, FORMAT_CSV, "api_order_items"),
    (r'^order_items/consignee/(?P<consignee>[-\w]+)/$', order_items_resource, FORMAT_CSV, "api_order_items"),                     
    (r'^order_items/(?P<order>[-\w]+)/$', order_items_resource, FORMAT_CSV, "api_order_items"),
    (r'^order_items/$', order_items_resource, FORMAT_CSV, "api_order_items"),
    
    # For StockItems CSV API
    (r'^stock_items/$', stock_items_resource, FORMAT_CSV, "api_stock_items"),
    (r'^stock_items/basic/$', stock_items_resource_basic, FORMAT_CSV, "api_stock_items_basic_auth"),
    (r'^stock_items/(?P<warehouse>[-\w]+)/$', stock_items_resource, FORMAT_CSV, "api_stock_items"),
    
    #Warehouses
    (r'^warehouses/$', warehouses_resource, FORMAT_CSV, "api_warehouses"),
    
    (r'^docs/$', documentation_view),

)
