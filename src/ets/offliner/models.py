import datetime, base64, zlib, urllib2

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Max

API_URL = 'http://127.0.0.1:8000/ets/api/offline/oauth/%s/'
WAREHOUSE = 'ISBX002'

class UpdateLog( models.Model ):
    date = models.DateTimeField(_("Update date"), default=datetime.datetime.now(), editable=False)
    serialized_data = models.TextField(_("Serialized data"))
    
    @classmethod
    def updata_data(cls, data):
        """Deserializes data and saves them"""
#        print data
        objects = serializers.deserialize('json', data)
        for wrapper in objects:
            wrapper.save()
        
        cls(serialized_data=data).save()
    
    @classmethod    
    def request_data(cls, start_date=None):
        #TODO: Authentication required.
        data = urllib2.urlopen(API_URL % WAREHOUSE, {
                'last_updated': start_date or cls.objects.aggregate(max_date=Max('date'))['max_date']
        }).read()
        cls.updata_data(data)
