### -*- coding: utf-8 -*- ####################################################

import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError 
from django.contrib.auth.forms import AuthenticationForm
from django.db import models

import ets.models
from ets.tests.utils import TestCaseMixin


class WaybillTestCase(TestCaseMixin, TestCase):
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        super(WaybillTestCase, self).setUp()
        
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.dispatcher = User.objects.get(username="dispatcher")
        self.receipient = User.objects.get(username="recepient")
        self.waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.reception_waybill = ets.models.Waybill.objects.get(pk="ISBX00311A")
        self.delivered_waybill = ets.models.Waybill.objects.get(pk="ISBX00312A")
        self.order = ets.models.Order.objects.get(pk='OURLITORDER')
        self.warehouse = ets.models.Warehouse.objects.get(pk="ISBX002")
        #self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
     
    
    def test_serialize(self):
        """Checks methods serialize of waybill instance"""
        data = self.waybill.serialize()
        self.assertTrue(data.startswith('[{"pk": "ISBX00211A", "model": "ets.waybill", "fields": {'))
    
    def test_compress(self):
        """Checks methods compress of waybill instance"""
        data = self.waybill.compress()
        self.assertTrue(isinstance(data, str))
    
    def test_login_form(self):
        self.client.logout()
        #Check login
        response = self.client.get(reverse('index'))
        self.assertContains(response, "The system requires you to be authenticated.")
        
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], AuthenticationForm))
    
    def test_index(self):
        """ tests index direct_to_template page """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_view(self):
        """ets.views.waybill_view test"""
        response = self.client.get(reverse('waybill_view', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_listing(self):
        """ receive/ and dispatch/ pages"""
        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.get(reverse('waybill_dispatch_list'))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['object_list'].count(), 1)

        #Dispatcher can not see reception list
        response = self.client.get(reverse('waybill_reception_list'))
        self.assertEqual(response.status_code, 302)

        self.client.login(username='recepient', password='recepient')
        response = self.client.get(reverse('waybill_reception_list'))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['object_list'].count(), 0)
    
    def test_waybill_search(self):
        """ets.views.waybill_search test"""
        #from ets.forms import WaybillSearchForm
        # Empty search query
        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.post(reverse('waybill_search'))
        self.assertEqual(response.status_code, 200)
        
        #: TODO: Test datatable view here
        #=======================================================================
        # self.assertListEqual([obj['pk'] for obj in response.context['object_list']], 
        #                      [self.waybill.pk, self.reception_waybill.pk, self.delivered_waybill.pk])
        #=======================================================================
        
        #=======================================================================
        # form = WaybillSearchForm({ 'q' : 'ISBX00211A'})
        # response = self.client.post(reverse('waybill_search'), data={'form': form, 'q': 'ISBX00211A'})
        #=======================================================================
        # Search query with existing waybill code  
        response = self.client.get(reverse('waybill_search'), data={'q': 'ISBX00211A'})
        self.assertEqual(response.status_code, 200)
        
        #TODO: insert test of datatables here
        #self.assertListEqual([obj['pk'] for obj in response.context['object_list']], [self.waybill.pk,])
        # Search query with not existing waybill code 
        response = self.client.get(reverse('waybill_search'), data={'q': 'ISBX00211A1'})
        self.assertEqual(response.status_code, 200)
        #TODO: insert test of datatables here
        #self.assertEqual(len(response.context['object_list']), 0)
        
         
    def test_create_waybill(self):
        """ets.views.waybill_create test"""
        from ets.forms import DispatchWaybillForm
        
        self.client.login(username='dispatcher', password='dispatcher')        
        response = self.client.get(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
        
        #Check form
        form = response.context['form']
        self.assertTrue(isinstance(form, DispatchWaybillForm))
        #Check that destination has only one possible choice
        self.assertEqual(tuple(form.fields['destination'].queryset.all()), 
                         (ets.models.Warehouse.objects.get(pk="ISBX003"),))
        
        data = {
            'loading_date': self.order.dispatch_date,
            'dispatch_date': self.order.dispatch_date,
            'transaction_type': u'WIT',
            'transport_type': u'02',
            'dispatch_remarks': 'You are funny guys!',
            'transport_sub_contractor': 'Arpaso',
            'transport_driver_name': 'Ahmed',
            'transport_driver_licence': 'KE23455',
            'transport_vehicle_registration': 'BG2345',
            
            'item-0-stock_item': 'KARX025KARX0010000944801MIXMIXHEBCG15586',
            'item-0-number_of_units': 12,
            'item-0-unit_weight_net': 1,
            'item-0-unit_weight_gross': 1.02,
            'item-0-total_weight_net': 12,
            'item-0-total_weight_gross': 12.24,
            
            'item-TOTAL_FORMS': 1,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 5,
        }
        
        response = self.client.post(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}), data=data)
        self.assertContains(response, u'Chose Destination Warehouse or another Transaction Type')
        self.assertContains(response, u'Overloaded for 10.250 tons')

        data.update({
            'item-0-overloaded_units': True,
            'transaction_type': u'DEL',
        })
        
        response = self.client.post(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}), data=data)
        self.assertEqual(response.status_code, 302)
        
        #check created waybill and loading details
        waybill = ets.models.Waybill.objects.get(pk=u'ISBX00212A000004')
        self.assertEqual(waybill.loading_details.count(), 1)

    
    def test_waybill_edit(self):
        """ets.views.waybill_edit"""
        self.client.login(username='dispatcher', password='dispatcher')
        
        edit_url = reverse('waybill_edit', kwargs={
            'order_pk': self.order.pk, 
            'waybill_pk': self.waybill.pk,
        })
        response = self.client.get(edit_url)
        self.assertContains(response, "Edit waybill: ISBX00211A", status_code=200)
        
        today = datetime.date.today()
        
        data={
            'loading_date': today,
            'dispatch_date': today,
            'destination': 'ISBX0034',
            'transaction_type': u'DEL',
            'transport_type': u'02',
            'dispatch_remarks': 'You are funny guys!',
            'transport_sub_contractor': 'Arpaso',
            'transport_driver_name': 'Ahmed',
            'transport_driver_licence': 'KE23455',
            'transport_vehicle_registration': 'BG2345',
            
            'item-0-slug': 'ISBX00211A1',
            'item-0-waybill': 'ISBX00211A',
            'item-0-stock_item': 'KARX025KARX0010000944801MIXMIXHEBCG15586',
            'item-0-number_of_units': 37,
            'item-0-unit_weight_net': 1,
            'item-0-unit_weight_gross': 1.02,
            'item-0-total_weight_net': 37,
            'item-0-total_weight_gross': 37.24,
            
            'item-TOTAL_FORMS': 1,
            'item-INITIAL_FORMS': 1,
            'item-MAX_NUM_FORMS': 5,
        }
        response = self.client.post(edit_url, data=data)
        self.assertContains(response, "Overloaded ")
        
        data['item-0-number_of_units'] = 12
        #let's check validation. Provide wrong destination warehouse
        response = self.client.post(edit_url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['destination'].errors.as_text(), '* Select a valid choice. That choice is not one of the available choices.')
        
        data['destination'] = 'ISBX003'
        data['item-0-number_of_units'] = '10'    
        data['item-0-overloaded_units'] = True
        
        #Valid data
        response = self.client.post(edit_url, data=data)
        self.assertEqual(response.status_code, 302)
        
        #check updated waybill and loading details
        waybill = ets.models.Waybill.objects.get(pk=self.waybill.pk)
        self.assertEqual(waybill.loading_date, today)
        self.assertEqual(waybill.loading_details.get().number_of_units, 10)
        
        
    #===========================================================================
    # def test_waybill_finalize_dispatch(self):
    #    """ets.views.waybill_finalize_dispatch"""
    #    self.client.login(username='dispatcher', password='dispatcher')
    #    response = self.client.post(reverse('waybill_finalize_dispatch', kwargs={"waybill_pk": self.waybill.pk,}))
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTrue(response.context['print_original'])
    #===========================================================================
    
    def test_waybill_reception(self):
        """ets.views.waybill_reception test"""
        from ets.forms import WaybillRecieptForm
        
        self.client.login(username='dispatcher', password='dispatcher')
        
        path = reverse('waybill_reception', kwargs={'waybill_pk': self.reception_waybill.pk,})
        #check it with dispatching waybill. It must fail
        response = self.client.get(reverse('waybill_reception', kwargs={'waybill_pk': self.waybill.pk,}))
        #System redirects user to login page because he can't receive
        self.assertFalse(self.dispatcher.person.receive)
        self.assertEqual(response.status_code, 302)
        
        #Set receive permit
        self.dispatcher.person.receive = True
        self.dispatcher.person.save()
        
        response = self.client.get(reverse('waybill_reception', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 404)
        
        #Check proper waybill
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], WaybillRecieptForm))
        
        #Let's receive some invalid data (not enough items)
        data = {
            'item-TOTAL_FORMS': 1,
            'item-INITIAL_FORMS': 1,
            'item-MAX_NUM_FORMS': 5,
            
            'item-0-number_units_good': 25,
            'item-0-number_units_lost': 11,
            'item-0-units_lost_reason': 'lsed',
            'item-0-number_units_damaged': 0,
            'item-0-units_damaged_reason': '',
            
            'item-0-slug': 'ISBX00311A1',
            'item-0-waybill': 'ISBX00311A',
            
            'arrival_date': '2012-08-30',
            'start_discharge_date': '2012-08-25',
            'end_discharge_date': '2012-08-24',
            'container_one_remarks_reciept': '',
            'container_two_remarks_reciept': '',
            'distance': 5,
            'receipt_remarks': 'test remarks',
        }
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "Cargo Discharge started before Arrival?")
        data.update({
            'arrival_date': '2012-08-23',
        })
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "Cargo finished Discharge before Starting?")
        data.update({
            'start_discharge_date': '2012-08-24',
        })
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "Over offloaded for 1")
        data.update({
            'item-0-number_units_lost': 0,
            'item-0-number_units_good': 0,
            'item-0-units_lost_reason': '',
        })
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "At least one of the fields number_units_good, number_units_damaged, number_units_lost must be filled")
        data.update({
            'item-0-number_units_good': 25,
        })

        response = self.client.post(path, data=data)
        self.assertContains(response, "35.000 Units loaded but 25.000 units accounted for")
        
        #Let's say we lost 5 units without a reason
        data.update({
            'item-0-number_units_lost': 5,
            'item-0-number_units_damaged': 5,
        })
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "You must provide a loss reason")
        
        # Let's provide a reason and damaged units
        data.update({
            'item-0-units_lost_reason': 'lsed',
        })
        
        response = self.client.post(path, data=data)
        self.assertContains(response, "You must provide a damaged reason")
        
        #Provide a reason of damage
        data.update({
            'item-0-units_damaged_reason': 'dsed',
        })
        
        response = self.client.post(path, data=data)
        #Provide a reception warehouse
        data.update({
            'destination': 'ISBX002',
        })
        
        response = self.client.post(path, data=data)
        
        self.assertEqual(str(response.context['formset'].errors), "[{'total_weight_net_received': [u'This field is required.'], 'total_weight_gross_received': [u'This field is required.']}]")
        
        #Provide total weight net
        data.update({
            'item-0-total_weight_gross_received': '4.0',
            'item-0-total_weight_net_received': '3.5',
        })
        response = self.client.post(path, data=data)

        # Now everything should be all right
        self.assertRedirects(response, self.reception_waybill.get_absolute_url())
        self.assertEqual(ets.models.Waybill.objects.get(pk="ISBX00311A").receipt_remarks, 'test remarks')
    
    def test_waybill_delete(self):
        """ets.views.waybill_delete"""  
        self.client.login(username='dispatcher', password='dispatcher')
        col = ets.models.Waybill.objects.all().count()     
        response = self.client.post(reverse('waybill_delete', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(ets.models.Waybill.objects.all().count(), col-1)
    
    def waybill_validate(self):
        """ets.views.waybill_validate"""
        #Let's check access firstly. Login as dispatcher, who is not a officer
        self.client.login(username='dispatcher', password='dispatcher')
        response = self.client.get(reverse("dispatch_validates"))
        self.assertEqual(response.status_code, 302)
        
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse("dispatch_validates"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 2)
        self.assertEqual(response.context['validated_waybills'].count(), 0)
        
        #Check stock
        stock_item = ets.models.StockItem.objects.get(pk="anotherstock1234")
        stock_item.number_of_units = 10
        stock_item.save()
        response = self.client.get(reverse("dispatch_validates"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "anotherstock1234 (WHEET). Shortage: 60.000")
        stock_item.number_of_units = 1000
        stock_item.save()
        
        #Let's validate some waybill
        response = self.client.get(reverse("validate_dispatch", kwargs={'waybill_pk': self.reception_waybill.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
        self.assertEqual(response.context['validated_waybills'].count(), 1)
        
        #Receipt validation 
        response = self.client.get(reverse("receipt_validates"))
        self.assertEqual(response.status_code, 200)
        #Check there is no waybill
        self.assertEqual(response.context['object_list'].count(), 0)
        self.assertEqual(response.context['validated_waybills'].count(), 0)
        
        #Sign a waybill
        self.delivered_waybill.receipt.sign()
        response = self.client.get(reverse("receipt_validates"))
        self.assertEqual(response.status_code, 200)
        #Check there is a waybill
        self.assertEqual(response.context['object_list'].count(), 1)
        
        #Let's validate it
        response = self.client.get(reverse("validate_receipt", kwargs={'waybill_pk': self.delivered_waybill.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 0)
        self.assertEqual(response.context['validated_waybills'].count(), 1)
        
        
    #===================================================================================================================
    # def test_barcode_qr(self):
    #    """ets.views.barcode_qr"""
    #    response = self.client.get(reverse('barcode_qr', args=(self.waybill.pk,) ))
    #    self.assertEqual(response.status_code, 200) 
    #===================================================================================================================
               
    def test_waybill_finalize_receipt(self):
        """ets.views.waybill_finalize_receipt"""
        
        self.client.login(username='dispatcher', password='dispatcher')
        
        response = self.client.post(reverse('waybill_finalize_receipt', kwargs={'waybill_pk': 'ISBX00312A',}))
        #Dispatcher can not do this, so system redirects him to login page
        self.assertEqual(response.status_code, 302)
        
        #Make him receive goods
        self.dispatcher.person.receive = True
        self.dispatcher.person.save()
        
        response = self.client.post(reverse('waybill_finalize_receipt', kwargs={'waybill_pk': 'ISBX00312A',}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['print_original'])
        
    def test_waybill_compass(self):
        
        waybill = ets.models.Waybill.objects.get(pk='ISBX00211A')
        waybill.sent_compas = datetime.datetime.now()
        waybill.save()
        
        response = self.client.get(reverse('compas_waybill'))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['object_list'].count(), 1)
        
    def test_waybill_compass_receipt(self):
        
        waybill_reciept = ets.models.Waybill.objects.get(pk='ISBX00311A')
        waybill_reciept.receipt_sent_compas = datetime.datetime.now()
        waybill_reciept.save()
        
        response = self.client.get(reverse('compas_waybill_receipt'))
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.context['object_list'].count(), 1)
    
    def test_deserialize(self):
        """ets.views.deserialize"""
        
        #Test with get request
        response = self.client.get(reverse('deserialize'))
        self.assertEqual(response.status_code, 302)
        
        #Test with compressed data
        data = self.reception_waybill.compress()
        response = self.client.get(reverse('deserialize'), data={'data': data,})
        self.assertEqual(response.context['object'], self.reception_waybill)   
        
        #Test receipt get request
        self.client.login(username='recepient', password='recepient')
        response = self.client.get(reverse('deserialize'), data={'data': data, 'receipt': 'Receipt Waybill'})
        self.assertRedirects(response, reverse('waybill_reception_scanned', kwargs={'scanned_code': data,}))

    def test_waybill_reception_scanned(self):
        """ets.views.waybill_reception_scanned"""
        
        self.client.login(username='foreigner', password='recepient')
        data = self.reception_waybill.compress()
        response = self.client.get(reverse('waybill_reception_scanned', kwargs={'scanned_code': data,}))
        self.assertEqual(response.status_code, 200)
        
        form_data = {
            'item-TOTAL_FORMS': 1,
            'item-INITIAL_FORMS': 1,
            'item-MAX_NUM_FORMS': 5,
            
            'item-0-number_units_good': 35,
            'item-0-number_units_lost': 0,
            'item-0-units_lost_reason': '',
            'item-0-number_units_damaged': 0,
            'item-0-units_damaged_reason': '',
            'item-0-total_weight_net_received': '3.5',
            'item-0-total_weight_gross_received': '4.0',
            
            'item-0-slug': 'ISBX00311A1',
            'item-0-waybill': 'ISBX00311A',
            
            'arrival_date': '2012-08-10',
            'start_discharge_date': '2012-08-25',
            'end_discharge_date': '2012-08-26',
            'container_one_remarks_reciept': '',
            'container_two_remarks_reciept': '',
            'distance': 5,
            'receipt_remarks': 'test remarks',
            'destination': 'OE7X001',
        }
        
        response = self.client.post(reverse('waybill_reception_scanned', kwargs={'scanned_code': data,}),
                                    data=form_data)
        # Everything should be fine
        self.assertRedirects(response, self.reception_waybill.get_absolute_url())
        self.assertEqual(ets.models.Waybill.objects.get(pk="ISBX00311A").receipt_remarks, 'test remarks')
        
        data = "-123143"
        response = self.client.get(reverse('waybill_reception_scanned', kwargs={'scanned_code': data,}))
        self.assertEqual(response.status_code, 404)
    
    def test_waybill_errors(self):
        """ets.views.waybill_errors"""
        
        response = self.client.get(reverse('waybill_errors', kwargs={'waybill_pk': self.reception_waybill.pk, 'logger_action': ets.models.CompasLogger.DISPATCH }))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Error-Error-Error")
