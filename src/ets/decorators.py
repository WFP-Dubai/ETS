from functools import wraps

from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import available_attrs

import ets.models


#Authentication decorators. If condition fails user is redirected to login form
person_required = user_passes_test(lambda u: ets.models.Person.objects.filter(user=u).count())
officer_required = user_passes_test(lambda u: ets.models.Compas.objects.filter(officers=u).count())

def user_filtered(function=None, filter=lambda queryset, user: ()):
    """Decorates view function and inserts queryset filtered by user"""
    
    def _decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, queryset=None, *args, **kwargs):
            return view_func(request, queryset=filter(queryset, request.user), *args, **kwargs)
        return _wrapped_view
    
    if function:
        return _decorator(function)
    
    return _decorator

#Decorators or views.
dispatch_view = user_filtered(filter=lambda queryset, user: ets.models.Waybill.dispatches(user))
receipt_view = user_filtered(filter=lambda queryset, user: ets.models.Waybill.receptions(user))

warehouse_related = user_filtered(filter=lambda queryset, user: queryset.filter(warehouse__in=ets.models.Warehouse.filter_by_user(user)))

def waybill_user_related_filter(queryset, user):
    """
    Returns a queryset with filter by user in widest range: 
    it could be a dispatcher, a recepient, officer of both compases.
    Status of waybill does not matter.
    """
    warehouses = ets.models.Warehouse.filter_by_user(user)
    return queryset.filter(Q(order__warehouse__in=warehouses) 
                           | Q(order__warehouse__compas__officers=user)
                           | Q(destination__in=warehouses)
                           | Q(destination__compas__officers=user))
                           
waybill_user_related = user_filtered(filter=waybill_user_related_filter)

#Validation
dispatch_compas = user_filtered(filter=lambda queryset, user: queryset.filter(
                        transport_dispach_signed_date__isnull=False, 
                        sent_compas__isnull=True, 
                        order__warehouse__compas__officers=user))

receipt_compas = user_filtered(filter=lambda queryset, user: queryset.filter(
                         transport_dispach_signed_date__isnull=False, 
                         receipt_signed_date__isnull=False, 
                         receipt_sent_compas__isnull=True, 
                         destination__compas__officers=user))
