### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand
from django.db import transaction

from ets.utils import sync_received_waybills


class Command(BaseCommand):

    help = 'Receive all changes from parent server with parent ETS server.'

    @transaction.commit_on_success
    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))
        if verbosity >= 2:
            print("Start receiving waybills from parent ETS ...")
        
        #Receive all data from parent
        sync_received_waybills()