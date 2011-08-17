### -*- coding: utf-8 -*- ####################################################

import datetime
from functools import wraps

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponseNotAllowed
from django.utils.datastructures import MultiValueDictKeyError 
from django.contrib.auth.forms import AuthenticationForm
from django.core.management import call_command

import ets.models
from ets.utils import update_compas

def change_settings(func, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        old_settings = {}
        for name, value in kwargs:
            old_settings[name] = getattr(settings, name)
            setattr(settings, value)
            
        result = func(*args, **kwargs)
        
        for name, value in kwargs:
            setattr(settings, old_settings[name])
        
        return result
    
    return wrapper


class WaybillTestCase(TestCase):
    
    multi_db = True
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database='compas')
        update_compas()
        call_command('loaddata', 'development.json', verbosity=0, commit=False, database='default')
        
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.order = ets.models.Order.objects.get(pk='OURLITORDER')
        self.warehouse = ets.models.Warehouse.objects.get(pk="ISBX002")
        #self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        #self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
    def test_serialize(self):
        """Checks methods serialize of waybill instance"""
        data = self.waybill.serialize()
        self.assertTrue(data.startswith('[{"pk": "ISBX00211A", "model": "ets.waybill", "fields": {"dispatcher_person": "ISBX0020000586"'))
    
    def test_compress(self):
        """Checks methods compress of waybill instance"""
        data = self.waybill.compress()
        self.assertTrue(isinstance(data, str))
    
    def test_login_form(self):
        self.client.logout()
        #Check login
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('index'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], AuthenticationForm))
    
    def test_index(self):
        """ tests index direct_to_template page """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_order_list(self):
        """ets.views.order_list"""
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)

        #Provide dispatch warehouse
        response = self.client.get(reverse('orders', kwargs={'warehouse_pk': settings.COMPAS_STATION}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['object_list'].count(), 1)
    
    def test_order_detail(self):
        """Order's detail page"""
        response = self.client.get(reverse('order_detail', kwargs={'object_id': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_view(self):
        """ets.views.waybill_view test"""
        response = self.client.get(reverse('waybill_view', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_search(self):
        """ets.views.waybill_search test"""
        #from ..forms import WaybillSearchForm
        # Empty search query
        response = self.client.post(reverse('waybill_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTupleEqual(tuple(response.context['waybill_list']), (self.waybill,))
        self.assertTupleEqual(tuple(response.context['my_wb']), (self.waybill.pk,))
        #=======================================================================
        # form = WaybillSearchForm({ 'q' : 'ISBX00211A'})
        # response = self.client.post(reverse('waybill_search'), data={'form': form, 'q': 'ISBX00211A'})
        #=======================================================================
        # Search query with existing waybill code  
        response = self.client.post(reverse('waybill_search'), data={'q': 'ISBX00211A'})
        self.assertEqual(response.status_code, 200)
        self.assertTupleEqual(tuple(response.context['waybill_list']), (self.waybill,))
        self.assertTupleEqual(tuple(response.context['my_wb']), (self.waybill.pk,))
        # Search query with not existing waybill code 
        response = self.client.post(reverse('waybill_search'), data={'q': 'ISBX00211A1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['waybill_list']), 0)
        
         
    def test_create_waybill(self):
        """ets.views.waybill_create test"""
        from ..forms import DispatchWaybillForm
        
        response = self.client.get(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}))
        self.assertEqual(response.status_code, 200)
        
        #Check form
        form = response.context['form']
        self.assertTrue(isinstance(form, DispatchWaybillForm))
        #Check that destination has only one possible choice
        self.assertEqual(tuple(form.fields['destination'].queryset.all()), 
                         (ets.models.Warehouse.objects.get(pk="ISBX003"),))
        
        response = self.client.post(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}), data={
            'loading_date': self.order.dispatch_date,
            'dispatch_date': self.order.dispatch_date,
            'destination': 'ISBX003',
            'transaction_type': u'WIT',
            'transport_type': u'02',
            'dispatch_remarks': 'You are funny guys!',
            'transport_sub_contractor': 'Arpaso',
            'transport_driver_name': 'Ahmed',
            'transport_driver_licence': 'KE23455',
            'transport_vehicle_registration': 'BG2345',
            
            'item-0-stock_item': 'testme0123',
            'item-0-number_of_units': '12',
            
            'item-TOTAL_FORMS': 5,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 5,
        })
        self.assertEqual(response.status_code, 302)
        
        #check created waybill and loading details
        waybill = ets.models.Waybill.objects.all()[1]
        self.assertEqual(waybill.loading_details.count(), 1)
    
    def test_waybill_edit(self):
        """ets.views.waybill_edit"""
        response = self.client.get(reverse('waybill_edit', kwargs={
            'order_pk': self.order.pk, 
            'waybill_pk': self.waybill.pk,
        }))
        self.assertContains(response, "Edit waybill: ISBX00211A", status_code=200)
        
        today = datetime.date.today()
        
        #let's check validation. Provide wrong destination warehouse
        response = self.client.post(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}), data={
            'loading_date': today,
            'dispatch_date': today,
            'destination': 'ISBX0034',
            'transaction_type': u'WIT',
            'transport_type': u'02',
            'dispatch_remarks': 'You are funny guys!',
            'transport_sub_contractor': 'Arpaso',
            'transport_driver_name': 'Ahmed',
            'transport_driver_licence': 'KE23455',
            'transport_vehicle_registration': 'BG2345',
            
            'item-0-stock_item': 'testme0123',
            'item-0-number_of_units': '12',
            
            'item-TOTAL_FORMS': 5,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form']['destination'].errors.as_text(), '* Select a valid choice. That choice is not one of the available choices.')
        
        #Valid data
        response = self.client.post(reverse('waybill_create', kwargs={'order_pk': self.order.pk,}), data={
            'loading_date': today,
            'dispatch_date': today,
            'destination': 'ISBX003',
            'transaction_type': u'WIT',
            'transport_type': u'02',
            'dispatch_remarks': 'You are funny guys!',
            'transport_sub_contractor': 'Arpaso',
            'transport_driver_name': 'Ahmed',
            'transport_driver_licence': 'KE23455',
            'transport_vehicle_registration': 'BG2345',
            
            'item-0-stock_item': 'testme0123',
            'item-0-number_of_units': '10',
            
            'item-TOTAL_FORMS': 5,
            'item-INITIAL_FORMS': 0,
            'item-MAX_NUM_FORMS': 5,
        })
        self.assertEqual(response.status_code, 302)
        
        #check updated waybill and loading details
        waybill = ets.models.Waybill.objects.all()[1]
        self.assertEqual(waybill.loading_date, today)
        self.assertEqual(waybill.loading_details.all()[0].number_of_units, 10)
        
        
    def test_waybill_finalize_dispatch(self):
        """ets.views.waybill_finalize_dispatch"""
        response = self.client.get(reverse('waybill_finalize_dispatch', kwargs={"waybill_pk": self.waybill.pk,}))
        self.assertEqual(response.status_code, 302)
        
        waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        self.assertEqual(waybill.status, waybill.SIGNED)
    
    def test_waybill_reception(self):
        """ets.views.waybill_reception test"""
        from ..forms import WaybillRecieptForm
        
        response = self.client.get(reverse('waybill_reception', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(isinstance(response.context['form'], WaybillRecieptForm))
        self.assertEqual(response.context['form'].instance, self.waybill)
        #TODO: Append more tests for this view and form inside it.
    
    def test_waybill_validate_form_update(self):
        """ets.views.waybill_validate_form_update test"""
        response = self.client.get(reverse('waybill_validate_form_update', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
        
    def test_dispatch(self):
        """ets.views.dispatch"""       
        response = self.client.get(reverse('dispatch'))
        self.assertEqual(response.status_code, 302)  

    #===================================================================================================================
    # def test_singleWBDispatchToCompas(self):
    #    """ets.views.singleWBDispatchToCompas"""
    #    response = self.client.get(reverse('singleWBDispatchToCompas', args=(self.waybill.pk,)))
    #    self.assertEqual(response.status_code, 302) 
    #    
    # def test_singleWBReceiptToCompas(self):
    #    """ets.views.singleWBReceiptToCompas"""
    #    response = self.client.get(reverse('singleWBReceiptToCompas', args=(self.waybill.pk,)))
    #    self.assertEqual(response.status_code, 200) 
    #===================================================================================================================
        
    def test_receiptToCompas(self):
        """ets.views.receiptToCompas"""
        response = self.client.get(reverse('receiptToCompas'))
        self.assertEqual(response.status_code, 200)
        
    def test_invalidate_waybill(self):
        """ets.views.invalidate_waybill"""
        response = self.client.get(reverse('invalidate_waybill', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
        
    def test_waybill_view_reception(self):
        """ets.views.waybill_view_reception"""
        response = self.client.get(reverse('waybill_view_reception', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200) 
        
    def test_waybill_validate_receipt_form(self):
        """ets.views.waybill_validate_receipt_form"""
        response = self.client.get(reverse('waybill_validate_receipt_form'))
        self.assertEqual(response.status_code, 200)     
        
    def test_deserialize(self):
        """ets.views.deserialize"""
        #Test with get request
        response = self.client.get(reverse('deserialize'))
        self.assertTrue(isinstance(response, HttpResponseNotAllowed))
        
        #Test without post parameters 
        self.assertRaises(MultiValueDictKeyError, lambda: self.client.post(reverse('deserialize')))
        
        #Test with post parameters
        data = self.waybill.serialize()
        response = self.client.post(reverse('deserialize'), data={'wbdata': data,})
        self.assertEqual(response.status_code, 302)
        
        #Test with compressed data
        data = self.waybill.compress()
        response = self.client.post(reverse('deserialize'), data={'wbdata': data,})
        self.assertEqual(response.status_code, 302)
        
    def test_viewLogView(self):
        """ets.views.viewLogView"""
        response = self.client.get(reverse('viewLogView'))
        self.assertEqual(response.status_code, 200)  
        
    def test_profile(self):
        """ets.views.profile"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200) 
                
    def test_ltis_report(self):
        """ets.views.ltis_report"""
        response = self.client.get(reverse('ltis_report'))
        self.assertEqual(response.status_code, 200)   
        
                               
    def test_dispatch_report_wh(self):
        """ets.views.dispatch_report_wh"""
        response = self.client.get(reverse('dispatch_report_wh', args=(self.lti.origin_wh_code,)))
        self.assertEqual(response.status_code, 200)   
        
    def test_receipt_report_wh(self):
        """ets.views.receipt_report_wh"""
        response = self.client.get(reverse('receipt_report_wh', args=(self.lti.destination_location_code, self.lti.consegnee_code,)))
        self.assertEqual(response.status_code, 200) 
        
    def test_receipt_report_cons(self):
        """ets.views.receipt_report_cons"""
        response = self.client.get(reverse('receipt_report_cons', args=(self.lti.consegnee_code,)))
        self.assertEqual(response.status_code, 200) 
        
        
    def test_select_data(self):
        """ets.views.select_data"""
        response = self.client.get(reverse('select_data'))
        self.assertEqual(response.status_code, 200) 
        
    #===================================================================================================================
    # def test_barcode_qr(self):
    #    """ets.views.barcode_qr"""
    #    response = self.client.get(reverse('barcode_qr', args=(self.waybill.pk,) ))
    #    self.assertEqual(response.status_code, 200) 
    #===================================================================================================================
        
    def test_post_synchronize_waybill(self):
        """ets.views.post_synchronize_waybill"""
        response = self.client.get(reverse('post_synchronize_waybill'))
        self.assertEqual(response.status_code, 200) 
        
    def test_get_synchronize_stock(self):
        """ets.views.get_synchronize_stock"""
        response = self.client.get(reverse('get_synchronize_stock', args=(self.stock.wh_code,)))
        self.assertEqual(response.status_code, 200)  
        
    def test_get_synchronize_lti(self):
        """ets.views.get_synchronize_lti"""
        response = self.client.get(reverse('get_synchronize_lti', args=(self.lti.origin_wh_code,)))
        self.assertEqual(response.status_code, 200) 
         
    def test_get_wb_stock(self):
        """ets.views.get_wb_stock"""
        response = self.client.get(reverse('get_wb_stock'), data={'warehouse': self.dispatch_point.pk})
        self.assertEqual(response.status_code, 200)  
        
    def test_get_synchronize_waybill(self):
        """ets.views.get_synchronize_waybill"""
        response = self.client.get(reverse('get_synchronize_waybill', args=(self.waybill.destinationWarehouse.pk,)))
        self.assertEqual(response.status_code, 200)
        
        
    def test_get_synchronize_waybill2(self):
        """ets.views.get_synchronize_waybill2"""
        response = self.client.get(reverse('get_synchronize_waybill2'))
        self.assertEqual(response.status_code, 200)  
        
    def test_get_all_data(self):
        """ets.views.get_all_data"""
        response = self.client.get(reverse('get_all_data'))
        self.assertEqual(response.status_code, 200)         
        
    def test_get_all_data_download(self):
        """ets.views.get_all_data_download"""
        response = self.client.get(reverse('get_all_data_download'))
        self.assertEqual(response.status_code, 200)  
               
    def waybill_validate_dispatch_form(self):
        """ets.views.waybill_validate_dispatch_form"""
        response = self.client.get(reverse("waybill_validate_dispatch_form"))
        self.assertEqual(response.status_code, 200)     
    
    def test_waybill_finalize_receipt(self):
        """ets.views.waybill_finalize_receipt"""
        
        self.waybill.update_status(ets.models.Waybill.INFORMED)
        
        response = self.client.get(reverse('waybill_finalize_receipt', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 302)
            
