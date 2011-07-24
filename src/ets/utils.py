import datetime
import zlib, base64, string
import urllib2

from django.conf import settings
from django.contrib.auth.models import User
from django.core import serializers
from django.core.urlresolvers import reverse
#from django.db import connections
#from django.forms.models import model_to_dict
#from django.utils import simplejson

import models

API_URL=getattr(settings, 'SYNC_URL', None)

"%s%s" % (getattr(settings, 'SYNC_DOMAIN', ''), reverse("api_waybill"))

def receive_waybills(station=settings.COMPAS_STATION, API_URL=getattr(settings, 'SYNC_URL', None), 
                     timeout=getattr(settings, 'SYNC_TIMEOUT', 10)):
    headers = {
        "Accept": "application/json;q=0.9,text/plain;q=0.8,*/*;q=0.5", #image/png,
        "Accept-Language": "en;q=0.5",
        "Accept-Charset": "utf-8;q=0.7,*;q=0.7",
        "Connection": "close",
    }
    response = urllib2.urlopen(urllib2.Request(DATA_URL, None, headers), timeout=DEFAULT_TIMEOUT)

def sync_received_waybills():
    data = receive_waybills()
    
def sync_dispatched_waybills():
    pass
