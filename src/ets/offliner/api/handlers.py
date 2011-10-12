from itertools import chain

from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core import serializers

from piston.emitters import Emitter, DjangoEmitter
from piston.handler import BaseHandler
import ets.models


class JSONOfflineHandler(BaseHandler):

    allowed_methods = ('GET','POST')
    model = ets.models.Waybill
    
    def read(self, request, warehouse_pk, start_date=None):
        """Return loading details for waybills in CSV"""
        result = []
        warehouse = get_object_or_404(ets.models.Warehouse, pk=warehouse_pk)    
        orders = ets.models.Order.objects.filter(warehouse__pk=warehouse_pk)
        waybills = ets.models.Waybill.objects.filter(order__warehouse__pk=warehouse_pk, transport_dispach_signed_date__isnull=False)
        waybills_log = ets.models.Waybill.audit_log.all()
        lodaing_details_log = ets.models.Waybill.audit_log.all()
        if start_date:
            orders = orders.filter(Q(created__gte=start_date) | Q(updated__gte=start_date))
            waybills = waybills.filter(Q(date_created__gte=start_date) | Q(date_modified__gte=start_date))
            waybills_log = waybills_log.filter(action_date__gte=start_date)
            lodaing_details_log = lodaing_details_log.filter(action_date__gte=start_date)
        for i in chain(ets.models.Person.objects.distinct().filter(Q(compas__warehouses__pk=warehouse_pk) |
                  Q(location__warehouses__in=warehouse_pk) | Q(organization__warehouses__pk=warehouse_pk)),
                  ets.models.StockItem.objects.filter(warehouse__pk=warehouse_pk),   
                  orders, ets.models.OrderItem.objects.filter(order__in=orders), 
                  waybills, ets.models.LoadingDetail.objects.filter(waybill__in=waybills),
                  waybills_log, lodaing_details_log
        ):
            result.append(i)
        result.append(warehouse.location)
        result.append(warehouse.compas)
        result.append(warehouse.organization)
        return result

    def create(self, request, warehouse_pk):

        if request.content_type:
            data = request.data
            objects = serializers.deserialize('python', data)
            for wrapper in objects:
                wrapper.save()
    

class DjangoJSONEmitter(DjangoEmitter):
    """
    Emitter for the Django serialized format in JSON.
    """
    def render(self, request, format='json'):
        return super(DjangoJSONEmitter,self).render(request, format=format)

Emitter.register('django_json', DjangoJSONEmitter, 'application/json; charset=utf-8')
