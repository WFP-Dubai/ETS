from functools import wraps

from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import available_attrs

import ets.models
from ets.utils import get_dispatch_compas_filters, get_receipt_compas_filters

#Authentication decorators. If condition fails user is redirected to login form
superuser_required = user_passes_test(lambda u: u.is_superuser)
person_required = user_passes_test(lambda u: hasattr(u, 'person'))
officer_required = user_passes_test(lambda u: ets.models.Compas.objects.filter(officers=u).exists())
dispatcher_required = user_passes_test(lambda u: (hasattr(u, 'person') and u.person.dispatch))
recipient_required = user_passes_test(lambda u: (hasattr(u, 'person') and u.person.receive))

def user_filtered(function=None, felter=lambda queryset, user: ()):
    """Decorates view function and inserts queryset filtered by user"""
    
    def _decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, queryset=None, *args, **kwargs):
            return view_func(request, queryset=felter(queryset, request.user), *args, **kwargs)
        return _wrapped_view
    
    if function:
        return _decorator(function)
    
    return _decorator

#Decorators or views.
dispatch_view = user_filtered(felter=lambda queryset, user: ets.models.Waybill.dispatches(user))

receipt_view = user_filtered(felter=lambda queryset, user: ets.models.Waybill.receptions(user))

warehouse_related = user_filtered(felter=lambda queryset, user: queryset.filter(warehouse__persons__pk=user.pk))

def waybill_user_related_filter(queryset, user):
    """
    Returns a queryset with filter by user in widest range: 
    it could be a dispatcher, a recepient, officer of both compases.
    Status of waybill does not matter.
    """
    if not user.is_superuser:
    
        #possible further optimization with persons
        queryset = queryset.filter(Q(order__warehouse__persons__pk=user.pk) 
                               | Q(order__warehouse__compas__officers__pk = user.pk)
                               | Q(destination__persons__pk=user.pk)
                               | Q(destination__compas__officers__pk = user.pk)).distinct()
    return queryset

waybill_user_related = user_filtered(felter=waybill_user_related_filter)

def waybill_officer_related_filter(queryset, user):
    """
    Returns a queryset with filter by user in widest range: 
    it could be a dispatcher, a recepient, officer of both compases.
    Status of waybill does not matter.
    """
    if not user.is_superuser:
    
        queryset = queryset.filter(Q(order__warehouse__compas__officers__pk = user.pk)
                               | Q(destination__compas__officers__pk = user.pk)).distinct()
    return queryset

waybill_officer_related = user_filtered(felter=waybill_officer_related_filter)

#Validation
dispatch_compas = user_filtered(felter=lambda queryset, user: queryset.filter(**get_dispatch_compas_filters(user)))
receipt_compas = user_filtered(felter=lambda queryset, user: queryset.filter(**get_receipt_compas_filters(user)))

