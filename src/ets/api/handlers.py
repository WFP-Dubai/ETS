### -*- coding: utf-8 -*- ####################################################

#from datetime import datetime
#from decimal import Decimal
import csv
import cStringIO


#from django.http import Http404
#import httplib, logging
from django.core import serializers
from django.db import transaction
from django.db.models import Sum, Count

from piston.handler import BaseHandler
from piston.utils import rc, Mimer
from piston.emitters import Emitter, DjangoEmitter

from ..models import Waybill, Place, sync_data, csv_sync_waybill

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

class ReadCSVAllWaybillsHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    
    def read(self, request):
        """Finds all sent waybills to provided destination"""
        #return self.model.objects.all().annotate(total_net=Sum('loading_details__calculate_total_net'))
        return self.model.objects.all().values_list()
        

class ReadCSVWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    
    def read(self, request, slug):
        """Finds all sent waybills to provided destination"""
        return csv_sync_waybill(self.model.objects.get(slug=slug))


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
        print type(self.construct())
        for i in self.construct():
            print i
        result = cStringIO.StringIO()
        writer = csv.writer(result)
        writer.writerows(self.construct())
        return result.getvalue()
        
Emitter.register('csv', CSVEmitter, 'application/csv')
