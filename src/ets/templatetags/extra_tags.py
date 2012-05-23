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
    waybillPk =0
    try:
        waybillPk = waybill['pk']
    except :
        waybillPk = waybill.pk
    return { 
            'text': text,
            'url': reverse('waybill_reception', kwargs={'waybill_pk': waybillPk}),
            'success': (not hasattr(user, 'person') or user.person.receive) and Waybill.receptions(user).filter(pk=waybillPk).count(),
    }


@register.inclusion_tag('tags/give_link.html')
def waybill_creation(order, user, text=_("Create")):
    return { 
            'text': text,
            'url': reverse('waybill_create', kwargs={'order_pk': order.pk}),
            'success': (not hasattr(user, 'person') or user.person.dispatch) and order.warehouse.persons.filter(pk=user.pk).count(),
    }


@function
def sign_dispatch(waybill, user):
    return (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=waybill.pk).count()

@function
def sign_reception(waybill, user):
    return (not hasattr(user, 'person') or user.person.receive) \
            and waybill.is_received() \
            and Waybill.receptions(user).filter(pk=waybill.pk).count()


@register.inclusion_tag('tags/form.html')
def validate_dispatch(waybill, user, link_text=_("Validate dispatch")):
    queryset = Waybill.objects.filter(sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                          .filter(order__warehouse__compas__officers=user) \
                          .filter(validated=False)

    return { 
            'text': link_text,
            'url': reverse('validate_dispatch', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).count(),
            'dialog_question': _("Are you sure you want to validate this waybill?"),
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
        'dialog_question': _("Are you sure you want to validate this waybill?"),
    }

@register.inclusion_tag('tags/form.html')
def waybill_delete(waybill, user, text=_("Delete"), redirect_to=''):
    waybillPk =0
    try:
        waybillPk = waybill['pk']
    except :
        waybillPk = waybill.pk
    return { 
        'text': text,
        'url': "%s?%s" % (reverse('waybill_delete', kwargs={'waybill_pk': waybillPk}), urlencode({'redirect_to': redirect_to})),
        'success': (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=waybillPk).count(),
        'dialog_question': _("Are you sure you want to delete this waybill?"),
    }

@register.simple_tag
def waybill_delivery_method(transaction_type):
    for o in Waybill.TRANSACTION_TYPES:
        if o[0]==transaction_type:
            return o[1].title()

    return transaction_type


@register.simple_tag
def waybill_url(waybill):
    wb = Waybill.objects.get(pk=waybill)

    return wb.get_absolute_url()

@register.simple_tag
def order_url(order):
    order = Order.objects.get(pk=order)

    return order.get_absolute_url()


@block
def person_only(context, nodelist, user):
    return hasattr(user, 'person') and nodelist.render(context) or ''

@block
def officer_only(context, nodelist, user):
    return Compas.objects.filter(officers=user).count() and nodelist.render(context) or ''

@register.inclusion_tag('sync/sync_form.html')
def sync_compas_form(compas, user):
    return { 
        'access_granted': user.is_superuser or Compas.objects.filter(pk=compas.pk, officers__pk=user.pk).exists(),
        'station': compas,
    }

@register.inclusion_tag('last_updated.html')
def get_last_update(user):
    """dummy function, just a wrapper"""
    
    failed = False
    for c in Compas.objects.all():
        try:
            last_attempt = c.import_logs.order_by('-when_attempted')[0]
            if last_attempt.status == ImportLogger.FAILURE:
                failed = True
        except (ImportLogger.DoesNotExist, IndexError):
            pass
         
    return {
        'last_updated': StockItem.get_last_update(),
        'failed': failed,
    }

@register.simple_tag
def named_object(slug, object_name, title=""):
    if object_name == "Waybill":
        waybill = Waybill.objects.get(slug=slug)
        title = "Waybill: %s" % slug
    elif object_name == "LoadingDetail":
        item = LoadingDetail.audit_log.filter(slug=slug)[0]
        waybill = item.waybill
        title = "Waybill: %s, Commodity: %s" % (waybill, item.stock_item)
    else:
        return
    return "<th><a href='%s'>%s</a></th>" % (reverse("admin:ets_waybill_change", args=[waybill.pk]), title)
