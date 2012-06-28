### -*- coding: utf-8 -*- ####################################################
import datetime
import csv
import StringIO


from django.db.models import Q, ForeignKey

from piston.handler import BaseHandler
from piston.emitters import Emitter
import xlwt

import ets.models
from ets.utils import (filter_for_orders, get_datatables_filtering,
                       get_dispatch_compas_filters, get_receipt_compas_filters)
from ets.api import unicodecsv
from ets.decorators import waybill_officer_related_filter, waybill_user_related_filter

def get_titles(model):
    """Extracts titles from model fields"""
    fields_name = {}
    for field in model._meta.fields:
        if ForeignKey == type(field):
            key = "%s%s" % (field.name, "_id")
            fields_name[key] = unicode(field.verbose_name)
        else:
            fields_name[field.name] = unicode(field.verbose_name)
    return fields_name   


class ReadWaybillHandler(BaseHandler):
    """ Waybill details without loading details """
    allowed_methods = ('GET',)
    model = ets.models.Waybill
    fields = (
        'slug',
        ('order', (
            'code', 'transport_code', 'transport_name', 'origin_type', 
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

    def read(self, request, slug="", warehouse="", destination="", filtering=None, format=""):
        """Return waybills in CSV"""
        waybills = self.model.objects.all()

        if filtering:
            officer_required = ets.models.Compas.objects.filter(officers=request.user).exists()
            if filtering == 'dispatches':
                waybills = self.model.dispatches(request.user)
            elif filtering == 'receptions':
                waybills = self.model.receptions(request.user)
            elif filtering == 'user_related':
                waybills = waybill_user_related_filter(waybills, request.user)
            elif filtering == 'compas_receipt':
                waybills = waybill_officer_related_filter(waybills.filter(receipt_sent_compas__isnull=False), request.user)
            elif filtering == 'compas_dispatch':
                waybills = waybill_officer_related_filter(waybills.filter(sent_compas__isnull=False), request.user)
            elif filtering == 'validate_receipt' and officer_required:
                waybills = waybills.filter(**get_receipt_compas_filters(request.user)).filter(receipt_validated=False)
            elif filtering == 'validate_dispatch' and officer_required:
                waybills = waybills.filter(**get_dispatch_compas_filters(request.user)).filter(validated=False)
            elif filtering == 'dispatch_validated' and officer_required:
                waybills = waybills.filter(**get_dispatch_compas_filters(request.user)).filter(validated=True)
            elif filtering == 'receipt_validated' and officer_required:
                waybills = waybills.filter(**get_receipt_compas_filters(request.user)).filter(receipt_validated=True)
        elif not request.user.has_perm("ets.waybill_api_full_access"):
            waybills = waybills.filter(order__warehouse__persons__pk=request.user.pk)

        if request.GET.has_key('sSearch'):
            waybills = get_datatables_filtering(request, waybills)

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
    """ Waybill details with loading details flattened """
    allowed_methods = ('GET',)
    model = ets.models.LoadingDetail
    
    fields = (
        'slug', 
        ('waybill', (
            'slug',
            ('order', (
                'code', 'transport_code', 'transport_name', 'origin_type',
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
            'code', 'si_code', 'project_number',
            ('commodity', ('code', 'name')),
        )),
        'number_of_units', 
        'unit_weight_net', 'unit_weight_gross',
        'total_weight_net', 'total_weight_gross',
        'number_units_good', 'number_units_lost', 'number_units_damaged', 
        ('units_lost_reason', ('cause',)), 
        ('units_damaged_reason', ('cause',)), 
        'overloaded_units', 'over_offload_units',
    )
    
    def read(self, request, waybill="", warehouse="", destination=""):
        """Return loading details for waybills in CSV"""
        load_details = self.model.objects.all()
        
        if not request.user.has_perm("ets.loadingetail_api_full_access"):
            load_details = load_details.filter(Q(waybill__order__warehouse__persons__pk=request.user.pk) 
                                               | Q(waybill__destination__persons__pk=request.user.pk))
        
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
    """ Order details without items """
    allowed_methods = ('GET',)
    model = ets.models.Order
    fields = (
        'code', 'created', 'expiry', 'dispatch_date', 
        'transport_code', 'transport_ouc', 'transport_name', 
        'origin_type', 
        ('warehouse', ('code', 'name')),
        ('consignee', ('code', 'name')),
        ('location', ('code', 'name')),
    )
        
    def read(self, request, code="", warehouse="", destination="", consignee="", format=""):
        """Return orders in CSV"""

        orders = self.model.objects.all()
        orders = orders.filter(**filter_for_orders())
     
        if not request.user.has_perm("ets.order_api_full_access"):
            orders = orders.filter(warehouse__persons__pk=request.user.pk)

        if request.GET.has_key('sSearch'):
            orders = get_datatables_filtering(request, orders)
        
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
    """ Order details with commodity items flattened """
    allowed_methods = ('GET',)
    model = ets.models.OrderItem
    fields = (
        'si_code', 'project_number',
        ('order', (
            'code', 'created', 'expiry', 'dispatch_date', 
            'transport_code', 'transport_ouc', 'transport_name', 
            'origin_type',
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
            order_items = order_items.filter(order__warehouse__persons__pk=request.user.pk)
        
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
    """Stock items"""
    allowed_methods = ('GET',)
    model = ets.models.StockItem
    
    fields = (
      'code', 
      ('warehouse', ('code', 'name')),
      'project_number', 'si_code', 
      ('commodity', ('code', 'name')),
      ('package', ('code', 'name')),
      'quality',
      'number_of_units', 'unit_weight_net', 'unit_weight_gross',
      'is_bulk', 'si_record_id', 'origin_id', 'allocation_code',
    )
        
    def read(self, request, warehouse="", format=""):
        """Finds all sent waybills to provided destination"""

        stock_items = self.model.objects.all()

        if request.GET.has_key('sSearch'):
            stock_items = get_datatables_filtering(request, stock_items)
        elif not request.user.has_perm("ets.stockitem_api_full_access"):
            stock_items = stock_items.filter(warehouse__persons__pk=request.user.pk)

        if warehouse: 
            stock_items = stock_items.filter(warehouse__pk=warehouse)

        return stock_items


class ReadCSVWarehouseHandler(BaseHandler):
    """Warehouse short information with code, name and location"""
    allowed_methods = ('GET',)
    model = ets.models.Warehouse
    fields = (
        'code', 'name', ('location', ('name', 'country')),
    )
    
    def read(self, request):
        """country, location. warehouse information"""
        
        warehouses = self.model.objects.all()
        
        if not request.user.has_perm("ets.warehouse_api_full_access"):
            warehouses = self.model.objects.filter(persons__pk=request.user.pk)
        
        return warehouses
    

def get_flattened_field_names(fields):
    """Generator to convert intermodel relations waybill__order__pk to getitem waybill.order.pk""" 
    for field_name in fields:
        if isinstance(field_name, (str, unicode)):
            yield field_name
        elif isinstance(field_name, (tuple, list)):
            for wrapped_field in get_flattened_field_names(field_name[1]):
                yield "%s.%s" % (field_name[0], wrapped_field)


def get_flattened_data(data):
    for item in data:
        yield dict(get_flattened_dict(item))

def get_flattened_dict(data):
    for name, value in data.items():
        if isinstance(value, dict):
            for wrapped_key, wrapped_value in get_flattened_dict(value):
                yield "%s.%s" % (name, wrapped_key), wrapped_value
        else:
            yield name, value


class CSVEmitter(Emitter):
    """Emitter that returns CSV file"""
    def render(self, request):

        result = StringIO.StringIO()
        
        field_names = list(get_flattened_field_names(self.fields))
        header = dict(zip(field_names, field_names))
        
        dict_writer = unicodecsv.UnicodeDictWriter(result, field_names, dialect=csv.excel_tab)
        dict_writer.writerow(header)
        dict_writer.writerows(get_flattened_data(self.construct()))
        
        return result.getvalue()

Emitter.register('csv', CSVEmitter, 'application/csv')

class ExcelEmitter(Emitter):
    """Emitter that returns Excel file"""
    def render(self, request):

        result = StringIO.StringIO()
        header = dict(enumerate(get_flattened_field_names(self.fields)))
        count = len(header)
        
        book = xlwt.Workbook()
        sheet = book.add_sheet('new')
        sheet.auto_style_outline = True
        for i in range(0, count):
            sheet.write(0, i, header[i])
        for row_index, row_contents in enumerate(get_flattened_data(self.construct())):
            for i in range(0, count):
                val = row_contents.get(header[i], "")
                if isinstance(val, str):
                    try:
                        val = int(val)
                        sheet.write(row_index + 1, i, val, xlwt.easyxf(num_format_str='#,##0'))
                    except ValueError:
                        sheet.write(row_index + 1, i, val, xlwt.easyxf(num_format_str='#,##0.00000'))
                elif isinstance(val, datetime.datetime):
                    sheet.write(row_index + 1, i, val, xlwt.easyxf(num_format_str='M/D/YY h:mm'))
                elif isinstance(val, datetime.date):
                    sheet.write(row_index + 1, i, val, xlwt.easyxf(num_format_str='M/D/YY'))
                else:
                    sheet.write(row_index + 1, i, val)
        book.save(result)
        
        return result.getvalue()

Emitter.register('excel', ExcelEmitter, 'application/excel')


