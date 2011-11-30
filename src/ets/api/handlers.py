### -*- coding: utf-8 -*- ####################################################

import csv
import StringIO

from django.db.models import Q, ForeignKey

from piston.handler import BaseHandler
from piston.emitters import Emitter

import ets.models


def get_titles(model):
    fields_name = {}
    for field in model._meta.fields:
        if ForeignKey == type(field):
            key = "%s%s" % (field.name, "_id")
            fields_name[key] = unicode(field.verbose_name)
        else:
            fields_name[field.name] = unicode(field.verbose_name)
    return fields_name   


class ReadWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Waybill
    fields = (
        'slug',
        ('order', (
            'code', 'transport_code', 'transport_name', 'origin_type', 'project_number', 
            ('warehouse', ('code', 'name')),
            ('consignee', ('code', 'name')),
            ('location', ('code', 'name')),
        )),
        ('destination', ('code', 'name', ('location', ('code', 'name')),)),
        'loading_date', 'dispatch_date',
        'transaction_type', 'transport_type',
        'dispatch_remarks', 
        ('dispatcher_person', ('code', 'title', 'username')),
        ('receipt_person', ('code', 'title', 'username')),
        'receipt_remarks', 'transport_sub_contractor',
        'transport_driver_name', 'transport_driver_licence',
        'transport_vehicle_registration', 'transport_trailer_registration',
        'container_one_number', 'container_two_number',
        'container_one_seal_number', 'container_two_seal_number',
        'container_one_remarks_dispatch', 'container_two_remarks_dispatch',
        'container_one_remarks_reciept', 'container_two_remarks_reciept',
        'arrival_date', 'start_discharge_date', 'end_discharge_date',
        'distance', 'transport_dispach_signed_date', 'receipt_signed_date',
        'validated', 'sent_compas',
        'receipt_validated', 'receipt_sent_compas',
    )

    def read(self, request, slug="", warehouse="", destination=""):
        """Return waybills in CSV"""
        waybills = self.model.objects.all()
        
        if not request.user.has_perm("ets.waybill_api_full_access"):
            waybills = waybills.filter(order__warehouse__in=ets.models.Warehouse.filter_by_user(request.user))
        
        filter_arg = {}
        if warehouse: 
            filter_arg['order__warehouse__pk'] = warehouse
        if destination:
            filter_arg['destination__pk'] = destination
        if slug:
            filter_arg['slug'] = slug
        if filter_arg:
            waybills = waybills.filter(**filter_arg)
            
        return waybills
        
        
class ReadLoadingDetailHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.LoadingDetail
    
    fields = (
        'slug', 
        ('waybill', (
            'slug',
            ('order', (
                'code', 'transport_code', 'transport_name', 'origin_type', 'project_number', 
                ('warehouse', ('code', 'name')),
                ('consignee', ('code', 'name')),
                ('location', ('code', 'name')),
            )),
            ('destination', ('code', 'name', ('location', ('code', 'name')),)),
            'loading_date', 'dispatch_date',
            'transaction_type', 'transport_type',
            'dispatch_remarks', 
            ('dispatcher_person', ('code', 'title', 'username')),
            ('receipt_person', ('code', 'title', 'username')),
            'receipt_remarks', 'transport_sub_contractor',
            'transport_driver_name', 'transport_driver_licence',
            'transport_vehicle_registration', 'transport_trailer_registration',
            'container_one_number', 'container_two_number',
            'container_one_seal_number', 'container_two_seal_number',
            'container_one_remarks_dispatch', 'container_two_remarks_dispatch',
            'container_one_remarks_reciept', 'container_two_remarks_reciept',
            'arrival_date', 'start_discharge_date', 'end_discharge_date',
            'distance', 'transport_dispach_signed_date', 'receipt_signed_date',
            'validated', 'sent_compas',
            'receipt_validated', 'receipt_sent_compas',
        )),
        ('stock_item', (
            'code', 'si_code', 
            ('commodity', ('code', 'name')),
        )),
        'number_of_units', 'number_units_good', 'number_units_lost', 'number_units_damaged', 
        ('units_lost_reason', ('cause',)), 
        ('units_damaged_reason', ('cause',)), 
        'overloaded_units', 'over_offload_units',
    )
    
    def read(self, request, waybill="", warehouse="", destination=""):
        """Return loading details for waybills in CSV"""
        load_details = self.model.objects.all()
        
        if not request.user.has_perm("ets.loadingetail_api_full_access"):
            warehouses = ets.models.Warehouse.filter_by_user(request.user)
            load_details = load_details.filter(Q(waybill__order__warehouse__in=warehouses) 
                                               | Q(waybill__destination__in=warehouses))
        
        filter_arg = {}
        if warehouse: 
            filter_arg['waybill__order__warehouse__pk'] = warehouse
        if destination:
            filter_arg['waybill__destination__pk'] = destination
        if waybill:
            filter_arg['waybill'] = waybill
        if filter_arg:
            load_details = load_details.filter(**filter_arg)            
        
        return load_details


class ReadOrdersHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Order
    fields = (
        'code', 'created', 'expiry', 'dispatch_date', 
        'transport_code', 'transport_ouc', 'transport_name', 
        'origin_type', 'project_number', 
        ('warehouse', ('code', 'name')),
        ('consignee', ('code', 'name')),
        ('location', ('code', 'name')),
    )
        
    def read(self, request, code="", warehouse="", destination="", consignee=""):
        """Return orders in CSV"""
        orders = self.model.objects.all()
     
        if not request.user.has_perm("ets.order_api_full_access"):
            orders = orders.filter(warehouse__in=ets.models.Warehouse.filter_by_user(request.user))
        
        filter_arg = {}
        if warehouse: 
            filter_arg['warehouse__pk'] = warehouse
        if destination:
            filter_arg['consignee__warehouses__pk'] = destination
        if consignee:
            filter_arg['consignee__pk'] = consignee
        if code:
            filter_arg['code'] = code
        if filter_arg:
            orders = orders.filter(**filter_arg)
        
        return orders
            

class ReadOrderItemsHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.OrderItem
    fields = (
        'lti_pk', 'si_code',
        ('order', (
            'code', 'created', 'expiry', 'dispatch_date', 
            'transport_code', 'transport_ouc', 'transport_name', 
            'origin_type', 'project_number', 
            ('warehouse', ('code',)),
            ('consignee', ('code',)),
            ('location', ('code',)),
        )),
        ('commodity', ('code', 'name')), 
        'number_of_units', 'lti_id',
    )
              
    def read(self, request, order="", warehouse="", destination="", consignee=""):
        """Return order items in CSV"""
        order_items = self.model.objects.all()
        
        if not request.user.has_perm("ets.orderitem_api_full_access"):
            order_items = order_items.filter(order__warehouse__in=ets.models.Warehouse.filter_by_user(request.user))
        
        filter_arg = {}
        
        if warehouse: 
            filter_arg['order__warehouse__pk'] = warehouse
        if destination:
            filter_arg['order__consignee__warehouses__pk'] = destination
        if consignee:
            filter_arg['order__consignee__pk'] = consignee
        if order:
            filter_arg['order'] = order
        if filter_arg:
            order_items = order_items.filter(**filter_arg)            
        
        return order_items
        
    
class ReadStockItemsHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.StockItem
    
    fields = (
      'code', 
      ('warehouse', ('code', 'name')),
      'project_number', 'si_code', 
      ('commodity', ('code', 'name')),
      ('package', ('code', 'name')),
      'quality_code', 'quality_description',
      'number_of_units', 'unit_weight_net', 'unit_weight_gross',
      'is_bulk', 'si_record_id', 'origin_id', 'allocation_code',
    )
        
    def read(self, request, warehouse=""):
        """Finds all sent waybills to provided destination"""
        
        stock_items = self.model.objects.all()
            
        if not request.user.has_perm("ets.stockitem_api_full_access"):
            stock_items = stock_items.filter(warehouse__in=ets.models.Warehouse.filter_by_user(request.user))
        
        if warehouse: 
            stock_items = stock_items.filter(warehouse=warehouse)
            
        return stock_items


class ReadCSVWarehouseHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Warehouse
    fields = (
        'code', 'name', ('location', ('name', 'country')),
    )
    
    def read(self, request):
        """country, location. warehouse information"""
        
        warehouses = self.model.objects.all()
        
        if not request.user.has_perm("ets.warehouse_api_full_access"):
            warehouses = self.model.filter_by_user(request.user)
        
        return warehouses
    

def get_flattened_field_names(fields):
    for field_name in fields:
        if isinstance(field_name, (str, unicode)):
            yield field_name
        elif isinstance(field_name, (tuple, list)):
            for wrapped_field in get_flattened_field_names(field_name[1]):
                yield "%s/%s" % (field_name[0], wrapped_field)


def get_flattened_data(data):
    for item in data:
        yield dict(get_flattened_dict(item))

def get_flattened_dict(data):
    for name, value in data.items():
        if isinstance(value, dict):
            for wrapped_key, wrapped_value in get_flattened_dict(value):
                yield "%s/%s" % (name, wrapped_key), wrapped_value
        else:
            yield name, value


class CSVEmitter(Emitter):
    """
    Emitter that returns CSV.
    """
    def render(self, request):
        result = StringIO.StringIO()
        
        field_names = list(get_flattened_field_names(self.fields))
        header = dict(zip(field_names, field_names))
        
        dict_writer = csv.DictWriter(result, field_names, dialect='excel', restval='')
        dict_writer.writerow(header)
        dict_writer.writerows(get_flattened_data(self.construct()))
        
        return result.getvalue()

Emitter.register('csv', CSVEmitter, 'application/csv')


