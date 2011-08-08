### -*- coding: utf-8 -*- ####################################################

from django.core.management.base import BaseCommand

import ets.models

class Command(BaseCommand):

    help = 'Synchronizes data with compas database'

    #@transaction.commit_on_success
    def handle(self, *args, **options):

        #verbosity = int(options.get('verbosity', 1))
        
        #Update places
        ets.models.Place.update()
        
        #Update persons
        ets.models.CompasPerson.update()
        
        #Update loss/damage types
        ets.models.LossDamageType.update()

        #Update stocks
        ets.models.EpicStock.update()

        #Update orders
        ets.models.LtiOriginal.update()
        
        
        