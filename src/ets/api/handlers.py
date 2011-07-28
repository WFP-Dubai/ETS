### -*- coding: utf-8 -*- ####################################################

#from datetime import datetime
#from decimal import Decimal

#from django.http import Http404
#import httplib, logging
from django.core import serializers
from django.db import transaction

from piston.handler import BaseHandler
from piston.utils import rc
from piston.emitters import Emitter, DjangoEmitter

from ..models import Waybill, Place, sync_data

class PlaceHandler(BaseHandler):

    #allowed_methods = ('GET',)
    model = Place
    exclude = ('_state',)


class WaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill


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
        return sync_data(self.model.objects.filter(status=self.model.SENT, destinationWarehouse__pk=destination))



class InformedWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    fields = ('pk',)
    
    def read(self, request, *args, **kwargs):
        obj = super(InformedWaybillHandler, self).read(request, *args, **kwargs)
        return obj.status == obj.INFORMED and obj


class DeliveredWaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    #fields = ('pk',)
    
    def read(self, request, *args, **kwargs):
        obj = super(DeliveredWaybillHandler, self).read(request, *args, **kwargs)
        return obj.status == obj.DELIVERED and [obj]


class DjangoJsonEmitter(DjangoEmitter):
    """
    Emitter for the Django serialized json format.
    """
    def render(self, request):
        return super(DjangoJsonEmitter, self).render(request, 'json')
        
Emitter.register('django_json', DjangoJsonEmitter, 'text/json; charset=utf-8')
