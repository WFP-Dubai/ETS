### -*- coding: utf-8 -*- ####################################################
from optparse import make_option
import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from ets.utils import get_date_from_string
from ets.decorators import waybill_user_related_filter
from ets.models import Waybill
from offliner.utils import compress_waybills


class Command(BaseCommand):

    help = 'Sends created and signed waybills to central server'
    
    option_list = BaseCommand.option_list + (
        make_option('-s', '--start_date', dest='start_date', type='string', help='Start date'),
        make_option('-e', '--end_date', dest='end_date', type='string', help='End date'),
        make_option('-u', '--user', dest='user', type='string', help='Username'),
        make_option('-P', '--passwd', dest='passwd', type='string', help='Password'),
    )

    def handle(self, *args, **options):
        start_date, res = get_date_from_string(options.get('start_date', None), default=datetime.date(1900, 1, 1))
        end_date, res = get_date_from_string(options.get('end_date', None), default=datetime.datetime.now())
        username = options.get('user', '')
        passwd = options.get('passwd', '')
        data = ""
        try:
            user = authenticate(username=username, password=passwd)
            queryset = waybill_user_related_filter(Waybill.objects.all(), user)
            data = compress_waybills(queryset, start_date, end_date)
        except User.DoesNotExist:
            print "Wrong password or username '%s'" % username
        return data
