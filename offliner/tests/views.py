'''
Created on 20/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-
from datetime import date
from decimal import Decimal

from django.test.client import Client
from django.conf import settings

from offliner.tests.base import AbstractTestCase
from offliner.models import LtiOriginal, Waybill, EpicPerson, Places
from offliner.tools import restant_si
 


class ViewTestCase(AbstractTestCase):
    
    def test_select_action(self):
        client = Client()
        response = client.get('/offliner/')     
        
        # Testing response status code and template          
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'select_action.html')

    def test_ltis_list(self):
        client = Client()
        response = client.get('/offliner/list/')     
        
        # Testing response status code and template          
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'lti/ltis_list.html')
        
        # Prepare expected response context content
        ltis = LtiOriginal.objects.values('code', 'destination_loc_name', 'consegnee_name', 'lti_date').distinct().filter(origin_wh_code=settings.OFFLINE_ORIGIN_WH_CODE)      
        still_ltis = []
        for lti in ltis:
            listOfSI_withDeduction = restant_si(lti['code'])
            for item in listOfSI_withDeduction:
                if item.CurrentAmount > 0 and not lti in still_ltis:
                    still_ltis.append(lti)
        
        # Testing response context content
        self.assertEquals(response.context['ltis'], still_ltis)
        self.assertEquals(response.context['WAREHOUSE_CODE'], settings.OFFLINE_ORIGIN_WH_CODE)
        
    def test_waybills_list(self):
        client = Client()
        response = client.get('/offliner/waybill/list/')     
        
        # Testing response status code and template          
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'waybill/waybills_list.html')
        
        # Prepare expected response context content
        waybills = Waybill.objects.all().order_by('-pk')
        
        # Testing response context content
        self.assertEqualList(response.context['waybill_list'], waybills)   
        
    def test_lti_detail(self):        
        lti_code = 'JERX0011000Z7901P'
        
        client = Client()
        response = client.get('/offliner/info/'+lti_code)  
        
        # Testing response status code and template
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'lti/lti_detail.html')
        
        # Prepare expected response context content
        detailed_lti = LtiOriginal.objects.filter(code=lti_code)       
        waybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code)
        
        # Testing response context content
        self.assertEqualList(response.context['detailed'], detailed_lti)
        self.assertEqualList(response.context['listOfWaybills'], waybills)
        
    def test_waybill_view(self):
        wb_id = 1
        
        client = Client()
        
        # 1. HTTP GET without data
        response = client.get('/offliner/viewwb/')               
        
        #    Testing response status code and template          
        self.assertEquals(302, response.status_code)
        
        # 2. HTTP GET with invalid data 
        response = client.get('/offliner/viewwb/'+str(777))               
        
        #    Testing response status code and template          
        self.assertEquals(302, response.status_code)        
        
        # 3. HTTP GET with valid data
        response = client.get('/offliner/viewwb/'+str(wb_id))
        
        #    Testing response status code and template
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'waybill/print/waybill_detail.html')
             
        #    Prepare expected response context content
        waybill = Waybill.objects.get(id=wb_id)            
        ltis = LtiOriginal.objects.filter(code=waybill.ltiNumber)   
        
        #    Testing response context content
        self.assertEquals(response.context['object'], waybill)
        self.assertEqualList(response.context['ltioriginal'], ltis)   
        
    def test_waybill_reception_list(self):
        client = Client()
        response = client.get('/offliner/waybill/reception/list/')     
        
        # Testing response status code and template          
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'waybill/waybill_reception_list.html')
        
        # Prepare expected response context content
        waybills = Waybill.objects.filter(destinationWarehouse__pk=settings.OFFLINE_ORIGIN_WH_CODE).filter(recipientSigned = False).order_by('-pk')
    
        # Testing response context content
        self.assertEqualList(response.context['waybill_list'], waybills)   
        
    def test_waybill_view_reception(self):
        wb_id = 1
        
        client = Client()
                
        # 1. HTTP GET without data
        response = client.get('/offliner/waybill/viewwb_reception/')               
        
        #    Testing response status code and template          
        self.assertEquals(302, response.status_code)
        
        # 2. HTTP GET with invalid data
        response = client.get('/offliner/waybill/viewwb_reception/'+str(777))               
        
        #    Testing response status code and template          
        self.assertEquals(302, response.status_code)        
              
        # 3. HTTP GET with valid data
        response = client.get('/offliner/waybill/viewwb_reception/'+str(wb_id))     
        
        #    Testing response status code and template          
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.template[0].name, 'waybill/print/waybill_detail_reception.html')
               
        #    Prepare expected response context content
        waybill = Waybill.objects.get(id=wb_id)               
        ltis = LtiOriginal.objects.filter(code=waybill.ltiNumber)
        number_of_lines = waybill.loadingdetail_set.select_related().count()
        extra_lines = 5 - number_of_lines
        my_empty = ['']*extra_lines
        disp_person = EpicPerson.objects.get(person_pk=waybill.dispatcherName) if waybill.dispatcherName else ''        
        rec_person = EpicPerson.objects.get(person_pk=waybill.recipientName) if waybill.recipientName else ''
        
        #    Testing response context content
        self.assertEquals(waybill, response.context['object'])
        self.assertEqualList(ltis, response.context['ltioriginal']) 
        self.assertEquals(my_empty, response.context['extra_lines'])
        self.assertEquals(disp_person, response.context['disp_person'])  
        self.assertEquals(rec_person, response.context['rec_person'])    
        
    def test_waybill_export(self):
        client = Client()
        
        # 1. HTTP GET without data
        response = client.get('/offliner/waybill/export/')               
        
        #    Testing response status code and template          
        self.assertEquals(302, response.status_code)
        

        # 2. HTTP GET with invalid data
        response = client.get('/offliner/waybill/export/', {'wbnumber': 'BAD_WB_NUMBER'})
        
        #    Testing response status code        
        self.assertEquals(302, response.status_code)


        # 3. HTTP GET with valid data
        wb_number = 'X0146'
        response = client.get('/offliner/waybill/export/', {'wbnumber': wb_number})
        
        #    Testing response status code        
        self.assertEquals(200, response.status_code)
        
        #    Prepare expected response context content
        waybill_to_serialize = Waybill.objects.filter(invalidated=False).filter(waybillNumber=wb_number)[0]
        
        from kiowa.db.utils import instance_as_dict            
        waybill_dict = instance_as_dict(waybill_to_serialize, exclude='id')
        
        loading_detail_list_dict = []
        for loading_detail in waybill_to_serialize.loadingdetail_set.select_related():
            loading_detail_list_dict.append(instance_as_dict(loading_detail, exclude=('id','wbNumber')))
        
        import simplejson as json 
        from kiowa.utils.encode import DecimalJSONEncoder       
        serialized_waybill = json.dumps([waybill_dict,loading_detail_list_dict], cls=DecimalJSONEncoder)

        #    Testing response context content       
        self.assertEquals('application/json', response['Content-Type'])
        self.assertEquals('filename=waybill-X0146.json', response['Content-Disposition'])
        self.assertEquals(serialized_waybill, response.content)
        
    def test_waybill_import(self):
        client = Client()

        # Prepare a file to POST
        count_before_import = Waybill.objects.filter(waybillNumber='X0158').count()
        self.assertEquals(0, count_before_import)
        
        import os
        file = open(os.path.dirname(__file__)+'/waybill-X0158.json', 'r')

        response = client.post('/offliner/waybill/import/', {'file': file})  
        
        # Testing response status code        
        self.assertEquals(302, response.status_code)               

        # Testing data import 
        count_after_import = Waybill.objects.filter(waybillNumber='X0158').count()
        self.assertEquals(1, count_after_import)

    def test_waybill_create(self):
        client = Client()

        count_before_create = Waybill.objects.all().count()

        # Prepare request to GET
        lti_code = 'JERX0011000A2040P'
        current_lti = LtiOriginal.objects.filter(code=lti_code)

        response = client.get('/offliner/create/'+lti_code)

        #    Testing response status code
        self.assertEquals(200, response.status_code)
        #...

        #    Testing response context content
        self.assertEquals(unicode(current_lti), unicode(response.context['lti_list']))

        # Prepare request to POST
        post_query_dict = {
                           u'waybillNumber': [u'N/A'],
                           u'transportVehicleRegistration': [u'Vehicle Registration No'],
                           u'transportContractor': [u'RAIS MIDDLE EAST LTD.'],
                           u'dateOfDispatch': [u'2011-01-11'],
                           u'invalidated': [u'False'],
                           u'transportSubContractor': [u'Transport Subcontractor'],
                           u'containerOneRemarksDispatch': [u'Container 1: Remarks'],
                           u'containerTwoSealNumber': [u'Container 2: Seal'],
                           u'dispatchRemarks': [u'Dispatch Remarks'],
                           u'dispatcherTitle': [u'LOGISTICS OFFICER'],
                           u'containerOneSealNumber': [u'Container 1: Seal'],
                           u'ltiNumber': [u'JERX0011000A2040P'],
                           u'csrfmiddlewaretoken': [u'53cf04277d7d0b7116f44492b231c385'],
                           u'transactionType': [u'DEL'],
                           u'containerTwoRemarksDispatch': [u'Container 2: Remarks'],
                           u'dateOfLoading': [u'2011-01-11'],
                           u'recipientConsingee': [u'WORLD FOOD PROGRAMME'],
                           u'transportType': [u'02'],
                           u'destinationWarehouse': [u'QD9X001'],
                           u'recipientLocation': [u'QALANDIA'],
                           u'dispatcherName': [u'JERX0010002630'],
                           u'transportDriverName': [u"Driver's Name"],
                           u'transportDriverLicenceID': [u"Driver's Licens No"],
                           u'containerOneNumber': [u'Container 1: Number'],
                           u'containerTwoNumber': [u'Container 2: Number'],
                           u'transportTrailerRegistration': [u'Trailer Registration No'],

                           u'loadingdetail_set-INITIAL_FORMS': [u'0'],
                           u'loadingdetail_set-TOTAL_FORMS': [u'5'],
                           u'loadingdetail_set-MAX_NUM_FORMS': [u'5'],

                           u'loadingdetail_set-0-id': [u''],
                           u'loadingdetail_set-0-overloadedUnits': [u'on'],
                           u'loadingdetail_set-0-numberUnitsLoaded': [u'100'],
                           u'loadingdetail_set-0-siNo': [u'JERX001000000000000011064HQX0001000000000000905687'],

                           u'loadingdetail_set-1-id': [u''],
                           u'loadingdetail_set-1-numberUnitsLoaded': [u'0'],
                           u'loadingdetail_set-1-siNo': [u''],

                           u'loadingdetail_set-2-id': [u''],
                           u'loadingdetail_set-2-numberUnitsLoaded': [u'0'],
                           u'loadingdetail_set-2-siNo': [u''],

                           u'loadingdetail_set-3-id': [u''],
                           u'loadingdetail_set-3-numberUnitsLoaded': [u'0'],
                           u'loadingdetail_set-3-siNo': [u''],

                           u'loadingdetail_set-4-id': [u''],
                           u'loadingdetail_set-4-numberUnitsLoaded': [u'0'],
                           u'loadingdetail_set-4-siNo': [u'']                  
        }

        response = client.post('/offliner/create/'+lti_code, post_query_dict)

        count_after_create = Waybill.objects.all().count()

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing request effects
        self.assertEquals(count_before_create+1, count_after_create)
        created_waybill = Waybill.objects.all().order_by('-pk')[0]
        self.assertEquals('X0003',created_waybill.waybillNumber)
        self.assertEquals('Vehicle Registration No',created_waybill.transportVehicleRegistration)
        self.assertEquals('RAIS MIDDLE EAST LTD.',created_waybill.transportContractor)
        self.assertEquals('QD9X001',created_waybill.destinationWarehouse.pk)
        created_loading_details = created_waybill.loadingdetail_set.all()
        self.assertEquals(1, len(created_loading_details))
        self.assertEquals(100, created_loading_details[0].numberUnitsLoaded)

    def test_waybill_upload(self):
        wb_id = 1

        client = Client()

        expected_connection_failure_message = "verify your connection"
        expected_data_failure_message = 'verify data integrity'

        # 1. HTTP GET with valid data, but the online app is unreachable
        response = client.get('/offliner/synchronize_waybill/'+str(wb_id))

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_connection_failure_message))
        self.assertFalse(response.cookies['messages'].OutputString().__contains__(expected_data_failure_message))

        # 2. HTTP GET without data
        response = client.get('/offliner/synchronize_waybill/')

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_connection_failure_message))
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_data_failure_message))

        # 3. HTTP GET with invalid data
        response = client.get('/offliner/synchronize_waybill/'+str(777))

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_connection_failure_message))
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_data_failure_message))

        # @todo: find a way to startup online app and then upload Waybill

    def test_stock_download(self):
        client = Client()

        expected_connection_failure_message = "verify your connection"

        # 1. HTTP GET with valid data, but the online app is unreachable
        response = client.get('/offliner/synchronize_stocks/')

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_connection_failure_message))
        
        # @todo: find a way to startup online app and then download Stocks

    def test_lti_download(self):
        client = Client()

        expected_connection_failure_message = "verify your connection"

        # 1. HTTP GET with valid data, but the online app is unreachable
        response = client.get('/offliner/synchronize_ltis/')

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_connection_failure_message))

        # @todo: find a way to startup online app and then download Ltis

    def test_waybill_finalize_dispatch_offline(self):
        wb_id = 1

        client = Client()

#        # 1. HTTP GET without data
#        response = client.get('/offliner/waybill/print_original/')
#
#        #    Testing response status code
#        self.assertEquals(302, response.status_code)
#
#        # 2. HTTP GET with invalid data
#        response = client.get('/offliner/waybill/print_original/'+str(777))
#
#        #    Testing response status code
#        self.assertEquals(302, response.status_code)

        # 3. HTTP GET with valid data
        response = client.get('/offliner/waybill/print_original/'+str(wb_id))

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing request effects
        finalized_waybill = Waybill.objects.get(pk=wb_id)
        self.assertTrue(finalized_waybill.transportDispachSigned)
        self.assertTrue(finalized_waybill.transportDispachSigned)
        self.assertEquals('Print Dispatch Original', finalized_waybill.auditComment)

        # @todo: find a way to startup online app and then upload Waybill

    def test_waybill_finalize_receipt_offline(self):
        wb_id = 1

        client = Client()

#        # 1. HTTP GET without data
#        response = client.get('/offliner/waybill/print_original_receipt/')
#
#        #    Testing response status code
#        self.assertEquals(302, response.status_code)
#
#        # 2. HTTP GET with invalid data
#        response = client.get('/offliner/waybill/print_original_receipt/'+str(777))
#
#        #    Testing response status code
#        self.assertEquals(302, response.status_code)

        # 3. HTTP GET with valid data
        response = client.get('/offliner/waybill/print_original_receipt/'+str(wb_id))

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing response content
        finalized_waybill = Waybill.objects.get(pk=wb_id)
        self.assertTrue(response.cookies['messages'].OutputString().__contains__('Waybill '+ str(finalized_waybill.waybillNumber) +' Receipt Signed'))

        #    Testing request effects
        self.assertTrue(finalized_waybill.recipientSigned)
        self.assertTrue(finalized_waybill.transportDeliverySigned)
        self.assertEquals('Print Dispatch Receipt', finalized_waybill.auditComment)

        # @todo: find a way to startup online app and then upload Waybill

    def test_waybill_reception(self):
        wb_code = 1

        client = Client()

        # Prepare request to GET
        waybill_to_receive = Waybill.objects.get(id=wb_code)
        current_lti = Waybill.objects.get(id=wb_code).ltiNumber

        response = client.get('/offliner/waybill/receive/' + str(wb_code))

        #    Testing response status code
        self.assertEquals(200, response.status_code)
        #...

        #    Testing response context content
        self.assertEquals(unicode(current_lti), unicode(response.context['lti_list']))

        # Prepare request to POST
        post_query_dict = {
                            u'containerOneRemarksReciept': [u''],
                            u'containerTwoRemarksReciept': [u''],
                            u'csrfmiddlewaretoken': [u'e2f67b3e6515a297553e1f014ee5fa7e'],
                            u'invalidated': [u'False'],
                            u'loadingdetail_set-0-id': [u'154'],
                            u'loadingdetail_set-0-numberUnitsDamaged': [u'50.000'],
                            u'loadingdetail_set-0-numberUnitsGood': [u'50.000'],
                            u'loadingdetail_set-0-numberUnitsLost': [u'0.000'],
                            u'loadingdetail_set-0-siNo': [u'JERX001000000000000011128HQX0001000000000000907177'],
                            u'loadingdetail_set-0-unitsDamagedReason': [u'3'],
                            u'loadingdetail_set-0-unitsDamagedType': [u'2'],
                            u'loadingdetail_set-0-unitsLostReason': [u''],
                            u'loadingdetail_set-0-unitsLostType': [u''],
                            u'loadingdetail_set-1-id': [u'155'],
                            u'loadingdetail_set-1-numberUnitsDamaged': [u'50.000'],
                            u'loadingdetail_set-1-numberUnitsGood': [u'100.000'],
                            u'loadingdetail_set-1-numberUnitsLost': [u'50.000'],
                            u'loadingdetail_set-1-siNo': [u'JERX001000000000000011128HQX0001000000000000992018'],
                            u'loadingdetail_set-1-unitsDamagedReason': [u'3'],
                            u'loadingdetail_set-1-unitsDamagedType': [u'3'],
                            u'loadingdetail_set-1-unitsLostReason': [u'4'],
                            u'loadingdetail_set-1-unitsLostType': [u'3'],
                            u'loadingdetail_set-INITIAL_FORMS': [u'2'],
                            u'loadingdetail_set-MAX_NUM_FORMS': [u''],
                            u'loadingdetail_set-TOTAL_FORMS': [u'2'],
                            u'recipientArrivalDate': [u'2010-12-23'],
                            u'recipientConsingee': [u'WORLD FOOD PROGRAMME'],
                            u'recipientDistance': [u'333'],
                            u'recipientEndDischargeDate': [u'2010-12-23'],
                            u'recipientLocation': [u'QALANDIA'],
                            u'recipientRemarks': [u'ricevuti'],
                            u'recipientStartDischargeDate': [u'2010-12-23'],
                            u'waybillNumber': waybill_to_receive.waybillNumber
        }

        response = client.post('/offliner/waybill/receive/' + str(wb_code), post_query_dict)

        #    Testing response status code
        self.assertEquals(302, response.status_code)

        #    Testing request effects
        received_waybill = Waybill.objects.get(id=wb_code)
        self.assertEquals('ricevuti',received_waybill.recipientRemarks)
        self.assertEquals(333,received_waybill.recipientDistance)

    def test_waybill_scan(self):
        client = Client()

        # Prepare text to POST
        count_before_import = Waybill.objects.filter(waybillNumber='X0161').count()
        self.assertEquals(0, count_before_import)
        wb_compressed_str = 'eJxtU11PgzAU/SsNL75M05aPfbyRlSmGDQdElyx76LBRIgNTmIkx/nfbi2OryFPPOffe3kPv3X5Z2Joh6z5INhgTgjH2KXbwgzVCFtHKBhOPaEQ1oirmGpNrApQ9pBxNMVEWH0J+asLVRFLzZw08UIvmnbf5K0rEgcu3RgvjiyZUD9SzsaYnmo7i2zDNwnmK4sUinAeJVqZaWfCyEdApmEj8MEXLkLEoQIGfZijK2A3I4CSTvGrea9mi9LjP66qVPG9rCQFgjknd9VWDVvzQlbUNOipyUSm1Bg2cPorXIi+FsvJSNKpgW9TVKcD9vbQohfw3wDM9TAxIwdJctcmLShUgM7Q6HvYC+qXEFKkh0kFmKngJkj3I6yVnkHXxPtQdJF6q4ARO4/4EdtZ+5K9Y6AMDb/YUJxFDizhm6CGJbxN/uQxglvAp0yb9qa9rj42fY0OpNZvqeYGxw4buEBNSE9omdEzomrDr4XuEtl/dRpzH9PypzfGcu/UG/xGm2PUm4359lHaj2H53euQYyDVQN9yZPIrzLJ+n5sLa9273A4Ud6vo='

        response = client.post('/offliner/waybill/scan/', {'wb_compressed_str': wb_compressed_str})

        # Testing response status code
        self.assertEquals(302, response.status_code)

        # Testing request effects
        count_after_import = Waybill.objects.filter(waybillNumber='X0161').count()
        self.assertEquals(1, count_after_import)

        waybill = Waybill.objects.filter(waybillNumber='X0161')[0]

        self.assertEquals(u'', waybill.auditComment)
        self.assertEquals(u'Container 1: Number', waybill.containerOneNumber)
        self.assertEquals(u'Container 1: Remarks',waybill.containerOneRemarksDispatch)
        self.assertEquals(u'', waybill.containerOneRemarksReciept)
        self.assertEquals(u'Container 1: Seal', waybill.containerOneSealNumber)
        self.assertEquals(u'Container 2: Number', waybill.containerTwoNumber)
        self.assertEquals(u'Container 2: Remarks', waybill.containerTwoRemarksDispatch)
        self.assertEquals(u'', waybill.containerTwoRemarksReciept)
        self.assertEquals(u'Container 2: Seal', waybill.containerTwoSealNumber)
        self.assertEquals(date(2011,01,11), waybill.dateOfDispatch)
        self.assertEquals(date(2011,01,11), waybill.dateOfLoading)
        self.assertEquals(Places.objects.get(org_code='QD9X001'), waybill.destinationWarehouse)
        self.assertEquals(u'Dispatch Remarks', waybill.dispatchRemarks)
        self.assertEquals(u'JERX0010002630', waybill.dispatcherName)
        self.assertEquals(False, waybill.dispatcherSigned)
        self.assertEquals(u'LOGISTICS OFFICER', waybill.dispatcherTitle)
        self.assertEquals(False, waybill.invalidated)
        self.assertEquals(u'JERX0011000A2040P', waybill.ltiNumber)
        self.assertEquals(u'WORLD FOOD PROGRAMME', waybill.recipientConsingee)
        self.assertEquals(u'QALANDIA', waybill.recipientLocation)
        self.assertEquals(u'', waybill.recipientName)
        self.assertEquals(u'', waybill.recipientRemarks)
        self.assertEquals(False, waybill.recipientSigned)
        self.assertEquals(u'', waybill.recipientTitle)
        self.assertEquals(u'Delivery', waybill.transactionType)
        self.assertEquals(u'RAIS MIDDLE EAST LTD.', waybill.transportContractor)
        self.assertEquals(False, waybill.transportDeliverySigned)
        self.assertEquals(False, waybill.transportDispachSigned)
        self.assertEquals(u"Driver's Licens No", waybill.transportDriverLicenceID)
        self.assertEquals(u"Driver's Name", waybill.transportDriverName)
        self.assertEquals(u'Transport Subcontractor', waybill.transportSubContractor)
        self.assertEquals(u'Trailer Registration No', waybill.transportTrailerRegistration)
        self.assertEquals(u'Road', waybill.transportType)
        self.assertEquals(u'Vehicle Registration No', waybill.transportVehicleRegistration)
        self.assertEquals(u'X0161', waybill.waybillNumber)
        self.assertEquals(False, waybill.waybillProcessedForPayment)
        self.assertEquals(False, waybill.waybillRecSentToCompas)
        self.assertEquals(False, waybill.waybillReceiptValidated)
        self.assertEquals(False, waybill.waybillSentToCompas)
        self.assertEquals(False, waybill.waybillValidated)

        self.assertEquals(1, waybill.loadingdetail_set.all().count())

        loadingdetail = waybill.loadingdetail_set.all()[0]
        self.assertEquals(False, loadingdetail.loadingDetailSentToCompas)
        self.assertEquals(Decimal('0.000'), loadingdetail.numberUnitsDamaged)
        self.assertEquals(Decimal('0.000'), loadingdetail.numberUnitsGood)
        self.assertEquals(Decimal('100.000'), loadingdetail.numberUnitsLoaded)
        self.assertEquals(Decimal('0.000'), loadingdetail.numberUnitsLost)
        self.assertEquals(False, loadingdetail.overOffloadUnits)
        self.assertEquals(True, loadingdetail.overloadedUnits)
        self.assertEquals(LtiOriginal.objects.get(lti_pk='JERX001000000000000011064HQX0001000000000000905687'), loadingdetail.siNo)


        # Prepare bad text to POST
        wb_compressed_str = 'THIS_IS_NOT_A VALID_COMPRESSED_REPRESENTATION'

        response = client.post('/offliner/waybill/scan/', {'wb_compressed_str': wb_compressed_str})

        # Testing response status code
        self.assertEquals(302, response.status_code)

        expected_data_failure_message = 'The contents of the text can not be loaded'

        #    Testing response content
        self.assertTrue(response.cookies['messages'].OutputString().__contains__(expected_data_failure_message))
