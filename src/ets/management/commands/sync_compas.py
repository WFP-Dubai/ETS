### -*- coding: utf-8 -*- ####################################################

from optparse import make_option
import lockfile
import os
import logging
import time
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db.utils import DatabaseError
from django.conf import settings

from ets.utils import update_compas
from ets.models import Compas

LOG_DIRECTORY = settings.LOG_DIRECTORY
MINIMUM_AGE = 30


class Command(BaseCommand):

    option_list = BaseCommand.option_list + ( 
        make_option('--compas', dest='compas', default='',
            help='Tells the system to synchronize only this one compas station'),
    )

    help = 'Import data from COMPAS stations'
    lock_file_name = 'sync_compas'
    log_name = 'sync_compas.log'
    
    def synchronize(self, compas):
        
        update_compas(compas)

    def get_log_name(self):
        return os.path.join(LOG_DIRECTORY, self.log_name)
    
    def get_lock_name(self, compas):
        return os.path.join(settings.EGG_ROOT, "%s%s" % (self.lock_file_name, compas))
    
    def handle(self, compas='', *args, **options):
        
        lock = lockfile.FileLock(self.get_lock_name(compas))

        try:
            lock.acquire(timeout=10)  # wait up to 30 seconds
        except lockfile.LockTimeout:
            
            lock_time = datetime.fromtimestamp(os.path.getctime(lock.lock_file))
            if lock_time + datetime.timedelta(minutes=MINIMUM_AGE) <= datetime.datetime.now():
                lock.break_lock()
                lock.acquire()
            
            raise
        
        try:
            stations = Compas.objects.all()
            if compas:
                stations = stations.filter(pk=compas)
                
            for compas in stations:
                self.synchronize(compas=compas.pk)
        
        finally:
            lock.release()
