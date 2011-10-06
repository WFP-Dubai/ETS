### -*- coding: utf-8 -*- ####################################################

from ets.utils import update_loss_damages
from .sync_compas import Command as UpdateCompas

class Command(UpdateCompas):

    help = 'Import data from COMPAS stations with loss/damage data'

    def synchronize(self, compas):
        update_loss_damages(compas)
        
