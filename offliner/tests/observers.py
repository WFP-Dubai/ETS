'''
Created on 12/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from datetime import date

from django.db.models import Max

from base import AbstractTestCase
from offliner.models import WaybillSynchroState, Waybill, Waybill, Places


class WaybillObserverTestCase(AbstractTestCase):

    def test_waybill_post_save_handler_synch_not_tried(self):
        """
        Test save a waybill not dispatcherSigned: no synchronization to online app must be performed.
        """
        data = {
                'ltiNumber' : 'ltiNumber',
                'waybillNumber' : 'waybillNumber',
                'dateOfLoading' : date(2010,11,11),
                'dateOfDispatch' : date(2010,11,11),
                'transactionType' : 'WIT',
                'transportType' : '02',
                'destinationWarehouse' : Places.objects.all()[0],
        }

        max_id = int(Waybill.objects.aggregate(Max('id')).get('id__max'))

        target_item = Waybill(**data)
        target_item.save()

        stored_item = Waybill.objects.get(id=max_id+1)

        self.assertEquals(target_item, stored_item)

        waybillsynchrostate = WaybillSynchroState.objects.filter(waybill=stored_item)[0]
        self.assertTrue(waybillsynchrostate)
        self.assertFalse(False, waybillsynchrostate.synchronized)

    def test_waybill_post_save_handler_synch_tried(self):
        """
        Test save a waybill dispatcherSigned: synchronization to online app is tried, but the online app is unreachable.
        """
        data = {
                'ltiNumber' : 'ltiNumber',
                'waybillNumber' : 'waybillNumber',
                'dateOfLoading' : date(2010,11,11),
                'dateOfDispatch' : date(2010,11,11),
                'transactionType' : 'WIT',
                'transportType' : '02',
                'destinationWarehouse' : Places.objects.all()[0],
                'dispatcherSigned': True
        }

        max_id = int(Waybill.objects.aggregate(Max('id')).get('id__max'))

        target_item = Waybill(**data)
        target_item.save()

        stored_item = Waybill.objects.get(id=max_id+1)

        self.assertEquals(target_item, stored_item)

        waybillsynchrostate = WaybillSynchroState.objects.filter(waybill=stored_item)[0]
        self.assertTrue(waybillsynchrostate)
        self.assertFalse(False, waybillsynchrostate.synchronized)

    def test_waybill_post_save_handler_synch_performed(self):
        """
        Test save a waybill dispatcherSigned: synchronization to online app is performed, the online app is reachable.
        """
        # @todo: find a way to startup online app and perform Waybill post_save process.