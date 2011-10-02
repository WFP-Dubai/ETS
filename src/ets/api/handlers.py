### -*- coding: utf-8 -*- ####################################################
import datetime
#from decimal import Decimal
import csv
import StringIO
from types import DictType
from itertools import chain


#from django.http import Http404
#import httplib, logging
from django.core import serializers
from django.db import transaction
from django.db.models import Q, Sum, Count, ForeignKey
from django.utils.html import escape
from django.http import HttpResponse

from piston.handler import BaseHandler
from piston.utils import rc
from piston.emitters import Emitter, DjangoEmitter

from ..models import Waybill, Warehouse
import ets.models
from django.shortcuts import get_object_or_404


def get_titles(model):
    fields_name = {}
    for field in model._meta.fields:
        if ForeignKey == type(field):
            key = "%s%s" % (field.name, "_id")
            fields_name[key] = unicode(field.verbose_name)
        else:
            fields_name[field.name] = unicode(field.verbose_name)
    return fields_name   


class ReadCSVWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Waybill

    def read(self, request, slug="", warehouse="", destination=""):
        """Return waybills in CSV"""
        #return self.model.objects.all().annotate(total_net=Sum('loading_details__calculate_total_net'))
        waybills = self.model.objects.filter(order__warehouse__in=Warehouse.filter_by_user(request.user)).values()
        filter_arg = {}
        if warehouse: 
            filter_arg['order__warehouse__pk'] = warehouse
        if destination:
            filter_arg['destination__pk'] = destination
        if slug:
            filter_arg['slug'] = slug
        if filter_arg:
            waybills = waybills.filter(**filter_arg)
        titles = get_titles(self.model)
        return [titles] + list(waybills.values())
           
        
class ReadCSVLoadingDetailHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.LoadingDetail
    
    def read(self, request, waybill="", warehouse="", destination=""):
        """Return loading details for waybills in CSV"""
        load_details = self.model.objects.filter(waybill__order__warehouse__in=Warehouse.filter_by_user(request.user)).values()
        filter_arg = {}
        if warehouse: 
            filter_arg['waybill__order__warehouse__pk'] = warehouse
        if destination:
            filter_arg['waybill__destination__pk'] = destination
        if waybill:
            filter_arg['waybill'] = waybill
        if filter_arg:
            load_details = load_details.filter(**filter_arg)            
        titles = get_titles(self.model)
        titles.update(get_titles(ets.models.Waybill))      
        result = [titles]
        for detail in load_details:
            waybills_data = ets.models.Waybill.objects.filter(pk=detail['waybill_id']).values()[0]
            waybills_data.update(detail)
            result.append(waybills_data)  
        return result


class ReadCSVOrdersHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Order
    
    def read(self, request, code="", warehouse="", destination="", consignee=""):
        """Return orders in CSV"""
        orders = self.model.objects.filter(warehouse__in=Warehouse.filter_by_user(request.user)).values()
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
        titles = get_titles(self.model)
        return [titles] + list(orders.values())
            

class ReadCSVOrderItemsHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.OrderItem
    
    def read(self, request, order="", warehouse="", destination="", consignee=""):
        """Return order items in CSV"""
        order_items = self.model.objects.filter(order__warehouse__in=Warehouse.filter_by_user(request.user)).values()
        filter_arg = {}
        #queryset = queryset.filter(order__warehouse__in=ets.models.Warehouse.filter_by_user(request.user))
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
        titles = get_titles(self.model)
        titles.update(get_titles(ets.models.Order))                     
        result = [titles]
        for item in order_items:
            order_items_data = ets.models.Order.objects.filter(code=item['order_id']).values()[0]
            order_items_data.update(item)
            result.append(order_items_data)         
        return result
        
    
class ReadCSVStockItemsHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.StockItem
    
    def read(self, request, warehouse=""):
        """Finds all sent waybills to provided destination"""
        stock_items = self.model.objects.filter(warehouse__in=Warehouse.filter_by_user(request.user)).values()
        if warehouse: 
            stock_items = stock_items.filter(warehouse=warehouse)       
        titles = get_titles(self.model)
        titles.update(get_titles(ets.models.Warehouse))   
        result = [titles]
        for item in stock_items:
            stock_items_data = ets.models.Warehouse.objects.filter(pk=item['warehouse_id']).values()[0]
            stock_items_data.update(item)
            result.append(stock_items_data)  
        return result

class ReadJSONOfflineHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = ets.models.Waybill
    
    def read(self, request, warehouse_pk, start_date=""):
        """Return loading details for waybills in CSV"""
        result = []
        warehouse = get_object_or_404(ets.models.Warehouse, pk=warehouse_pk)    
        orders = ets.models.Order.objects.filter(warehouse__pk=warehouse_pk)
        waybills = ets.models.Waybill.objects.filter(order__warehouse__pk=warehouse_pk)
        if start_date:
            orders = orders.filter(Q(created__gte=start_date) | Q(updated__gte=start_date))
            waybills = waybills.filter(Q(date_created__gte=start_date) | Q(date_modified__gte=start_date))
        for i in chain(ets.models.Person.objects.distinct().filter(Q(compas__warehouses__pk=warehouse_pk) |
                  Q(location__warehouses__in=warehouse_pk) | Q(organization__warehouses__pk=warehouse_pk)),
                  ets.models.StockItem.objects.filter(warehouse__pk=warehouse_pk),   
                  orders, ets.models.OrderItem.objects.filter(order__in=orders), 
                  waybills, ets.models.LoadingDetail.objects.filter(waybill__in=waybills)):
            result.append(i)
        result.append(warehouse.location)
        result.append(warehouse.compas)
        result.append(warehouse.organization)
        return result
 
class CreateJSONHandler(BaseHandler):

    allowed_methods = ('PUT',)
    model = ets.models.Waybill
       
    def create(self, request):
        if request.content_type:
            data = request.data
            
            em = self.model(title=data['title'], content=data['content'])
            em.save()
            
            for loading_detail in data['loading_details']:
                Loading_detail(parent=em, content=comment['content']).save()
                
            return rc.CREATED
        else:
            super(ExpressiveTestModel, self).create(request)


class CSVEmitter(Emitter):
    """
    Emitter that returns CSV.
    """
    def render(self, request):
        result = StringIO.StringIO()
        if type(self.construct()[0]) is DictType:
            fieldnames = self.construct()[0].keys()
            dict_writer = csv.DictWriter(result, fieldnames, dialect='excel', restval='')
#            header = {}
#            for field in fieldnames:
#                header[field] = field
#            dict_writer.writerow(header)
            dict_writer.writerows(self.construct())
        else: 
            writer = csv.writer(result)
            writer.writerows(self.construct())
        return result.getvalue()
            
Emitter.register('csv', CSVEmitter, 'application/csv')

class DjangoJSONEmitter(DjangoEmitter):
    """
    Emitter for the Django serialized format in JSON.
    """
    def render(self, request, format='json'):
        print format
        return super(DjangoJSONEmitter,self).render(request, format=format)

Emitter.register('django_json', DjangoJSONEmitter, 'text/json; charset=utf-8')

