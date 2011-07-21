### -*- coding: utf-8 -*- ####################################################

import datetime

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

from ..models import Waybill, LtiOriginal, EpicStock
from ..forms import WaybillRecieptForm, WaybillForm

class UnathenticatedTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def test_login_form(self):
        #Check login
        response = self.client.get(reverse('select_action'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('select_action'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.context['form'], AuthenticationForm))


class WaybillTestCase(TestCase):
    
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.waybill = Waybill.objects.get(pk=1)
    
    def test_serialize(self):
        """Checks methods serialize of waybill instance"""
        data = self.waybill.serialize()
        self.assertTrue(data.startswith('[{"pk": 1, "model": "ets.waybill", "fields": {"waybillNumber": "A0009",'))
    
    def test_compress(self):
        """Checks methods compress of waybill instance"""
        data = self.waybill.compress()
        self.assertTrue(data.startswith('eJztWG1zokgQ/iuUn7MpQI1mv6GgUlFxgWySulxRExh1LgjuMG4udbX//RpmhAExuW9XV2fKygvd0zz99NM9M+n89tdzZ//63PmqaFfKc2eXRjj'))


class ClientWaybillTestCase(TestCase):
    
    #multi_db = True
    fixtures = ['development.json', ]
    
    def setUp(self):
        "Hook method for setting up the test fixture before exercising it."
        self.client.login(username='admin', password='admin')
        self.user = User.objects.get(username="admin")
        self.waybill = Waybill.objects.get(pk=1)
        self.lti = LtiOriginal.objects.get(pk="QANX001000000000000005217HQX0001000000000000984141")
        self.stock = EpicStock.objects.get(pk="KARX025KARX0010000944801MIXMIXHEBCG15586")
     
    #===================================================================================================================
    # def tearDown(self):
    #    "Hook method for deconstructing the test fixture after testing it."
    #===================================================================================================================
    
    def test_index(self):
        response = self.client.get(reverse('select_action'))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_reception(self):
        """ets.views.waybill_reception test"""
        response = self.client.get(reverse('waybill_reception', args=(self.waybill.pk,)))
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
            'recipientLocation': u'QANDAHAR CITY',
            'transportContractor': u' MUSLIM TRANSPORT',
            'waybillNumber': 'N/A'
        })
    
    def test_waybill_view(self):
        """ets.views.waybill_view test"""
        response = self.client.get(reverse('waybill_view', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
    
    def test_waybill_validate_form_update(self):
        """ets.views.waybill_validate_form_update test"""
        response = self.client.get(reverse('waybill_validate_form_update', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.lti in response.context['lti_list'])
        
    def test_listOfLtis(self):
        """ets.views.listOfLtis"""
        response = self.client.get(reverse('listOfLtis',args=(self.lti.origin_wh_code,)))
        self.assertEqual(response.status_code, 200)
    
    def test_ltis(self):
        """ets.views.ltis"""
        response = self.client.get(reverse('ltis'))
        self.assertEqual(response.status_code, 200)
        
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

    def test_waybill_finalize_dispatch(self):
        """ets.views.waybill_finalize_dispatch"""
        response = self.client.get(reverse('waybill_finalize_dispatch', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 302) 
        
    def test_waybill_finalize_receipt(self):
        """ets.views.waybill_finalize_receipt"""
        response = self.client.get(reverse('waybill_finalize_receipt', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 302) 
             
    def test_singleWBDispatchToCompas(self):
        """ets.views.singleWBDispatchToCompas"""
        response = self.client.get(reverse('singleWBDispatchToCompas', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 302) 
        
    def test_singleWBReceiptToCompas(self):
        """ets.views.singleWBReceiptToCompas"""
        response = self.client.get(reverse('singleWBReceiptToCompas', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200) 
        
    def test_receiptToCompas(self):
        """ets.views.receiptToCompas"""
        response = self.client.get(reverse('receiptToCompas'))
        self.assertEqual(response.status_code, 200)
        
    def test_invalidate_waybill(self):
        """ets.views.invalidate_waybill"""
        response = self.client.get(reverse('invalidate_waybill', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200)
        
    def test_waybill_view_reception(self):
        """ets.views.waybill_view_reception"""
        response = self.client.get(reverse('waybill_view_reception', args=(self.waybill.pk,)))
        self.assertEqual(response.status_code, 200) 
        
    def test_waybill_validate_receipt_form(self):
        """ets.views.waybill_validate_receipt_form"""
        response = self.client.get(reverse('waybill_validate_receipt_form'))
        self.assertEqual(response.status_code, 200)     
        
        
    def test_deserialize(self):
        """ets.views.deserialize"""
        #Test without post parameters 
        response = self.client.post(reverse('deserialize'))
        
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
        response = self.client.get(reverse('get_wb_stock'))
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
                                                    
#=======================================================================================================================
#    
#        c = Client()
#        response = c.get(reverse('calendar'))
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, 'для Thornhill')
# 
#    def test_calendar_with_radius(self):
#        c = Client()
#        response = c.get(reverse('calendar'), {'radius': 200})
#        self.assertEqual(response.status_code, 200)
#    
#    def test_calendar_with_city(self):
#        c = Client()
#        response = c.get(reverse('calendar'), {'city': 2})
#        self.assertEqual(response.status_code, 200)
#        self.assertContains(response, 'для Los Angeles')
#=======================================================================================================================
