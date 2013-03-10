### -*- coding: utf-8 -*- ####################################################
import datetime

from django.conf.urls.defaults import patterns
from django.contrib.auth.decorators import login_required
from django.views.decorators.vary import vary_on_headers

from piston.resource import Resource
from piston.doc import documentation_view
from piston.authentication import HttpBasicAuthentication

from ets.api.handlers import ReadLoadingDetailHandler, ReadStockItemsHandler, ReadWarehouseHandler
from ets.api.handlers import ReadOrdersHandler, ReadOrderItemsHandler, ReadWaybillHandler


class ExpandedResource(Resource):
    
    def __init__(self, handler, authentication=None, headers=None):
        super(ExpandedResource, self).__init__(handler=handler, authentication=authentication)
        self.headers = headers or {}
    
    @vary_on_headers('Authorization')
    def __call__(self, request, *args, **kwargs):
        response = super(ExpandedResource, self).__call__(request, *args, **kwargs)
        for header, value in self.headers.items():
            response[header] = value
        return response

def expand_response(view, headers):
    #@wraps(view)
    def wrapper(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        for header, value in headers.items():
            response[header] = value
        return response
    return wrapper

def create_file_header(name, ext):
    return {'Content-Disposition': 'attachment; filename=%s.%s' % (name, ext) }


FORMAT_CSV = {'emitter_format': 'csv'}
FORMAT_EXCEL = {'emitter_format': 'excel'}

authentication = HttpBasicAuthentication(realm='ETS API HTTP')

#Waybills
waybills_resource = login_required(expand_response(Resource(ReadWaybillHandler), create_file_header('waybills', 'xls')))

stock_items_resource = login_required(expand_response(Resource(ReadStockItemsHandler), create_file_header('stock-items', 'xls')))

urlpatterns = patterns('',

    # Waybill API
    (r'^waybills/(?P<filtering>dispatches|receptions|user_related|compas_dispatch|compas_receipt|validate_receipt|validate_dispatch|dispatch_validated|receipt_validated)/$', 
     waybills_resource, FORMAT_EXCEL, "api_waybills"),
    (r'^waybills/$', waybills_resource, FORMAT_EXCEL, "api_waybills"),
        
    # LoadingDetail API
    (r'^loading_details/$', login_required(expand_response(Resource(ReadLoadingDetailHandler), 
                                                           create_file_header('loading-details', 'xls'))), 
     FORMAT_EXCEL, "api_loading_details"),
    (r'^loading_details/basic/$', ExpandedResource(ReadLoadingDetailHandler, authentication=authentication, 
                                                   headers=create_file_header('loading-details', 'csv')), 
     FORMAT_CSV, "api_loading_details_basic_auth"),

    # Order API
    (r'^orders/$', login_required(expand_response(Resource(ReadOrdersHandler), create_file_header('orders', 'xls'))), 
     FORMAT_EXCEL, "api_orders"),

    # OrderItem API
    (r'^order_items/$', login_required(expand_response(Resource(ReadOrderItemsHandler), 
                                                       create_file_header('order-items', 'xls'))), 
     FORMAT_EXCEL, "api_order_items"),

    # StockItems API
    (r'^stock_items/$', stock_items_resource, FORMAT_EXCEL, "api_stock_items"),
    (r'^stock_items/basic/$', ExpandedResource(ReadStockItemsHandler, 
                                              authentication=authentication, 
                                              headers=create_file_header('stock-items', 'csv')), 
     FORMAT_CSV, "api_stock_items_basic_auth"),
    (r'^stock_items/(?P<warehouse>[-\w]+)/$', stock_items_resource, FORMAT_EXCEL, "api_stock_items"),
    
    # Warehouses API
    (r'^warehouses/$', login_required(expand_response(Resource(ReadWarehouseHandler), 
                                                      create_file_header('warehouses', 'xls'))), 
     FORMAT_EXCEL, "api_warehouses"),
    
    (r'^docs/$', documentation_view),

)
