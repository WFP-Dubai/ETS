### -*- coding: utf-8 -*- ####################################################

from ets.management.commands.sync_compas import Command as UpdateCompas

class Command(UpdateCompas):
    
    help = 'Import organizations, places, warehouses, reasons, persons from COMPAS stations'

    def synchronize(self, compas):
        compas.update(base=True)
