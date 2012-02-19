from datetime import datetime
from itertools import chain

from django.core import serializers

from ets.compress import compress_json
from ets.models import Waybill, LoadingDetail

def compress_waybills(start_date, end_date):
    #Append log entry 
    data = chain(
        Waybill.objects.filter(date_modified__range=(start_date, end_date+datetime.timedelta(1))),
        LoadingDetail.objects.filter(waybill__date_modified__range=(start_date, end_date+datetime.timedelta(1)),
                                                waybill__date_removed__isnull=True)
    )
    
    return compress_json( serializers.serialize('json', data, use_decimal=False) )
