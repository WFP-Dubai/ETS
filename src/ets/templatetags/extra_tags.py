import datetime

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.db.models import Sum
from django.db.models.aggregates import Max

from native_tags.decorators import function, block

#from ets import settings
from ets.models import Warehouse, Waybill, Person, Compas, LoadingDetail, StockItem, ImportLogger, Order
from ets.utils import changed_fields, get_compases

register = template.Library()

@register.inclusion_tag('tags/give_link.html')
def waybill_edit(waybill, user, text=_("Edit")):
    return { 
            'text': text,
            'url': reverse('waybill_edit', kwargs={'waybill_pk': waybill.pk, 'order_pk':waybill.order.pk }),
            'success': waybill.has_dispatch_permission(user),
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_reception(waybill, user, text=_("Receive")):
    return { 
            'text': text,
            'url': reverse('waybill_reception', kwargs={'waybill_pk': waybill.pk}),
            'success': waybill.has_receive_permission(user),
    }


@register.inclusion_tag('tags/give_link.html')
def waybill_creation(order, user, text=_("Create")):
    return { 
            'text': text,
            'url': reverse('waybill_create', kwargs={'order_pk': order.pk}),
            'success': order.has_waybill_creation_permission(user),
    }


@function
def sign_dispatch(waybill, user):
    return waybill.has_dispatch_permission(user)

@function
def sign_reception(waybill, user):
    return (not hasattr(user, 'person') or user.person.receive) \
            and waybill.is_received() \
            and Waybill.receptions(user).filter(pk=waybill.pk).exists()


@register.inclusion_tag('tags/form.html')
def validate_dispatch(waybill, user, link_text=_("Validate dispatch")):
    queryset = Waybill.objects.filter(sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                          .filter(order__warehouse__compas__officers=user) \
                          .filter(validated=False)

    return { 
            'text': link_text,
            'url': reverse('validate_dispatch', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).exists(),
            'dialog_question': _("Are you sure you want to validate this waybill?"),
    }


@register.inclusion_tag('tags/form.html')
def validate_receipt(waybill, user, link_text=_("Validate receipt")):
    queryset = Waybill.objects.filter(receipt_sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                              .filter(receipt_signed_date__isnull=False) \
                              .filter(receipt_warehouse__compas__officers=user) \
                              .filter(receipt_validated=False)

    return { 
        'text': link_text,
        'url': reverse('validate_receipt', kwargs={'waybill_pk': waybill.pk,}),
        'success': queryset.filter(pk=waybill.pk).exists(),
        'dialog_question': _("Are you sure you want to validate this waybill?"),
    }

@register.inclusion_tag('tags/form.html')
def waybill_delete(waybill, user, text=_("Delete"), redirect_to=''):
    return { 
        'text': text,
        'url': "%s?%s" % (reverse('waybill_delete', kwargs={'waybill_pk': waybill.pk}), urlencode({'redirect_to': redirect_to})),
        'success': waybill.has_dispatch_permission(user),
        'dialog_question': _("Are you sure you want to delete this waybill?"),
    }

@block
def person_only(context, nodelist, user):
    return hasattr(user, 'person') and nodelist.render(context) or ''

@block
def officer_only(context, nodelist, user):
    return Compas.objects.filter(officers=user).exists() and nodelist.render(context) or ''

@register.inclusion_tag('sync/sync_form.html')
def sync_compas_form(compas, user):
    return { 
        'access_granted': user.is_superuser or Compas.objects.filter(pk=compas.pk, officers__pk=user.pk).exists(),
        'station': compas,
        'base_locked': compas.is_locked(base=True),
        'update_locked': compas.is_locked(base=False),
    }

def user_compases(user):
    return get_compases(user).values_list('pk', flat=True)
user_compases = function(user_compases, cache=3600)


@register.inclusion_tag('last_updated.html')
def get_last_update(user):
    """dummy function, just a wrapper"""
    
    failed = False
    compases = get_compases(user)
    for c in compases:
        try:
            if c.get_last_attempt().status == ImportLogger.FAILURE:
                failed = True
        except (ImportLogger.DoesNotExist, IndexError):
            pass
         
    return {
        'last_updated': compases.aggregate(last_updated=Max('warehouses__stock_items__updated'))['last_updated'],
        'failed': failed,
    }
