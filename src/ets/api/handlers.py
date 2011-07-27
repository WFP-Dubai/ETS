### -*- coding: utf-8 -*- ####################################################

#from datetime import datetime
#from decimal import Decimal

#from django.http import Http404
#import httplib, logging
from django.core import serializers

from piston.handler import BaseHandler
from piston.utils import rc

from ..models import Waybill, Place

class PlaceHandler(BaseHandler):

    #allowed_methods = ('GET',)
    model = Place
    exclude = ('_state',)


class WaybillHandler(BaseHandler):

    allowed_methods = ('GET',)
    model = Waybill
    #fields = (('user', ("username",)), 'ltiNumber', 'waybillNumber')
#    exclude = ('resource_uri',)
    
    def create(self, request):
        if request.content_type:
            data = request.data
            print "data --> ", data
            
            waybill = self.model(**data)
            waybill.save()
            
            for place_data in data['destinationWarehouse']:
                Place(destinationWarehouse=waybill, content=place_data['content']).save()
                
            return rc.CREATED
        else:
            super(WaybillHandler, self).create(request)
    
    
#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history', [])



class NewWaybillHandler(BaseHandler):

    allowed_methods = ('GET', 'POST')
    model = Waybill
    #fields = (('user', ("username",)), 'ltiNumber', 'waybillNumber')
#    exclude = ('resource_uri',)
    
    def create(self, request):
        if request.content_type:
            data = request.data
            
            for obj in serializers.deserialize('python', data):
                obj.save()
            
            return rc.CREATED
        else:
            super(NewWaybillHandler, self).create(request)
    