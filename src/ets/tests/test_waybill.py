### -*- coding: utf-8 -*- ####################################################

import datetime
from functools import wraps

from django.core.urlresolvers import reverse
from django.test.client import Client
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
    
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.waybill = ets.models.Waybill.objects.all()[0]
    
    #===================================================================================================================
    # def test_slug(self):
    #    """Tests slug"""
    #    self.assertEqual(self.waybill.slug, u'ISBX00211A')
    #===================================================================================================================
        
    
    def test_serialize(self):
        """Checks methods serialize of waybill instance"""
        data = self.waybill.serialize()
        self.assertTrue(data.startswith('[{"pk": "ISBX00211A", "model": "ets.waybill", "fields": {"waybillNumber": "A0009",'))
    
    def test_compress(self):
        """Checks methods compress of waybill instance"""
        data = self.waybill.compress()
        self.assertTrue(isinstance(data, str))


class ClientWaybillTestCase(TestCase):
    
    multi_db = True
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        
        call_command('loaddata', 'compas.json', verbosity=0, commit=False, database='compas')
        update_compas()
        call_command('loaddata', 'development.json', verbosity=0, commit=False, database='default')
        
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.waybill = ets.models.Waybill.objects.get(pk="ISBX00211A")
        #self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        #self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
        #self.dispatch_point = DispatchPoint.objects.get(pk=1)
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
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
    
    
    def test_waybill_reception(self):
        """ets.views.waybill_reception test"""
        from ..forms import WaybillRecieptForm
        
        response = self.client.get(reverse('waybill_reception', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(isinstance(response.context['form'], WaybillRecieptForm))
        self.assertEqual(response.context['form'].instance, self.waybill)
        #TODO: Append more tests for this view and form inside it.
    
    def test_waybill_search(self):
        """ets.views.waybill_search test"""
        response = self.client.get(reverse('waybill_search'))
        self.assertEqual(response.status_code, 200)
        self.assertTupleEqual(tuple(response.context['waybill_list']), (self.waybill,))
        self.assertTupleEqual(tuple(response.context['my_wb']), (self.waybill.pk,))
        
    def test_create_waybill(self):
        """ets.views.waybillCreate test"""
        from ..forms import WaybillForm
        
        response = self.client.get(reverse('waybillCreate', args=(self.lti.code,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
        self.assertTrue(isinstance(response.context['form'], WaybillForm))
        self.assertEqual(response.context['form'].initial, {
            'dateOfDispatch': datetime.date.today(),
            'dateOfLoading': datetime.date.today(),
            'destinationWarehouse': '',
            'dispatcherName': u'ISBX0020000586',
            'dispatcherTitle': u'LOGISTICS OFFICER',
            'invalidated': 'False',
            'ltiNumber': u'QANX0010010128226P',
            'recipientConsingee': u'DEPARTMENT OF EDUCATION AFGHANISTAN',
            'recipientLocation': u'DADU',
            'transportContractor': u' MUSLIM TRANSPORT',
            'waybillNumber': 'N/A'
        })
    
    def test_waybill_view(self):
        """ets.views.waybill_view test"""
        response = self.client.get(reverse('waybill_view', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_edit(self):
        """ets.views.waybill_edit"""
        response = self.client.get(reverse('waybill_edit', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)

    
    def test_waybill_validate_form_update(self):
        """ets.views.waybill_validate_form_update test"""
        response = self.client.get(reverse('waybill_validate_form_update', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
        
    def test_import_ltis(self):
        """ets.views.import_ltis"""
        response = self.client.get(reverse('import_ltis'))
        self.assertEqual(response.status_code, 302)
    
    def test_lti_detail_url(self):
        """ets.views.lti_detail_url"""
        response = self.client.get(reverse('lti_detail_url', args=(self.lti.code,)))
        self.assertEqual(response.status_code, 200)  
        
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
    
    def test_waybill_finalize_dispatch(self):
        """ets.views.waybill_finalize_dispatch"""
        response = self.client.get(reverse('waybill_finalize_dispatch', kwargs={"waybill_pk": self.waybill.pk,}))
        self.assertEqual(response.status_code, 302) 
    
    
    def test_waybill_finalize_receipt(self):
        """ets.views.waybill_finalize_receipt"""
        
        self.waybill.update_status(ets.models.Waybill.INFORMED)
        
        response = self.client.get(reverse('waybill_finalize_receipt', kwargs={'waybill_pk': self.waybill.pk,}))
        self.assertEqual(response.status_code, 302)
            