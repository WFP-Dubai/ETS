from datetime import timedelta
from itertools import chain

from django.core import serializers
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry

from ets.compress import compress_json
from ets.models import Waybill


def compress_waybills(queryset, start_date, end_date):
    #Append log entry

    data = (
        chain(waybill, waybill.loading_details.all(),
            LogEntry.objects.filter(content_type__id=ContentType.objects.get_for_model(Waybill).pk,
                                    object_id = waybill.pk,
                                    action_time__range=(start_date, end_date+timedelta(1))))
        for waybill in queryset.filter(Q( date_modified__range=(start_date, end_date+timedelta(1)),
                                          date_removed__isnull=True ),
                                       Q( Q(transport_dispach_signed_date__isnull=False) |
                                          Q(receipt_signed_date__isnull=False) )
        )
    )
    
    return compress_json( serializers.serialize('json', data, use_decimal=False) )
