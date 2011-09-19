import datetime

from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from native_tags.decorators import function, block

#from ets import settings
from ets.models import Warehouse, Waybill, Person, Compas, LoadingDetail
from ets.utils import changed_fields

register = template.Library()


@register.filter
def truncatesmart( value, limit = 80 ):
    """
    Truncates a string after a given number of chars keeping whole words.
    
    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """

    try:
        limit = int( limit )
    # invalid literal for int()
    except ValueError:
        # Fail silently.
        return value

    # Make sure it's unicode
    value = unicode( value )

    # Return the string itself if length is smaller or equal to the limit
    if len( value ) <= limit:
        return value

    # Cut the string
    value = value[:limit]

    # Break into words and remove the last
    words = value.split( ' ' )[:-1]

    # Join the words and return
    return ' '.join( words ) + '...'


@register.inclusion_tag('tags/give_link.html')
def waybill_edit(waybill, user, text=_("Edit")):
    return { 
            'text': text,
            'url': reverse('waybill_edit', kwargs={'waybill_pk': waybill.pk, 'order_pk':waybill.order.pk }),
            'success': Waybill.dispatches(user).filter(pk=waybill.pk).count(),
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_reception(waybill, user, text=_("Receive")):
    return { 
            'text': text,
            'url': reverse('waybill_reception', kwargs={'waybill_pk': waybill.pk}),
            'success': Waybill.receptions(user).filter(pk=waybill.pk).count(),
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_creation(order, user, text=_("Create")):
    return { 
            'text': text,
            'url': reverse('waybill_create', kwargs={'order_pk': order.pk}),
            'success': Warehouse.filter_by_user(user).filter(pk=order.warehouse.pk).count(),
    }
    
@register.inclusion_tag('tags/give_link.html')
def waybill_delete(waybill, user, text=_("Delete")):
    return { 
            'text': text,
            'url': reverse('waybill_delete', kwargs={'waybill_pk': waybill.pk,}),
            'success': Waybill.dispatches(user).filter(pk=waybill.pk).count(),
    }


@function
def sign_dispatch(waybill, user):
    return Waybill.dispatches(user).filter(pk=waybill.pk).count()

@function
def sign_reception(waybill, user):
    return Waybill.receptions(user).filter(pk=waybill.pk).count()


@register.inclusion_tag('tags/give_link.html')
def validate_dispatch(waybill, user, link_text=_("Validate dispatch"), forbidden_text=""):
    queryset = Waybill.objects.filter(sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                          .filter(order__warehouse__compas__officers=user) \
                          .filter(validated=False)

    return { 
            'text': link_text,
            'forbidden_text': forbidden_text,
            'url': reverse('validate_dispatch', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).count(),
    }


@register.inclusion_tag('tags/give_link.html')
def validate_receipt(waybill, user, link_text=_("Validate receipt"), forbidden_text=""):
    queryset = Waybill.objects.filter(receipt__sent_compas__isnull=True, transport_dispach_signed_date__isnull=False) \
                              .filter(receipt__signed_date__isnull=False) \
                              .filter(destination__compas__officers=user) \
                              .filter(receipt__validated=False)

    return { 
            'text': link_text,
            'forbidden_text': forbidden_text,
            'url': reverse('validate_receipt', kwargs={'waybill_pk': waybill.pk,}),
            'success': queryset.filter(pk=waybill.pk).count(),
    }

@block
def person_only(context, nodelist, user):
    return Person.objects.filter(user=user).count() and nodelist.render(context) or ''

@block
def officer_only(context, nodelist, user):
    return Compas.objects.filter(officers=user).count() and nodelist.render(context) or ''

@register.inclusion_tag('tags/history_waybill.html')
def history_waybill(entry, waybill_changes="", loading_details=""):
    if entry.action_type == "U":
        previous = Waybill.audit_log.filter(slug=entry.slug, action_id__lt=entry.action_id).order_by('-action_id')[0]
        waybill_changes = changed_fields(Waybill, entry, previous) #waybill__pk=entry.slug, 
        max_datetime = entry.action_date + datetime.timedelta(seconds=10)
        loading_details = LoadingDetail.audit_log.filter(waybill__pk=entry.slug, action_user=entry.action_user\
                        , action_date__gte=entry.action_date, action_date__lte=max_datetime )
    print entry.action_date       
    return {
            'item': entry,
            'changes': waybill_changes,
            'loading_details': loading_details,
    }
        
@register.inclusion_tag('tags/changed_fields.html')
def history_loading_details(entry, loading_details_changes=""):
    print "OK"
    print entry.action_date
    if entry.action_type == "U":
        previous = LoadingDetail.audit_log.filter(waybill__pk=entry.waybill_id, slug=entry.slug, action_id__lt=entry.action_id).order_by('-action_id')[0]
        loading_details_changes = changed_fields(LoadingDetail, entry, previous)        
    return {
            'item': entry,
            'changes': loading_details_changes,
    }