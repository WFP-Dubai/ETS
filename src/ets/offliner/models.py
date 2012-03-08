import datetime, base64, zlib, urllib2

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Max

from ets.models import Waybill
from ets.compress import decompress_json

API_URL = 'http://10.11.208.242/api/offline/%s/'
WAREHOUSE = 'ISBX002'

class UpdateLog( models.Model ):
    
    date = models.DateTimeField(_("Update date"), default=datetime.datetime.now(), editable=False)
    serialized_data = models.TextField(_("Serialized data"))
    
    class Meta:
        ordering = ('date',)
        verbose_name = _('Offline import logger')
        verbose_name_plural = _("Loggers")
    
    @classmethod
    def updata_data(cls, data):
        """Deserializes data and saves them"""
        
        #Decompress field names
        data = decompress_json(data)
        #Deserialize them
        objects = serializers.deserialize('json', data)
        #And save
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

    
class WaybillSync(models.Model):
    
    waybill = models.OneToOneField(Waybill, verbose_name=_("Waybill"), related_name="offline_sync")
    date = models.DateTimeField(_("date/time"), default=datetime.datetime.now)
