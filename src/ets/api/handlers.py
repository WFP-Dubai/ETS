### -*- coding: utf-8 -*- ####################################################

#from datetime import datetime
#from decimal import Decimal
import csv
import StringIO
from types import DictType


#from django.http import Http404
#import httplib, logging
from django.core import serializers
from django.db import transaction
from django.db.models import Q, Sum, Count

from piston.handler import BaseHandler
from piston.utils import rc, Mimer
from piston.emitters import Emitter, DjangoEmitter

from ..models import Waybill, LoadingDetail, Place, sync_data

class PlaceHandler(BaseHandler):

    #allowed_methods = ('GET',)
    model = Place
    exclude = ('_state',)


#===============================================================================
# class WaybillHandler(BaseHandler):
# 
#    allowed_methods = ('GET',)
#    model = Waybill
#===============================================================================

class ReadCSVWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    
    def read(self, request, slug="", warehouse="", destination=""):
        """Finds all sent waybills to provided destination"""
        #return self.model.objects.all().annotate(total_net=Sum('loading_details__calculate_total_net'))
        filter_arg = {}
        if warehouse: 
            filter_arg['warehouse__code'] = warehouse
        if destination:
            filter_arg['destination__code'] = destination
        if slug:
            filter_arg['slug'] = slug
        if filter_arg:
            return self.model.objects.filter(**filter_arg).values()
        else:
            return self.model.objects.values()
             
        
class ReadCSVLoadingDetailHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = LoadingDetail
    
    def read(self, request, waybill="", warehouse="", destination=""):
        """Finds all sent waybills to provided destination"""
        filter_arg = {}
        if warehouse: 
            filter_arg['waybill__warehouse__code'] = warehouse
        if destination:
            filter_arg['waybill__destination__code'] = destination
        if waybill:
            filter_arg['waybill'] = waybill
        if filter_arg:
            load_details = self.model.objects.filter(**filter_arg).values()
        else:
            load_details = self.model.objects.all().values()         
        result = []
        for detail in load_details:
            waybills_data = Waybill.objects.filter(pk=detail['waybill_id']).values()[0]
            waybills_data.update(detail)
            result.append(waybills_data)  
        return result
            


class NewWaybillHandler(BaseHandler):

    allowed_methods = ('POST',)
    model = Waybill
    
    @transaction.commit_on_success
    def create(self, request):
        if request.content_type:
            data = request.data
            
            for obj in serializers.deserialize('python', data):
                obj.save()
                if hasattr(obj.object, 'update_status'):
                    obj.object.update_status(self.model.SENT)
            
            return rc.CREATED
        else:
            super(NewWaybillHandler, self).create(request)
    

class ReceivingWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    
    def read(self, request, destination):
        """Finds all sent waybills to provided destination"""
        return sync_data(self.model.objects.filter(status=self.model.SENT, destination__pk=destination))



class InformedWaybillHandler(BaseHandler):

    allowed_methods = ('GET', 'PUT')
    model = Waybill
    fields = ('pk',)
    
    def read(self, request, *args, **kwargs):
        obj = super(InformedWaybillHandler, self).read(request, *args, **kwargs)
        return obj.status == obj.INFORMED and obj
    
    def update(self, request):
        if hasattr(request, 'data'):
            self.model.objects.filter(pk__in=request.data, status__lt=self.model.INFORMED)\
                              .update(status=self.model.INFORMED)
            return rc.ALL_OK
        else:
            return rc.BAD_REQUEST
        

class DeliveredWaybillHandler(BaseHandler):

    allowed_methods = ('GET', 'PUT')
    model = Waybill
    #fields = ('pk',)
    
    def read(self, request, *args, **kwargs):
        obj = super(DeliveredWaybillHandler, self).read(request, *args, **kwargs)
        return obj.status == obj.DELIVERED and [obj]
    
    def update(self, request):
        if hasattr(request, 'data') and request.data:
            for obj in serializers.deserialize('python', request.data):
                obj.save()
 
            return rc.ALL_OK
        else:
            return rc.BAD_REQUEST


class DjangoJsonEmitter(DjangoEmitter):
    """
    Emitter for the Django serialized json format.
    """
    def render(self, request):

        return super(DjangoJsonEmitter, self).render(request, 'json')
        
Emitter.register('django_json', DjangoJsonEmitter, 'application/json; charset=utf-8')


class CSVEmitter(Emitter):
    """
    Emitter that returns CSV.
    """
    def render(self, request):
        result = StringIO.StringIO()
        if type(self.construct()[0]) is DictType:
            fieldnames = self.construct()[0].keys()
            dict_writer = csv.DictWriter(result, fieldnames, dialect='excel')
            header = {}
            for field in fieldnames:
                header[field] = field
            dict_writer.writerow(header)
            dict_writer.writerows(self.construct())
        else: 
            writer = csv.writer(result)
            writer.writerows(self.construct())
        return result.getvalue()
        
        
Emitter.register('csv', CSVEmitter, 'application/csv')
