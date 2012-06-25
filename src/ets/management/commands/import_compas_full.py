### -*- coding: utf-8 -*- ####################################################

from ets.management.commands.sync_compas import Command as UpdateCompas

class Command(UpdateCompas):
    
    help = 'Import organizations, places, warehouses, reasons, persons from COMPAS stations'

    def synchronize(self, compas):
        from ets import utils
        compas.update(utils.import_partners, utils.import_places, utils.import_reasons, utils.import_persons)
