### -*- coding: utf-8 -*- ####################################################
from optparse import make_option
import datetime
from itertools import chain

from django.core.management.base import BaseCommand
from django.core import serializers

from ets.compress import compress_json
from ets.models import Waybill, LoadingDetail
from ets.utils import get_date_from_string
from ets.offliner.utils import compress_waybills

class Command(BaseCommand):

    help = 'Sends created and signed waybills to central server'
    
    option_list = BaseCommand.option_list + (
        make_option('-s', '--start_date', dest='start_date', type='string', help='Start date'),
        make_option('-e', '--end_date', dest='end_date', type='string', help='End date'),
    )

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 1))        
        start_date, res = get_date_from_string(options.get('start_date', None), default=datetime.date(1900, 1, 1))
        end_date, res = get_date_from_string(options.get('end_date', None), default=datetime.datetime.now())
        data = ""
        #data = compress_waybills(start_date, end_date)
        
        return data
