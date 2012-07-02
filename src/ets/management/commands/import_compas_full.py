### -*- coding: utf-8 -*- ####################################################

from ets.management.commands.sync_compas import Command as UpdateCompas

class Command(UpdateCompas):
    """
    Import organizations, places, warehouses, reasons, persons from COMPAS stations
    Accepts following arguments:
        
        --compas -- COMPAS station identifier (i.e. ISBX002 for example)
        
    """
    
    help = 'Import organizations, places, warehouses, reasons, persons from COMPAS stations'

    def synchronize(self, compas):
        compas.update(base=True)
