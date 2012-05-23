from datetime import datetime, timedelta
from itertools import chain

from django.core import serializers
from django.db.models import Q

from ets.compress import compress_json
from ets.models import Waybill, LoadingDetail

def compress_waybills(user, start_date, end_date):
    #Append log entry 
    data = chain.from_iterable(
        [
            chain.from_iterable([
                [ waybill ], waybill.loading_details.all(),
                waybill.audit_log.filter(action_date__range=(start_date, end_date+timedelta(1))),
                LoadingDetail.audit_log.filter(waybill=waybill, action_date__range=(start_date, end_date+timedelta(1)))
            ]) \
            for waybill in Waybill.objects.filter(Q( date_modified__range=(start_date, end_date+timedelta(1)),
                                                     date_removed__isnull=True ),
                                                  Q( Q(transport_dispach_signed_date__isnull=False, order__warehouse__persons__pk=user.pk) |
                                                     Q(receipt_signed_date__isnull=False, destination__persons__pk=user.pk) )
            )
        ]
    )
    
    return compress_json( serializers.serialize('json', data, use_decimal=False) )
