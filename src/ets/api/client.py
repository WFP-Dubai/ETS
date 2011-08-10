import urllib2

from django.core import serializers
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils import simplejson

from ..models import Waybill, sync_data

DEFAULT_TIMEOUT = 10
API_DOMAIN = "http://localhost:8000"
COMPAS_STATION = getattr(settings, 'COMPAS_STATION', None)

def send_new():
    """Sents new waybills to central server"""
    url = "%s%s" % (API_DOMAIN, reverse("api_new_waybill"))
    
    waybills = Waybill.objects.filter(status=Waybill.SIGNED, warehouse__pk=COMPAS_STATION)
    
    data = serializers.serialize( 'json', sync_data(waybills), indent=True)
    if data:
        try:
            response = urllib2.urlopen(urllib2.Request(url, data, {
                'Content-Type': 'application/json'
            }), timeout=DEFAULT_TIMEOUT)
        except (urllib2.HTTPError, urllib2.URLError) as err:
            print err
        else:
            if response.read() == 'Created':
                waybills.update(status=Waybill.SENT)

def get_informed():
    """Dispatcher reads the server for new informed waybills"""
    for waybill in Waybill.objects.filter(status=Waybill.SENT, warehouse__pk=COMPAS_STATION):
        url = "%s%s" % (API_DOMAIN, reverse("api_informed_waybill", kwargs={"slug": waybill.slug}))
        try:
            response = urllib2.urlopen(url, timeout=DEFAULT_TIMEOUT)
        except (urllib2.HTTPError, urllib2.URLError) as err:
            print err
        else:
            if response.code == 200:
                waybill.update_status(Waybill.INFORMED)

def get_delivered():
    """Dispatcher reads the server for delivered waybills"""
    for waybill in Waybill.objects.filter(status=Waybill.INFORMED, warehouse__pk=COMPAS_STATION):
        url = "%s%s" % (API_DOMAIN, reverse("api_delivered_waybill", kwargs={"slug": waybill.slug}))
        try:
            response = urllib2.urlopen(url, timeout=DEFAULT_TIMEOUT)
        except (urllib2.HTTPError, urllib2.URLError) as err:
            print err
        else:
            if response.code == 200:
                for obj in serializers.deserialize('json', response.read()):
                    obj.save()
            
def get_receiving():
    """
    Receiver reads the server for new waybills, that we are expecting to receive 
    and update status of such waybills to 'informed'.
    """ 
    url = "%s%s" % (API_DOMAIN, reverse("api_receiving_waybill", kwargs={'destination': COMPAS_STATION}))
    try:
        response = urllib2.urlopen(url, timeout=DEFAULT_TIMEOUT)
    except (urllib2.HTTPError, urllib2.URLError) as err:
        print err
    else:
        if response.code == 200:
            for obj in serializers.deserialize('json', response.read()):
                obj.save()
            
def send_informed():
    """Receiver updates status of receiving waybill to 'informed'"""
    
    waybills = Waybill.objects.filter(status=Waybill.SENT, destination__pk=COMPAS_STATION)
    url = "%s%s" % (API_DOMAIN, reverse("api_informed_waybill"))
    
    request = urllib2.Request(url, simplejson.dumps(tuple(waybills.values_list('pk', flat=True))), {
        'Content-Type': 'application/json'
    })
    request.get_method = lambda: 'PUT'
    try:
        response = urllib2.urlopen(request, timeout=DEFAULT_TIMEOUT)
    except (urllib2.HTTPError, urllib2.URLError) as err:
        print err
    else:
        if response.code == 200:
            waybills.update(status=Waybill.INFORMED)

def send_delivered():
    """Receiver sends 'delivered' waybills to the central server"""
    waybills = Waybill.objects.filter(status=Waybill.DELIVERED, destination__pk=COMPAS_STATION)
    url = "%s%s" % (API_DOMAIN, reverse("api_delivered_waybill"))
    data = serializers.serialize( 'json', waybills, indent=True)
    
    request = urllib2.Request(url, data, {
        'Content-Type': 'application/json'
    })
    request.get_method = lambda: 'PUT'
    
    try:
        response = urllib2.urlopen(request, timeout=DEFAULT_TIMEOUT)
    except (urllib2.HTTPError, urllib2.URLError) as err:
        print err
    else:
        if response.code == 200:
            waybills.update(status=Waybill.COMPLETE)