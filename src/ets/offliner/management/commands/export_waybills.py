### -*- coding: utf-8 -*- ####################################################
from optparse import make_option
import datetime
from itertools import chain

from django.core.management.base import BaseCommand
from django.core import serializers

from ets.compress import compress_json
from ets.models import Waybill, LoadingDetail
from ets.utils import get_date_from_string

class Command(BaseCommand):

    help = 'Sends created and signed waybills to central server'
    
    option_list = BaseCommand.option_list + (
        make_option('-s', '--start_date', dest='start_date', type='string', help='Start date'),
        make_option('-e', '--end_date', dest='end_date', type='string', help='End date'),
        make_option('-c', '--compress', dest='compress', action="store_true", help='Tells the system to compress output json'),
    )

    def handle(self, *args, **options):
        compress = options.get('compress', False)
        verbosity = int(options.get('verbosity', 1))        
        start_date, res = get_date_from_string(options.get('start_date', None), default=datetime.date(1900, 1, 1))
        end_date, res = get_date_from_string(options.get('end_date', None), default=datetime.datetime.now())
        
        data = chain(
            Waybill.objects.filter(date_modified__range=(start_date, end_date+datetime.timedelta(1)),
                                   transport_dispach_signed_date__isnull=False),
            LoadingDetail.objects.filter(waybill__date_modified__range=(start_date, end_date+datetime.timedelta(1)),
                                         waybill__transport_dispach_signed_date__isnull=False),
            Waybill.audit_log.filter(action_date__range=(start_date, end_date+datetime.timedelta(1))),
            LoadingDetail.audit_log.filter(action_date__range=(start_date, end_date+datetime.timedelta(1)))
        )
        data = serializers.serialize('json', data, use_decimal=False)

        if compress:
            data = compress_json(data)
        
        return data
