### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):

    help = 'Synchronizes with parent ETS server.'

    @transaction.commit_on_success
    def handle(self, *args, **options):

        verbosity = int(options.get('verbosity', 1))
        if verbosity >= 2:
            print("Start synchronizing with parent ETS ...")
        
        #Dispatch all data to parent
        #Serialize data and send them to parent ETS
        dispath_sync_data()
        #Receive all data from parent
        receive_sync_data()