'''
Created on 10/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-
from django.db.models.sql.datastructures import Date
from offliner.tests.base import AbstractTestCase

from offliner.forms import WaybillForm, WaybillRecieptForm, MyModelChoiceField, MyModelChoiceField
from offliner.models import Waybill, Places, LtiOriginal


class WaybillFormTestCase(AbstractTestCase):

    def test_form_validation_bestcase(self):
        """
        test di validazione form con dati coerenti
        """
        destinationWarehouse = Places.objects.all()[0]
        #transport_type = Waybill.transport_type[0]
        #transaction_type = Waybill.transaction_type_choice[0]

        req  = Waybill()
        data = {
                'ltiNumber': 'ltiNumber',
                'waybillNumber': '1',
                'dateOfLoading': '2010-01-01',
                'dateOfDispatch': '2010-01-02',
                'transactionType': 'WIT',#transaction_type,
                'transportType': '02',#transport_type,
                'transportContractor': 'transportContractor',
                'dispatchRemarks': 'dispatchRemarks',
                'dispatcherName': 'dispatcherName',
                'dispatcherTitle': 'dispatcherTitle',
                'destinationWarehouse': destinationWarehouse.pk,
                'recipientLocation': 'recipientLocation',
                'recipientConsingee': 'recipientConsingee',
                }
        form = WaybillForm(data,instance=req)

        self.assertTrue(form.is_valid())

    def test_form_validation_worstcase_1(self):
        """
        test di validazione form con dati incoerenti: not all required fields are provided.
        """
        destinationWarehouse = Places.objects.all()[0]

        req  = Waybill()
        data = {
                'ltiNumber': 'ltiNumber',
                'waybillNumber': '1',
                'dateOfLoading': '2010-01-01',
                'dateOfDispatch': '2010-01-02',
                'transactionType': 'WIT',#transaction_type,
                'transportType': '02',#transport_type,
                'transportContractor': 'transportContractor',
                'dispatchRemarks': 'dispatchRemarks',
                'dispatcherName': 'dispatcherName',
                'dispatcherTitle': 'dispatcherTitle',
                'destinationWarehouse': destinationWarehouse.pk,
                }
        form = WaybillForm(data,instance=req)
        
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
        self.assertTrue(form.errors['recipientLocation'].as_text().__contains__(u'This field is required'))
        self.assertTrue(form.errors['recipientConsingee'].as_text().__contains__(u'This field is required'))

    def test_form_validation_worstcase_2(self):
        """
        test di validazione form con dati incoerenti: dateOfLoading > dateOfDispatch.
        """
        destinationWarehouse = Places.objects.all()[0]

        req  = Waybill()
        data = {
                'ltiNumber': 'ltiNumber',
                'waybillNumber': '1',
                'dateOfLoading': '2010-01-01',
                'dateOfDispatch': '2000-01-02',
                'transactionType': 'WIT',
                'transportType': '02',
                'transportContractor': 'transportContractor',
                'dispatchRemarks': 'dispatchRemarks',
                'dispatcherName': 'dispatcherName',
                'dispatcherTitle': 'dispatcherTitle',
                'destinationWarehouse': destinationWarehouse.pk,
                'recipientLocation': 'recipientLocation',
                'recipientConsingee': 'recipientConsingee',
                }
        form = WaybillForm(data,instance=req)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
        self.assertTrue(form.errors.as_text().__contains__(u'Cargo Dispatched before being Loaded'))


class WaybillRecieptFormTestCase(AbstractTestCase):

    def test_form_validation_bestcase(self):
        """
        test di validazione form con dati coerenti
        """

        req  = Waybill.objects.get(id='1')
        data = {
                'waybillNumber': '1',
                'recipientArrivalDate': '2011-01-03',
                'recipientStartDischargeDate': '2011-01-04',
                'recipientEndDischargeDate': '2011-01-05',
                'recipientDistance': '',
                'recipientRemarks': '',
                'recipientSigned': '',
                'recipientSignedTimestamp': '',
                'recipientLocation': 'recipientLocation',
                'recipientConsingee': 'recipientConsingee',
                'transportDeliverySigned': '',
                }
        form = WaybillRecieptForm(data,instance=req)

        self.assertTrue(form.is_valid())

    def test_form_validation_worstcase_1(self):
        """
        test di validazione form con dati incoerenti: not all required fields are provided.
        """

        req  = Waybill.objects.get(id='1')
        data = {
                'waybillNumber': '1',
                'recipientArrivalDate': '2011-01-03',
                'recipientStartDischargeDate': '2011-01-04',
                'recipientEndDischargeDate': '2011-01-05',
                'recipientDistance': '',
                'recipientRemarks': '',
                'recipientSigned': '',
                'recipientSignedTimestamp': '',
                'transportDeliverySigned': '',
                }
        form = WaybillRecieptForm(data,instance=req)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
        self.assertTrue(form.errors['recipientLocation'].as_text().__contains__(u'This field is required'))
        self.assertTrue(form.errors['recipientConsingee'].as_text().__contains__(u'This field is required'))

    def test_form_validation_worstcase_2(self):
        """
        test di validazione form con dati incoerenti: arrival_date < dispatch_date.
        """

        req  = Waybill.objects.get(id='1')
        data = {
                'waybillNumber': '1',
                'recipientArrivalDate': '2010-01-03',
                'recipientStartDischargeDate': '2010-01-04',
                'recipientEndDischargeDate': '2010-01-05',
                'recipientDistance': '',
                'recipientRemarks': '',
                'recipientSigned': '',
                'recipientSignedTimestamp': '',
                'transportDeliverySigned': '',
                'recipientLocation': 'recipientLocation',
                'recipientConsingee': 'recipientConsingee',
                }
        form = WaybillRecieptForm(data,instance=req)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
        self.assertTrue(form.errors.as_text().__contains__(u'Cargo arrived before being dispatched'))

    def test_form_validation_worstcase_3(self):
        """
        test di validazione form con dati incoerenti: arrival_date < dispatch_date and discharge_start < arrival_date and discharge_end < discharge_start.
        """

        req  = Waybill.objects.get(id='1')
        data = {
                'waybillNumber': '1',
                'recipientArrivalDate': '2000-01-03',
                'recipientStartDischargeDate': '2000-01-02',
                'recipientEndDischargeDate': '2000-01-01',
                'recipientDistance': '',
                'recipientRemarks': '',
                'recipientSigned': '',
                'recipientSignedTimestamp': '',
                'transportDeliverySigned': '',
                'recipientLocation': 'recipientLocation',
                'recipientConsingee': 'recipientConsingee',
                }
        form = WaybillRecieptForm(data,instance=req)

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),4)

        self.assertTrue(form.errors.as_text().__contains__(u'Cargo arrived before being dispatched'))
        self.assertTrue(form.errors.as_text().__contains__(u'Cargo Discharge started before Arrival'))
        self.assertTrue(form.errors.as_text().__contains__(u'Cargo finished Discharge before Starting'))



class MyModelChoiceFieldTestCase(AbstractTestCase):

     def test_label_from_instance(self):
         queryset = LtiOriginal.objects.all()

         my_model_choice_field = MyModelChoiceField(queryset)

         obj = LtiOriginal.objects.get(lti_pk='JERX001000000000000011031HQX0001000000000000990922')

         self.assertEquals('00004178 - WHEAT FLOUR', my_model_choice_field.label_from_instance(obj))