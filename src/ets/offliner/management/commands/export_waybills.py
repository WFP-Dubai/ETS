### -*- coding: utf-8 -*- ####################################################
import urllib2
from optparse import make_option
import datetime

from django.core.management.base import BaseCommand

from ets.models import Waybill

class Command(BaseCommand):

    help = 'Sends created and signed waybills to central server'
    
    option_list = BaseCommand.option_list + (
        make_option('-start', '--start_date', dest='start_date', type='date', help='Start date'),
        make_option('-end', '--end_date', dest='end_date', type='date', help='End date'),
    )

    def handle(self, start_date, end_date, *args, **options):
        
        verbosity = int(options.get('verbosity', 1))
        
        for waybill in Waybill.objects.filter(date_modified__range=(start_date, end_date+datetime.timedelta(1)),
                                              transport_dispach_signed_date__isnull=False):
            
            pass