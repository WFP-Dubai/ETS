'''
Created on 14/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from django.db.models.signals import post_save
from django.conf import settings

from models import Waybill, WaybillSynchroState

  
    
def waybill_post_save_handler(sender, instance, **kwargs):
    '''
    This method handles the Waybill post_save process.
    '''

    # initialize the waybill synchro state
    if WaybillSynchroState.objects.filter(waybill=instance).count()==0:
        waybillSynchroState = WaybillSynchroState()
        waybillSynchroState.waybill = Waybill.objects.get(pk=instance.id)
        waybillSynchroState.save()

    if instance.dispatcherSigned and not instance.dispatcherSigned == '':
                       
        # try to call an exposed view of waybill (online) application for waybill upload
        from tools import synchronize_waybill
        response_message = synchronize_waybill(instance.pk)
        
        # update waybill synchro state
        waybillSynchroState = WaybillSynchroState.objects.get(waybill=instance)  
        waybillSynchroState.synchronized = response_message == 'SYNCHRONIZATION_DONE'
        waybillSynchroState.save()    
        
#    else:
#        pass


#print 111111111111111111, settings.SIGNALS_ENABLED

if settings.SIGNALS_ENABLED:
    post_save.connect(receiver=waybill_post_save_handler, sender=Waybill, weak=True, dispatch_uid='waybill_post_save_handler')
