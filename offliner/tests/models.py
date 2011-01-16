'''
Created on 20/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from datetime import date

from django.conf import settings
from django.db import IntegrityError, DatabaseError
from django.db.models import Max

from offliner.models import Waybill, WaybillSynchroState, Places, LoadingDetail, LtiOriginal, EpicStock, LossesDamagesReason, \
                            LossesDamagesType, EpicLossReason, EpicPerson, DispatchPoint, ReceptionPoint, \
                            PackagingDescriptonShort, SIWithRestant
from offliner.tests.base import AbstractTestCase



class WaybillTestCase(AbstractTestCase):
      
    def test_save_bestcase(self):
        """
        Test save best-case: all mandatory fields are provided.
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
        
    def test_save_worstcase_1(self):
        """
        Test save worst-case: not all mandatory fields are provided => IntegrityError.
        """             
        data = {
                'ltiNumber' : 'ltiNumber',
                'waybillNumber' : 'waybillNumber',
                'dateOfLoading' : date(2010,11,11),
                'dateOfDispatch' : date(2010,11,11),
                'transactionType' : 'WIT',
                'transportType' : '02',
        }        
       
        target_item = Waybill(**data)
        self.assertRaises(IntegrityError, target_item.save)
        
    def test_waybill_instance_methods(self):
        """
        Test the Waybill instance methods.
        """
        waybill = Waybill.objects.get(id=1)
               
        self.assertEquals('X0146', unicode(waybill))
        self.assertEquals('X0146', waybill.mydesc())
        
        self.assertEquals(True, waybill.check_lines())
        self.assertEquals(True, waybill.check_lines_receipt())
        
        if waybill.dispatcherName:
            self.assertEquals(EpicPerson.objects.get(person_pk=waybill.dispatcherName), waybill.dispatchPerson())
        
        if waybill.recipientName:
            self.assertEquals(EpicPerson.objects.get(person_pk=waybill.recipientName), waybill.recieptPerson())
        
        self.assertEquals(False, waybill.isBulk())



class OwnedWaybillManagerTestCase(AbstractTestCase):  
    
    def test_get_query_set(self):
        """
        Test Wabills retrieve by OwnedWaybillManager.
        """
        # Prepare expected method return     
        expected_owned_waybills = Waybill.objects.filter(ltiNumber__in = [e.code for e in LtiOriginal.objects.filter(origin_wh_code=settings.OFFLINE_ORIGIN_WH_CODE)])     
        
        # Call to tested method
        actual_owned_waybills = Waybill.owned.all() 
        
        # Testing method return
        self.assertEquals(str(expected_owned_waybills), str(actual_owned_waybills))   
          
          
 
class WaybillSynchroStateTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'waybill' : Waybill.objects.all()[0],
        }
       
        rec_num_before = WaybillSynchroState.objects.all().count()       
       
        target_item = WaybillSynchroState(**data)
        target_item.save()   
       
        rec_num_after = WaybillSynchroState.objects.all().count()    
        
        if rec_num_before == 0:
            self.assertEquals(rec_num_before+1, rec_num_after)
        else:
            self.assertEquals(rec_num_before, rec_num_after)
        self.assertEquals(target_item.synchronized, False)

    def test_save_worst_case(self):
        """
        Test save worst-case: not all mandatory fields are provided => IntegrityError.
        """       
        data = {
                'synchronized' : True,
        }        
       
        target_item = WaybillSynchroState(**data)
        self.assertRaises(IntegrityError, target_item.save)      
       
        

class LoadingDetailTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'wbNumber' : Waybill.objects.all()[0],
                'siNo' : LtiOriginal.objects.all()[0],
                'overloadedUnits' : True,
                'loadingDetailSentToCompas' :  True,
                'overOffloadUnits' : True,
        }
       
        max_id = int(LoadingDetail.objects.aggregate(Max('id')).get('id__max'))       
       
        target_item = LoadingDetail(**data)
        target_item.save()   
       
        stored_item = LoadingDetail.objects.get(id=max_id+1)    
        
        self.assertEquals(target_item, stored_item)     
   
    def test_save_worst_case(self):
        """
        Test save worst-case: not all mandatory fields are provided => IntegrityError.
        """      
        data = {
                'siNo' : LtiOriginal.objects.all()[0],
                'overloadedUnits' : True,
                'loadingDetailSentToCompas' :  True,
                'overOffloadUnits' : True,
        }        
       
        target_item = LoadingDetail(**data)
        self.assertRaises(IntegrityError, target_item.save)

    def test_loadingdetail_instance_methods(self):
        """
        Test the LoadingDetail instance methods.
        """
        loadingdetail = LoadingDetail.objects.all()[0]

        self.assertEquals('X0146 - JERX0011000A2066P - JERX001000000000000011128HQX0001000000000000907177', unicode(loadingdetail))
        from decimal import Decimal
        self.assertEquals(Decimal('0.000000'), loadingdetail.calcGrossRecievedGood())
        self.assertEquals(Decimal('0.000000'), loadingdetail.calcGrossRecievedDamaged())
        self.assertEquals(Decimal('0.000000'), loadingdetail.calcNetRecievedLost())
        self.assertEquals(Decimal('0.000000'), loadingdetail.calcGrossRecievedLost())



class PlacesTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'org_code' : 'A007',
        }
       
        rec_num_before = Places.objects.all().count()       
        
        target_item = Places(**data)
        target_item.save()   
       
        rec_num_after = Places.objects.all().count()    
        
        self.assertEquals(rec_num_before+1, rec_num_after) 
        
    def test_save_worst_case(self):
        """
        Test save worst-case: invalid pk field value => DatabaseError.
        """       
        data = {
                'org_code' : 'INVALID_ORG_CODE',
        }        
       
        target_item = Places(**data)
        
        self.assertRaises(DatabaseError, target_item.save)
        
    def test_place_instance_methods(self):
        """
        Test the Place instance methods.
        """        
        place = Places.objects.get(org_code='ASHX004')
                
        self.assertEquals('ASHDOD_OVERSEAS_BONDED', unicode(place))
       


class OwnedLtiOriginalManagerTestCase(AbstractTestCase):  
    
    def test_get_query_set(self):
        """
        Test LtiOriginal retrieve by OwnedLtiOriginalManager.
        """
        # Prepare expected method return     
        expected_owned_ltis = LtiOriginal.objects.filter(origin_wh_code=settings.OFFLINE_ORIGIN_WH_CODE)
        
        # Call to tested method
        actual_owned_ltis = LtiOriginal.owned.all() 
        
        # Testing method return
        self.assertEquals(str(expected_owned_ltis), str(actual_owned_ltis)) 
        
       

class LtiOriginalTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'lti_pk' : 'lti_pk',
                'lti_id' : 'lti_id',
                'code' : 'code',
                'lti_date' : date(2010,11,11),     
                'quantity_net' : 100,
                'quantity_gross' : 50,
                'number_of_units' : 350,  
        }
       
        rec_num_before = LtiOriginal.objects.all().count()       
       
        target_item = LtiOriginal(**data)
        target_item.save()   
       
        rec_num_after = LtiOriginal.objects.all().count()    
        
        self.assertEquals(rec_num_before+1, rec_num_after) 
        
    def test_save_worst_case(self):
        """
        Test save worst-case: not pk field value provided => DatabaseError.
        """       
        data = {
                'lti_id' : 'lti_id',
                'code' : 'code',
                'lti_date' : date(2010,11,11),
        }        
        
        target_item = LtiOriginal(**data)
        
        self.assertRaises(DatabaseError, target_item.save)

    def test_lti_instance_methods(self):
        """
        Test the LtiOriginal instance methods.
        """
        lti = LtiOriginal.objects.get(lti_pk='JERX001000000000000011031HQX0001000000000000990922')

        self.assertEquals(' No Stock   WHEAT FLOUR  3000 ', unicode(lti))
        self.assertEquals('JERX0011000Z7901P', lti.mydesc())
        self.assertEquals(lti.cmmname, lti.commodity())
        #self.assertEquals(lti.sitracker.number_units_left, lti.restant())



class EpicStockTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'wh_pk' : 'wh_pk',
                'number_of_units' : 100,
        }
       
        rec_num_before = EpicStock.objects.all().count()       
       
        target_item = EpicStock(**data)
        target_item.save()   
       
        rec_num_after = EpicStock.objects.all().count()    
        
        self.assertEquals(rec_num_before+1, rec_num_after) 
        
    def test_save_worst_case(self):
        """
        Test save worst-case: not all mandatory fields are provided => IntegrityError.
        """       
        data = {
                'wh_regional' : 'Z007',
                'wh_country' : 'wh_country',
                'wh_location' : 'wh_location',
        }        
        
        target_item = EpicStock(**data)
        
        self.assertRaises(IntegrityError, target_item.save)

    def test_stock_instance_methods(self):
        """
        Test the EpicStock instance methods.
        """
        data = {
                'wh_name': 'warehouse name',
                'cmmname': 'cmm name',
                'wh_pk' : 'wh_pk',
                'number_of_units' : 100,
        }

        target_item = EpicStock(**data)
        target_item.save()         

        self.assertEquals('warehouse name\tcmm name\t100', unicode(target_item))

        
        
class LossesDamagesReasonTestCase(AbstractTestCase):
    
    def test_save_bestcase(self):
        """
        Test save best-case: all mandatory fields are provided.
        """             
        data = {
                'compasRC' : EpicLossReason.objects.all()[0],
                'compasCode' : 'compasCode',
                'description' : 'description',
        }
       
        max_id = int(LossesDamagesReason.objects.aggregate(Max('id')).get('id__max'))       
       
        target_item = LossesDamagesReason(**data)
        target_item.save()   
       
        stored_item = LossesDamagesReason.objects.get(id=max_id+1)    
        
        self.assertEquals(target_item, stored_item)   
        
    def test_save_worstcase_1(self):
        """
        Test save worst-case: not all mandatory fields are provided => IntegrityError.
        """             
        data = {
                'compasCode' : 'compasCode',
                'description' : 'description',
        }        
       
        target_item = LossesDamagesReason(**data)
        self.assertRaises(IntegrityError, target_item.save)

    def test_lossdamagesreason_instance_methods(self):
        """
        Test the LossesDamagesReason instance methods.
        """
        data = {
                'compasRC' : EpicLossReason.objects.get(reason_code='0001'),
                'compasCode' : 'compasCode',
                'description' : 'description',
        }

        max_id = int(LossesDamagesReason.objects.aggregate(Max('id')).get('id__max'))

        target_item = LossesDamagesReason(**data)
        target_item.save()

        self.assertEquals('DETERIORATION OF PACKAGING MATERIALS', unicode(target_item))



class LossesDamagesTypeTestCase(AbstractTestCase):
    
    def test_save_bestcase(self):
        """
        Test save best-case: all mandatory fields are provided.
        """             
        data = {
                'description' : 'description',
        }
       
        max_id = int(LossesDamagesType.objects.aggregate(Max('id')).get('id__max'))       
       
        target_item = LossesDamagesType(**data)
        target_item.save()   
       
        stored_item = LossesDamagesType.objects.get(id=max_id+1)    
        
        self.assertEquals(target_item, stored_item) 
        
    def test_save_worstcase_1(self):
        """
        Test save worst-case: invalid description field value => DatabaseError.
        """             
        data = {
                'description' : 'INVALID_DESCRIPTION_TOO_LONG_VALUE',
        }        
       
        target_item = LossesDamagesType(**data)
        self.assertRaises(DatabaseError, target_item.save)   

    def test_lossdamagestype_instance_methods(self):
        """
        Test the LossesDamagesType instance methods.
        """
        data = {
                'description' : 'losses damages type',
        }

        target_item = LossesDamagesType(**data)
        target_item.save()

        self.assertEquals('losses damages type', unicode(target_item))

        
        
class EpicLossReasonTestCase(AbstractTestCase):
    
    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """   
        data = {
                'reason_code' : 'RC001',
                'reason' : 'reason',
        }
       
        rec_num_before = EpicLossReason.objects.all().count()       
       
        target_item = EpicLossReason(**data)
        target_item.save()   
       
        rec_num_after = EpicLossReason.objects.all().count()    
        
        self.assertEquals(rec_num_before+1, rec_num_after) 
        
    def test_save_worst_case(self):
        """
        Test save worst-case: invalid reason_code field value => DatabaseError.
        """       
        data = {
                'reason_code' : 'INVALID_REASON_CODE_TOO_LONG_VALUE',
                'reason' : 'reason',
        }        
        
        target_item = EpicLossReason(**data)
        
        self.assertRaises(DatabaseError, target_item.save)

    def test_lossreason_instance_methods(self):
        """
        Test the EpicLossReason instance methods.
        """
        data = {
                'reason_code' : 'RC001',
                'reason' : 'reason description',
        }
       
        target_item = EpicLossReason(**data)
        target_item.save()

        self.assertEquals('reason description', unicode(target_item))



class DispatchPointTestCase(AbstractTestCase):

    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """
        data = {
                'origin_loc_name': 'origin_loc_name',
                'origin_location_code': 'origin_loc_name',
                'origin_wh_code': 'origin_wh_code',
                'origin_wh_name': 'origin_wh_name',
        }

        rec_num_before = DispatchPoint.objects.all().count()

        target_item = DispatchPoint(**data)
        target_item.save()

        rec_num_after = DispatchPoint.objects.all().count()

        self.assertEquals(rec_num_before+1, rec_num_after)

    def test_save_worst_case(self):
        """
        Test save worst-case: invalid fields length => DatabaseError.
        """
        data = {
                'origin_loc_name': 'too long origin location name',
        }

        target_item = DispatchPoint(**data)
        
        self.assertRaises(DatabaseError, target_item.save)

    def test_dispatchpoint_instance_methods(self):
        """
        Test the DispatchPoint instance methods.
        """
        dispatchpoint = DispatchPoint.objects.get(id='2')

        self.assertEquals('QD9X002 - QALANDIA', unicode(dispatchpoint))



class ReceptionPointTestCase(AbstractTestCase):

    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """
        data = {
                'loc_name': 'loc_name',
                'location_code': 'location_code',
                'consegnee_code': 'consegnee_code',
                'consegnee_name': 'consegnee_name',
        }

        rec_num_before = ReceptionPoint.objects.all().count()

        target_item = ReceptionPoint(**data)
        target_item.save()

        rec_num_after = ReceptionPoint.objects.all().count()

        self.assertEquals(rec_num_before+1, rec_num_after)

    def test_save_worst_case(self):
        """
        Test save worst-case: invalid fields length => DatabaseError.
        """
        data = {
                'loc_name': 'too long location name',
        }

        target_item = ReceptionPoint(**data)

        self.assertRaises(DatabaseError, target_item.save)

    def test_receptionpoint_instance_methods(self):
        """
        Test the ReceptionPoint instance methods.
        """
        receptionpoint = ReceptionPoint.objects.get(id='159')

        self.assertEquals('ABU DEIS WFP_DISTRIB - WFP_DISTRIBUTION TEAM', unicode(receptionpoint))



class PackagingDescriptonShortTestCase(AbstractTestCase):

    def test_save_best_case(self):
        """
        Test save best-case: all mandatory fields are provided.
        """
        data = {
                'packageCode': 'XXX02',
                'packageShortName': 'BAMBOO BAS',
        }

        rec_num_before = PackagingDescriptonShort.objects.all().count()

        target_item = PackagingDescriptonShort(**data)
        target_item.save()

        rec_num_after = PackagingDescriptonShort.objects.all().count()

        self.assertEquals(rec_num_before+1, rec_num_after)

    def test_save_worst_case(self):
        """
        Test save worst-case: invalid fields length => DatabaseError.
        """
        data = {
                'packageCode': 'too long package code',
        }

        target_item = PackagingDescriptonShort(**data)

        self.assertRaises(DatabaseError, target_item.save)

    def test_packagingdescriptonshort_instance_methods(self):
        """
        Test the PackagingDescriptonShort instance methods.
        """
        packagingdescriptonshort = PackagingDescriptonShort.objects.get(packageCode='TN21')

        self.assertEquals('TN21 - BOTTLE  1 ', unicode(packagingdescriptonshort))



class SIWithRestantTestCase(AbstractTestCase):

    def test_siwithrestant_instance_methods(self):
        siwithrestant = SIWithRestant(SINumber='SINumber', StartAmount=10.0, CommodityName='CommodityName')

        self.assertEquals('SINumber', siwithrestant.SINumber)
        self.assertEquals(10.0, siwithrestant.getStartAmount())
        self.assertEquals(10.0, siwithrestant.getCurrentAmount())

        siwithrestant.reduceCurrent(4.0)

        self.assertEquals(10.0, siwithrestant.getStartAmount())
        self.assertEquals(6.0, siwithrestant.getCurrentAmount())
