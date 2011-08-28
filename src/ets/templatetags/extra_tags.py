import time, calendar

from django import template
from django.core.urlresolvers import reverse

from ets import settings

register = template.Library()
# Sample
@register.tag( name = "current_time" )
def do_current_time( parser, token ):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    if not ( format_string[0] == format_string[-1] and format_string[0] in ( '"', "'" ) ):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return CurrentTimeNode( format_string[1:-1] )



import datetime

class CurrentTimeNode( template.Node ):
    def __init__( self, format_string ):
        self.format_string = format_string
    def render( self, context ):
        return datetime.datetime.now().strftime( self.format_string )

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

@register.tag( name = "print_tag" )
def do_print_tag( parser, token ):
    return PrintTagNode()

class PrintTagNode( template.Node ):
    def render( self, context ):
        #TODO: remove such try...except and prints
        try:
            logfile = 'tagfile.tag'
            FILE = open( logfile )
            the_date = FILE.read()
            return '<br/><small>Latest COMPAS import from <b>' + settings.COMPAS_STATION + '</b>: ' + the_date[0:19] + '</small>'
        except Exception as e:
            print e
            return ''

#=======================================================================================================================
# @register.tag
# def waybill_edit( parser, token ):
#    try:
#        tag_name, action, waybill, user = token.split_contents()
#    except ValueError:
#        msg = '%r tag requires waybill and user as arguments' % token.contents[0]
#        raise template.TemplateSyntaxError(msg)   
#    return WaybillEditNode(action, waybill, user)
#    
# 
# class WaybillEditNode(template.Node):
#    def __init__(self, action, waybill, user):
#        self.user = user
#        self.waybill = waybill
#        self.action = action
# 
#    def render(self, context):
#        if self.user.get_profile().receipt_warehouse == self.waybill.destination:
#            return '<a href="{% url waybill_edit self.waybill.pk %}">%s</a>' % self.action
#        else:
#            return self.action
# 
# 
# @register.tag
# def waybill_reception( parser, token ):
#    try:
#        tag_name, action, waybill, user = token.split_contents()
#    except ValueError:
#        msg = '%r tag requires waybill and user as arguments' % token.contents[0]
#        raise template.TemplateSyntaxError(msg)   
#    return WaybillReceptionnNode(action, waybill, user)
#    
# 
# class WaybillReceptionnNode(template.Node):
#    def __init__(self, action, waybill, user):
#        self.user = user
#        self.waybill = waybill
#        self.action = action
# 
#    def render(self, context):
#        if self.user.get_profile().dispatch_warehouse == self.waybill.warehouse:
#            return '<a href="{% url waybill_reception waybill_pk=self.waybill.pk, order_pk=self.waybill.order_code %}">%s</a>' % self.action
#        else:
#            return self.action  
#=======================================================================================================================


@register.inclusion_tag('tags/give_link.html')
def waybill_edit(waybill, user):
    text = "Edit"
    if user.get_profile().compas_person.warehouse == waybill.warehouse:
        success = True
    else:
        success = False
    return { 
            'text': text,
            'url': reverse('waybill_edit', kwargs={'waybill_pk': waybill.pk, 'order_pk':waybill.order_code }),
            'success': success,
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_reception(waybill, user):
    text = "Recept"
    if user.get_profile().compas_person.warehouse == waybill.destination:
        success = True
    else:
        success = False
    return { 
            'text': text,
            'url': reverse('waybill_reception', kwargs={'waybill_pk': waybill.pk}),
            'success': success,
    }

@register.inclusion_tag('tags/give_link.html')
def waybill_creation(order, user):
    text = "Create"
    if user.get_profile().get_warehouses() == order.warehouse:
        success = True
    else:
        success = False
    return { 
            'text': text,
            'url': reverse('waybill_create', kwargs={'order_pk': order.pk}),
            'success': success,
    }