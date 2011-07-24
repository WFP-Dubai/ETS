### -*- coding: utf-8 -*- ####################################################

#from datetime import datetime
#from decimal import Decimal

#from django.http import Http404
#import httplib, logging

from piston.handler import BaseHandler

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

    def read(self, request):
        """
        Method **read** of **Waybill** handler used to retrieve all Waybill objects existing in database.
        It can be useful for initial database loading without any filtering.

        **URL** : */api/history/*
        """
        return self.model.objects.all()

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history', [])


#=======================================================================================================================
# class HistoryIdHandler(BaseHandler):
# 
#    allowed_methods = ('GET',)
#    model = History
#    fields = (('user',("username",)), 'date', 'cash')
# #    exclude = ('resource_uri',)
# 
#    def read(self, request, object_id):
#        """
#        Method **read** of **HistoryIdHandler** handler used to retrieve History objects filtered by *object_id*.
# 
#        - *object_id* - ID of history object in database
#        - *restrict* - optional argument of GET query. If present result set limits will be restricted. Argument value will not affect the result.
# 
#        When **restrict** argument of query provided then only one **History** object with ID equal to **object_id**
#          will be returned otherwise method will fetch all **History** objects with with ID greater than **object_id** value.
# 
#        **URL** : */mall/api/history/id/{object_id}/*
#        """
#        restrict = 'restrict' in request.GET
# 
#        if restrict:
#            return self.model.objects.filter(id=object_id)
#        else:
#            return self.model.objects.filter(id__gt=object_id)
#=======================================================================================================================

#    @staticmethod
#    def resource_uri(*args, **kwargs):
#        return ('history_id', {'object_id':'id'})
