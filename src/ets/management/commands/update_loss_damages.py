### -*- coding: utf-8 -*- ####################################################

from ets.models import LossDamageType
from .sync_compas import Command as UpdateCompas

class Command(UpdateCompas):

    help = 'Import data from COMPAS stations with loss/damage data'

    def synchronize(self, compas):
        LossDamageType.update(compas)

        
