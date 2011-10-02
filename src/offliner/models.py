import datetime, base64, zlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import serializers


#=======================================================================================================================
# Offliner
#=======================================================================================================================

class UpdateLog( models.Model ):
    last_update = models.DateTimeField(_("Update date"), default=datetime.datetime.now(), editable=False)

    @classmethod    
    def request_data(cls, start_date):
        data_serialized = serializers.serialize( 'json', Waybill.objects.all(), LoadingDetail.objects.all())
        return base64.b64encode( zlib.compress(data_serialized) )
    
    @classmethod    
    def import_data(cls, data):
        try:
            data_serialized = zlib.decompress( base64.b64decode(data) )
        except TypeError:
            pass
