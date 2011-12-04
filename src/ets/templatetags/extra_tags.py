import datetime

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlencode
from django.db.models import Sum
from django.db.models.aggregates import Max

from native_tags.decorators import function, block

#from ets import settings
from ets.models import Warehouse, Waybill, Person, Compas, LoadingDetail, StockItem
from ets.utils import changed_fields

register = template.Library()

@register.inclusion_tag('tags/give_link.html')
def waybill_edit(waybill, user, text=_("Edit")):
    return { 
            'text': text,
            'url': reverse('waybill_edit', kwargs={'waybill_pk': waybill.pk, 'order_pk':waybill.order.pk }),
            'success': (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=waybill.pk).count(),
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_reception(waybill, user, text=_("Receive")):
    return { 
            'text': text,
            'url': reverse('waybill_reception', kwargs={'waybill_pk': waybill.pk}),
            'success': (not hasattr(user, 'person') or user.person.receive) and Waybill.receptions(user).filter(pk=waybill.pk).count(),
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_creation(order, user, text=_("Create")):
    return { 
            'text': text,
            'url': reverse('waybill_create', kwargs={'order_pk': order.pk}),
            'success': (not hasattr(user, 'person') or user.person.dispatch) and Warehouse.filter_by_user(user).filter(pk=order.warehouse.pk).count(),
    }
    

@function
def sign_dispatch(waybill, user):
    return (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=waybill.pk).count()

@function
def sign_reception(waybill, user):
    return (not hasattr(user, 'person') or user.person.receive) and Waybill.receptions(user).filter(pk=waybill.pk).count()


@register.inclusion_tag('tags/form.html')
def validate_dispatch(waybill, user, link_text=_("Validate dispatch")):
    queryset = Waybill.objects.filter(sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                          .filter(order__warehouse__compas__officers=user) \
                          .filter(validated=False)

    return { 
            'text': link_text,
            'url': reverse('validate_dispatch', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).count(),
    }


@register.inclusion_tag('tags/form.html')
def validate_receipt(waybill, user, link_text=_("Validate receipt")):
    queryset = Waybill.objects.filter(receipt_sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                              .filter(receipt_signed_date__isnull=False) \
                              .filter(destination__compas__officers=user) \
                              .filter(receipt_validated=False)

    return { 
            'text': link_text,
            'url': reverse('validate_receipt', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).count(),
    }

@register.inclusion_tag('tags/form.html')
def waybill_delete(waybill, user, text=_("Delete"), redirect_to=''):
    return { 
            'text': text,
            'url': "%s?%s" % (reverse('waybill_delete', kwargs={'waybill_pk': waybill.pk}), urlencode({'redirect_to': redirect_to})),
            'success': (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=waybill.pk).count(),
    }



@block
def person_only(context, nodelist, user):
    return hasattr(user, 'person') and nodelist.render(context) or ''

@block
def officer_only(context, nodelist, user):
    return Compas.objects.filter(officers=user).count() and nodelist.render(context) or ''


def get_last_update():
    return StockItem.objects.aggregate(max_date=Max('updated'))['max_date']

get_last_update = function(get_last_update, cache=3600)
