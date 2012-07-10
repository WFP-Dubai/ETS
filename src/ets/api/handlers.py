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

    def read(self, request, slug="", warehouse="", destination="", filtering=None, **kwargs):
        """Return waybills in CSV"""
        waybills = self.model.objects.all()

        if filtering:
            officer_required = ets.models.Compas.objects.filter(officers=request.user).exists()

            filter_choice = {
                'dispatches': lambda user: self.model.dispatches(user),
                'receptions': lambda user: self.model.receptions(user),
                'user_related': lambda user: waybill_user_related_filter(waybills, user),
                'compas_receipt': lambda user: waybill_officer_related_filter(waybills.filter(receipt_sent_compas__isnull=False), user),
                'compas_dispatch': lambda user: waybill_officer_related_filter(waybills.filter(sent_compas__isnull=False), user),
                'validate_receipt': lambda user: officer_required and waybills.filter(**get_receipt_compas_filters(user)).filter(receipt_validated=False),
                'validate_dispatch': lambda user: officer_required and waybills.filter(**get_dispatch_compas_filters(user)).filter(validated=False),
                'dispatch_validated': lambda user: officer_required and waybills.filter(**get_dispatch_compas_filters(user)).filter(validated=True),
                'receipt_validated': lambda user: officer_required and waybills.filter(**get_receipt_compas_filters(user)).filter(receipt_validated=True),
            }
            waybills = filter_choice[filtering](request.user)

        elif not request.user.has_perm("ets.waybill_api_full_access"):
            waybills = waybills.filter(order__warehouse__persons__pk=request.user.pk)

        if request.GET.has_key('sSearch'):
            waybills = get_datatables_filtering(request, waybills)

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
    
    def read(self, request, waybill="", warehouse="", destination="", **kwargs):
        """Return loading details for waybills"""
        load_details = self.model.objects.all()
        
        if not request.user.has_perm("ets.loadingetail_api_full_access"):
            load_details = load_details.filter(Q(waybill__order__warehouse__persons__pk=request.user.pk) 
                                               | Q(waybill__destination__persons__pk=request.user.pk))
        
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
        
    def read(self, request, code="", warehouse="", destination="", consignee="", **kwargs):
        """Return orders"""

        orders = self.model.objects.all()
        orders = orders.filter(**filter_for_orders())
     
        if not request.user.has_perm("ets.order_api_full_access"):
            orders = orders.filter(warehouse__persons__pk=request.user.pk)

        if request.GET.has_key('sSearch'):
            orders = get_datatables_filtering(request, orders)
        
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
              
    def read(self, request, order="", warehouse="", destination="", consignee="", **kwargs):
        """Return order items"""
        order_items = self.model.objects.all().distinct()
        
        order_items = order_items.filter(**dict([("order__%s" % key, value) for key, value in filter_for_orders().items()]))
        
        if not request.user.has_perm("ets.orderitem_api_full_access"):
            order_items = order_items.filter(order__warehouse__persons__pk=request.user.pk)
        
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
        
    def read(self, request, warehouse="", **kwargs):
        """Finds all sent waybills to provided destination"""

        stock_items = self.model.objects.all()

        if request.GET.has_key('sSearch'):
            stock_items = get_datatables_filtering(request, stock_items)
        elif not request.user.is_superuser and not request.user.has_perm("ets.loadingetail_api_full_access"):
            stock_items = stock_items.filter(Q(warehouse__persons__pk=request.user.pk) | Q(warehouse__compas__officers=request.user))

        if warehouse: 
            stock_items = stock_items.filter(warehouse__pk=warehouse)

        return stock_items


class ReadWarehouseHandler(BaseHandler):
    """Warehouse short information with code, name and location"""
    allowed_methods = ('GET',)
    model = ets.models.Warehouse
    fields = (
        'code', 'name', ('location', ('name', 'country')),
    )
    
    def read(self, request, **kwargs):
        """country, location. warehouse information"""

        warehouses = self.model.objects.all()

        if request.GET.has_key('sSearch'):
            warehouses = get_datatables_filtering(request, self.model.get_active_warehouses())
        elif not request.user.is_superuser:
            warehouses = warehouses.filter(Q(persons__pk=request.user.pk) | Q(compas__officers=request.user))

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
        
        field_names = tuple(get_flattened_field_names(self.fields))
        
        dict_writer = unicodecsv.UnicodeDictWriter(result, field_names, dialect=csv.excel_tab)
        dict_writer.writerow(dict(zip(field_names, field_names)))
        dict_writer.writerows(get_flattened_data(self.construct()))
        
        return result.getvalue()

Emitter.register('csv', CSVEmitter, 'application/csv')

def detect_style(val):
    if isinstance(val, str):
        for typ in [int, float]:
            try:
                val = typ(val)
                return val, typ
            except ValueError:
                pass

class ExcelEmitter(Emitter):
    """Emitter that returns Excel file"""
    def render(self, request):

        result = StringIO.StringIO()
        header = dict(enumerate(get_flattened_field_names(self.fields)))
        count = len(header)
        
        book = xlwt.Workbook()
        sheet = book.add_sheet('new')
        styles = {
            datetime.date: xlwt.easyxf(num_format_str='M/D/YY'),
            int: xlwt.easyxf(num_format_str='#,##0'),
            float: xlwt.easyxf(num_format_str='#,##0.00000'),
            datetime.datetime: xlwt.easyxf(num_format_str='M/D/YY h:mm'),
            unicode: xlwt.easyxf(),
        }
        styles['default'] = styles[unicode]
        
        for i in range(0, count):
            sheet.write(0, i, header[i])
        for row_index, row_contents in enumerate(get_flattened_data(self.construct())):
            for i in range(0, count):
                val = row_contents.get(header[i], "")
                val, key = (val, type(val)) if styles.has_key(type(val)) else detect_style(val) or (val, 'default')
                sheet.write(row_index + 1, i, val, styles[key])
        book.save(result)
        
        return result.getvalue()

Emitter.register('excel', ExcelEmitter, 'application/excel')


