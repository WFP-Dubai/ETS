
from django import template
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from native_tags.decorators import function

#from ets import settings
from ets.models import Warehouse, Waybill

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
    