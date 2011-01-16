'''
Created on 02/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models, connection
from django.db.models import Model
from django.db.models.manager import Manager
from django.contrib.auth.models import User

from audit_log.models.managers import AuditLog



class Places(Model):
    '''
    Places : Class that models a geographical place.
    This data are managed by Compas.
    '''
    org_code = models.CharField(max_length=7, primary_key=True, db_column='ORG_CODE')
    name = models.CharField(max_length=100, db_column='NAME')
    geo_point_code = models.CharField(max_length=4, db_column='GEO_POINT_CODE')
    geo_name = models.CharField(max_length=100, db_column='GEO_NAME')
    country_code = models.CharField(max_length=3, db_column='COUNTRY_CODE')
    reporting_code = models.CharField(max_length=7, db_column='REPORTING_CODE')
    organization_id = models.CharField(max_length=20, db_column='ORGANIZATION_ID')
    
    class Meta:
        db_table = u'epic_geo'
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.name
    

class OwnedWaybillManager(Manager):
    '''
    OwnedWaybillManager: Manager class that retrieves only owned Waybills, filtering by warehouse code.
    '''  
    def get_query_set(self):
        owned_ltis_list = [e.code for e in LtiOriginal.objects.filter(origin_wh_code=settings.OFFLINE_ORIGIN_WH_CODE)]       
        return Waybill.objects.filter(ltiNumber__in = owned_ltis_list)
      

class Waybill(Model):
    '''
    Waybill: @todo write Class definition.
    This data are managed by ETS.
    '''
    
    objects = Manager()
    owned = OwnedWaybillManager()
    
    transaction_type_choice = (
        (u'WIT', u'WFP Internal'),
        (u'DEL', u'Delivery'),
#        (u'SWA',u'Swap'),
#        (u'REP',u'Repayment'),
#        (u'SAL',u'Sale'),
#        (u'ADR',u'Air drop'),
#        (u'INL',u'Inland Shipment')
#        (u'DIS', u'Distribution'),
#        (u'LON', u'Loan'),
#        (u'DSP', u'Disposal'),
#        (u'PUR', u'Purchase'),
#        (u'SHU',u'Shunting'),
#        (u'COS',u'Costal Transshipment'),
    )
    
    transport_type = (
        (u'02', u'Road'),
#        (u'01',u'Rail'),
#        (u'04',u'Air'),
#        (u'I',u'Inland Waterways'),
#        (u'C',u'Costal Waterways'),
#        (u'07',u'Multi-mode'),
#        (u'O',u'Other Please Specify')
    )
                        
    # General fields
    ltiNumber = models.CharField(max_length=20)
    waybillNumber = models.CharField(max_length=20)
    dateOfLoading = models.DateField(null=True, blank=True)
    dateOfDispatch = models.DateField(null=True, blank=True)
    transactionType = models.CharField(max_length=10, choices=transaction_type_choice)
    transportType = models.CharField(max_length=10, choices=transport_type)
    
    # Dispatcher fields
    dispatchRemarks = models.CharField(max_length=200)
    dispatcherName = models.TextField(blank=True, null=True)
    dispatcherTitle = models.TextField(blank=True)
    dispatcherSigned = models.BooleanField(blank=True)
    
    # Transporter fields
    transportContractor = models.TextField(blank=True)
    transportSubContractor = models.TextField(blank=True)
    transportDriverName = models.TextField(blank=True)
    transportDriverLicenceID = models.TextField(blank=True)
    transportVehicleRegistration = models.TextField(blank=True)
    transportTrailerRegistration = models.TextField(blank=True)
    transportDispachSigned = models.BooleanField(blank=True)
    transportDispachSignedTimestamp = models.DateTimeField(null=True, blank=True)
    transportDeliverySigned = models.BooleanField(blank=True)
    transportDeliverySignedTimestamp = models.DateTimeField(null=True, blank=True)
    
    # Container fields       
    containerOneNumber = models.CharField(max_length=40, blank=True)
    containerTwoNumber = models.CharField(max_length=40, blank=True)
    containerOneSealNumber = models.CharField(max_length=40, blank=True)
    containerTwoSealNumber = models.CharField(max_length=40, blank=True)
    containerOneRemarksDispatch = models.CharField(max_length=40, blank=True)
    containerTwoRemarksDispatch = models.CharField(max_length=40, blank=True)
    containerOneRemarksReciept = models.CharField(max_length=40, blank=True)
    containerTwoRemarksReciept = models.CharField(max_length=40, blank=True)
    
    # Recipient fields
    recipientLocation = models.CharField(max_length=100, blank=True)
    recipientConsingee = models.CharField(max_length=100, blank=True)
    recipientName = models.CharField(max_length=100, blank=True)
    recipientTitle = models.CharField(max_length=100, blank=True)
    recipientArrivalDate = models.DateField(null=True, blank=True)
    recipientStartDischargeDate = models.DateField(null=True, blank=True)
    recipientEndDischargeDate = models.DateField(null=True, blank=True)
    recipientDistance = models.IntegerField(blank=True, null=True)
    recipientRemarks = models.TextField(blank=True)
    recipientSigned = models.BooleanField(blank=True)
    recipientSignedTimestamp = models.DateTimeField(null=True, blank=True)
    destinationWarehouse = models.ForeignKey(Places, blank=True)
    
    # Extra fields
    waybillValidated = models.BooleanField()
    waybillReceiptValidated = models.BooleanField()
    waybillSentToCompas = models.BooleanField()
    waybillRecSentToCompas = models.BooleanField()
    waybillProcessedForPayment = models.BooleanField()
    invalidated = models.BooleanField()
    
    # Audit fields
    auditComment = models.TextField(null=True, blank=True)
    
    audit_log = AuditLog()

    class Meta:        
        app_label = 'offliner'    
        
    def __unicode__(self):
        return self.waybillNumber
        
    def mydesc(self):
        return self.waybillNumber
        
    def errors(self):
        return loggerCompas.objects.get(wb=self)
    
    def check_lines(self):
        lines = LoadingDetail.objects.filter(wbNumber=self)
        for line in lines:
            if line.check_stock():
                pass
            else:
                return False
        return True
    
    def check_lines_receipt(self):
        lines = LoadingDetail.objects.filter(wbNumber=self)
        for line in lines:
            if line.check_reciept_item():
                pass
            else:
                return False
        return True
    
    def dispatchPerson(self):
        return EpicPerson.objects.get(person_pk=self.dispatcherName)
    
    def recieptPerson(self):
        return EpicPerson.objects.get(person_pk=self.recipientName)
    
    def isBulk(self):
        return LtiOriginal.objects.filter(code=self.ltiNumber)[0].isBulk()

 
class WaybillSynchroState(Model):
    '''
    WaybillSynchroState: Utility class that models an helper table used to store Waybill synchronization state.
    This data are managed by ETS.
    '''
    waybill = models.ForeignKey(Waybill, primary_key=True)
    synchronized = models.BooleanField(default=False)
        

'''
Models based on Compas Views & Tables
'''    


class OwnedLtiOriginalManager(Manager):
    '''
    OwnedLtiOriginalManager: Manager class that retrieves only owned LtiOriginals, filtering by warehouse code.
    '''  
    def get_query_set(self):
        return LtiOriginal.objects.filter(origin_wh_code=settings.OFFLINE_ORIGIN_WH_CODE)      


class LtiOriginal(Model):
    '''
    LTI: Class that models a Landside Transport Instruction.
    This data are managed by Compas. 
    '''
    
    objects = Manager()
    owned = OwnedLtiOriginalManager()
    
    lti_pk = models.CharField(max_length=50, primary_key=True, db_column='LTI_PK')
    lti_id = models.CharField(max_length=40, db_column='LTI_ID')
    code = models.CharField(max_length=40, db_column='CODE')
    lti_date = models.DateField(db_column='LTI_DATE')
    expiry_date = models.DateField(blank=True, null=True, db_column='EXPIRY_DATE')
    transport_code = models.CharField(max_length=4, db_column='TRANSPORT_CODE')
    transport_ouc = models.CharField(max_length=13, db_column='TRANSPORT_OUC')
    transport_name = models.CharField(max_length=30, db_column='TRANSPORT_NAME')
    origin_type = models.CharField(max_length=1, db_column='ORIGIN_TYPE')
    origintype_desc = models.CharField(max_length=12, blank=True, db_column='ORIGINTYPE_DESC')
    origin_location_code = models.CharField(max_length=10, db_column='ORIGIN_LOCATION_CODE')
    origin_loc_name = models.CharField(max_length=30, db_column='ORIGIN_LOC_NAME')
    origin_wh_code = models.CharField(max_length=13, blank=True, db_column='ORIGIN_WH_CODE')
    origin_wh_name = models.CharField(max_length=50, blank=True, db_column='ORIGIN_WH_NAME')
    destination_location_code = models.CharField(max_length=10, db_column='DESTINATION_LOCATION_CODE')
    destination_loc_name = models.CharField(max_length=30, db_column='DESTINATION_LOC_NAME')
    consegnee_code = models.CharField(max_length=12, db_column='CONSEGNEE_CODE')
    consegnee_name = models.CharField(max_length=80, db_column='CONSEGNEE_NAME')
    requested_dispatch_date = models.DateField(blank=True, null=True, db_column='REQUESTED_DISPATCH_DATE')
    project_wbs_element = models.CharField(max_length=24, blank=True, db_column='PROJECT_WBS_ELEMENT')
    si_record_id = models.CharField(max_length=25, blank=True, db_column='SI_RECORD_ID')
    si_code = models.CharField(max_length=8, db_column='SI_CODE')
    comm_category_code = models.CharField(max_length=9, db_column='COMM_CATEGORY_CODE')
    commodity_code = models.CharField(max_length=18, db_column='COMMODITY_CODE')
    cmmname = models.CharField(max_length=100, blank=True, db_column='CMMNAME')
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3, db_column='QUANTITY_NET')
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3, db_column='QUANTITY_GROSS')
    number_of_units = models.DecimalField(max_digits=7, decimal_places=0, db_column='NUMBER_OF_UNITS')
    unit_weight_net = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_column='UNIT_WEIGHT_NET')
    unit_weight_gross = models.DecimalField(max_digits=8, decimal_places=3, blank=True, null=True, db_column='UNIT_WEIGHT_GROSS')
        
    class Meta:
        db_table = u'epic_lti'
        app_label = 'offliner' 
                
    def __unicode__(self):
        return self.valid() + ' ' + self.coi_code() + '  ' + self.cmmname + '  %.0f ' % self.restant2() 
    
    def mydesc(self):
        return self.code
        
    def commodity(self):
        return self.cmmname 
        
    def restant(self):
        return self.sitracker.number_units_left
        
    def valid(self):
        return "Void " if RemovedLtis.objects.filter(lti=self.lti_pk) else ''
        
    def restant2(self):
        lines = LoadingDetail.objects.filter(siNo=self)
        used = 0
        
        for line in lines:
            used += line.numberUnitsLoaded
        
        return self.quantity_net - used if self.isBulk() else self.number_of_units - used
            
    def reducesi(self, units):
        self.sitracker.updateUnits(units)
        return self.restant()
        
    def inStock(self):
        try:
            thisItem = EpicStock.objects.filter(wh_code=self.origin_wh_code).filter(si_code=self.si_code).filter(commodity_code=self.commodity_code)
        except:
            pass
        
    def restoresi(self, units):
        self.sitracker.updateUnitsRestore(units)
        return self.restant()
        
    def packaging(self):
        pack = 'Unknown'
        
        try:
            mypkg = EpicStock.objects.filter(wh_code=self.origin_wh_code).filter(si_code=self.si_code).filter(commodity_code=self.commodity_code)
            pack = str(mypkg[0].packagename)
        except:
#            print 'nogo'
            pass
        
        return pack
    
    def isBulk(self):
        return self.packaging() == 'BULK'
        
    def coi_code(self):
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT origin_id from epic_stock where  (WH_CODE=%s  and SI_CODE=%s and COMMODITY_CODE=%s )", [self.origin_wh_code, self.si_code, self.commodity_code])
            stock = cursor.fetchall()
            item = stock[0]
            return str(item[0][7:])              
        except:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT origin_id from epic_stock where  ( SI_CODE=%s and COMM_CATEGORY_CODE=%s )", [self.si_code, self.comm_category_code])
                stock = cursor.fetchall()
                item = stock[0]
                return str(item[0][7:])
            except:                
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT origin_id from epic_stock where  (WH_CODE=%s  and SI_CODE=%s and COMM_CATEGORY_CODE=%s )", [self.origin_wh_code, self.si_code, self.comm_category_code])
                    stock = cursor.fetchall()
                    item = stock[0]
                    return str(item[0][7:])
                except:                
                    return 'No Stock '
                    
    def remove_lti(self):
        all_removed = RemovedLtis.objects.all()
        this_lti = RemovedLtis()
        this_lti.lti = self
        if this_lti not in all_removed:
            this_lti.save()


class removedLtisManager(models.Manager):
    '''
    removedLtisManager: Manager class that retrieves removed LTIs.
    '''
        
    def list(self):
        listExl = []
        listOfExcluded = RemovedLtis.objects.all()
        for exl in listOfExcluded:
            listExl += [exl.lti.LTI_PK]
        return listExl


class RemovedLtis(Model):
    '''
    RemovedLtis: Utility class that models an helper table for nolonger existing LTI items.
    This data are managed by Compas.
    '''    
    lti = models.ForeignKey(LtiOriginal, primary_key=True)
    objects = removedLtisManager()
  
    class Meta:
        db_table = u'offliner_removed_ltis'
        app_label = 'offliner'

    def __unicode__(self):
        return self.lti.lti_id

        
class EpicPerson(Model):
    '''
    EpicPerson: Class that models a Person.
    This data are managed by Compas.
    '''    
    person_pk = models.CharField(max_length=20, blank=True, primary_key=True)
    org_unit_code = models.CharField(max_length=13)
    code = models.CharField(max_length=7)
    type_of_document = models.CharField(max_length=2, blank=True)
    organization_id = models.CharField(max_length=12)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=25)
    title = models.CharField(max_length=50, blank=True)
    document_number = models.CharField(max_length=25, blank=True)
    e_mail_address = models.CharField(max_length=100, blank=True)
    mobile_phone_number = models.CharField(max_length=20, blank=True)
    official_tel_number = models.CharField(max_length=20, blank=True)
    fax_number = models.CharField(max_length=20, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location_code = models.CharField(max_length=10)

    class Meta:
        db_table = u'epic_persons'
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.last_name + ', ' + self.first_name


class EpicStock(Model):
    '''
    EpicStock: Class that models a Stock.
    This data are managed by Compas.
    '''     
    wh_pk = models.CharField(max_length=90, blank=True, primary_key=True)
    wh_regional = models.CharField(max_length=4, blank=True)
    wh_country = models.CharField(max_length=15)
    wh_location = models.CharField(max_length=30)
    wh_code = models.CharField(max_length=13)
    wh_name = models.CharField(max_length=50, blank=True)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    si_record_id = models.CharField(max_length=25)
    si_code = models.CharField(max_length=8)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    cmmname = models.CharField(max_length=100, blank=True)
    package_code = models.CharField(max_length=17)
    packagename = models.CharField(max_length=50, blank=True)
    qualitycode = models.CharField(max_length=1)
    qualitydescr = models.CharField(max_length=11, blank=True)
    quantity_net = models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
    quantity_gross = models.DecimalField(null=True, max_digits=12, decimal_places=3, blank=True)
    number_of_units = models.IntegerField()
    allocation_code = models.CharField(max_length=10)
    reference_number = models.CharField(max_length=50)

    class Meta:
        db_table = u'epic_stock'
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.wh_name + '\t' + self.cmmname + '\t' + str(self.number_of_units)
    
    def packagingDescrShort(self):
        pck = PackagingDescriptonShort.objects.get(pk=self.package_code)
        return pck.packageShortName
           
            
class EpicLossReason(Model):
    '''
    EpicLossReason: Class that models a loss reason.
    This data are managed by Compas.
    '''     
    reason_code = models.CharField(max_length=5, primary_key=True)
    reason = models.CharField(max_length=80)
    
    class Meta:
        db_table = u'epic_lossreason'
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.reason        


class LossesDamagesReason(Model):
    '''
    LossesDamagesReason: Class that models a loss damage reason.
    This data are managed by Compas.
    '''
    compasRC = models.ForeignKey(EpicLossReason)
    compasCode = models.CharField(max_length=20)
    description = models.CharField(max_length=80)

    class Meta:
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.compasRC.reason
      
        
class LossesDamagesType(Model):
    '''
    LossesDamagesReason: Class that models a loss damages type.
    This data are managed by Compas.
    '''    
    description = models.CharField(max_length=20)
    
    class Meta:
        app_label = 'offliner'    
    
    def __unicode__(self):
        return self.description


class LoadingDetail(Model):
    '''
    LodigDeatil: Class that models a loading detail.
    This data are managed by ETS. 
    '''    
    wbNumber = models.ForeignKey(Waybill)
    siNo = models.ForeignKey(LtiOriginal)
    numberUnitsLoaded = models.DecimalField(default=0, blank=True, null=True, max_digits=10, decimal_places=3)
    numberUnitsGood = models.DecimalField(default=0, blank=True, null=True, max_digits=10, decimal_places=3)
    numberUnitsLost = models.DecimalField(default=0, blank=True, null=True, max_digits=10, decimal_places=3)
    numberUnitsDamaged = models.DecimalField(default=0, blank=True, null=True, max_digits=10, decimal_places=3)
    unitsLostReason = models.ForeignKey(LossesDamagesReason, related_name='LD_LostReason', blank=True, null=True)
    unitsDamagedReason = models.ForeignKey(LossesDamagesReason, related_name='LD_DamagedReason', blank=True, null=True)
    unitsDamagedType = models.ForeignKey(LossesDamagesType, related_name='LD_DamagedType', blank=True, null=True)
    unitsLostType = models.ForeignKey(LossesDamagesType, related_name='LD_LossType', blank=True, null=True)
    overloadedUnits = models.BooleanField()
    loadingDetailSentToCompas = models.BooleanField()
    overOffloadUnits = models.BooleanField()
    
    audit_log = AuditLog()
    
    class Meta:
        app_label = 'offliner'    
    
    def check_stock(self):
        thisStock = EpicStock.objects.filter(si_code=self.siNo.si_code).filter(wh_code=self.siNo.origin_wh_code)
        #Am i in stock? # fix for bulk...
        if self.siNo.isBulk():
            return self.numberUnitsLoaded <= thisStock[0].quantity_net
        else:
            return self.numberUnitsLoaded <= thisStock[0].number_of_units
         
    def check_reciept_item(self):
        totalUnitsOffloaded = self.numberUnitsGood + self.numberUnitsDamaged + self.numberUnitsLost
        
        return totalUnitsOffloaded <= self.numberUnitsLoaded
    
    def getStockItem(self):
        try:
            stockItem = EpicStock.objects.filter(si_code=self.siNo.si_code).filter(commodity_code=self.siNo.commodity_code)
            return stockItem[0]
        except:
            try:
                stockItem = EpicStock.objects.filter(si_code=self.siNo.si_code).filter(comm_category_code=self.siNo.comm_category_code)
                return stockItem[0]
            except:
                return 'N/A'
    
    def calcTotalNet(self):
        totalNet = (self.numberUnitsLoaded * self.siNo.unit_weight_net) / 1000
        return totalNet
        
    def calcTotalGross(self):
        totalGross = (self.numberUnitsLoaded * self.siNo.unit_weight_gross) / 1000
        return totalGross
            
    def calcNetRecievedGood(self):
        totalNet = (self.numberUnitsGood * self.siNo.unit_weight_net) / 1000
        return totalNet
        
    def calcGrossRecievedGood(self):
        totalGross = (self.numberUnitsGood * self.siNo.unit_weight_gross) / 1000
        return totalGross
    
    def calcNetRecievedDamaged(self):
        totalNet = (self.numberUnitsDamaged * self.siNo.unit_weight_net) / 1000
        return totalNet
        
    def calcGrossRecievedDamaged(self):
        totalGross = (self.numberUnitsDamaged * self.siNo.unit_weight_gross) / 1000
        return totalGross
    
    def calcNetRecievedLost(self):
        totalNet = (self.numberUnitsLost * self.siNo.unit_weight_net) / 1000
        return totalNet
        
    def calcGrossRecievedLost(self):
        totalGross = (self.numberUnitsLost * self.siNo.unit_weight_gross) / 1000
        return totalGross
        
    def calcTotalReceivedUnits(self):
        total = self.numberUnitsGood + self.numberUnitsDamaged 
        return total
        
    def calcTotalReceivedNet(self):
        total = self.calcNetRecievedGood() + self.calcNetRecievedDamaged() 
        return total
    
    def __unicode__(self):
        return self.wbNumber.mydesc() + ' - ' + self.siNo.mydesc() + ' - ' + self.siNo.lti_pk


class DispatchPoint(Model):
    '''
    DispatchPoint: Class that models a dispatch point.
    This data are managed by Compas.
    '''    
    origin_loc_name = models.CharField(max_length=20, blank=True, db_column='ORIGIN_LOC_NAME')
    origin_location_code = models.CharField(max_length=20, blank=True, db_column='ORIGIN_LOCATION_CODE')
    origin_wh_code = models.CharField(max_length=20, blank=True, db_column='ORIGIN_WH_CODE')
    origin_wh_name = models.CharField(max_length=30, blank=True, db_column='ORIGIN_WH_NAME')
    desc_name = models.CharField(max_length=20, blank=True, null=True, db_column='DESC_NAME')
    active_start_date = models.DateField(null=True, blank=True, db_column='ACTIVE_START_DATE')
 
    class Meta:
        app_label = 'offliner' 
       
    def __unicode__(self):
        return self.origin_wh_code + ' - ' + self.origin_loc_name
        
        
class ReceptionPoint(Model):
    '''
    ReceptionPoint: Class that models a reception point.
    This data are managed by Compas.
    '''     
    loc_name = models.CharField(max_length=20, blank=True, db_column='LOC_NAME')
    location_code = models.CharField(max_length=20, blank=True, db_column='LOCATION_CODE')
    consegnee_code = models.CharField(max_length=20, blank=True, db_column='CONSEGNEE_CODE')
    consegnee_name = models.CharField(max_length=80, blank=True, db_column='CONSEGNEE_NAME')
    #DESC_NAME                = models.CharField(max_length=80, blank=True)
    active_start_date = models.DateField(null=True, blank=True, db_column='ACTIVE_START_DATE')
    
    def __unicode__(self):
        return self.loc_name + ' ' + self.consegnee_code + ' - ' + self.consegnee_name
    
    class Meta:
        ordering = ['loc_name', 'consegnee_name']
        app_label = 'offliner'

        
class UserProfile(Model):
    '''
    UserProfile: Class that models a user profile.
    This data are managed by ETS.
    '''     
    user = models.ForeignKey(User, unique=True, primary_key=True)#OneToOneField(User, primary_key=True)
    warehouses = models.ForeignKey(DispatchPoint, blank=True, null=True)
    receptionPoints = models.ForeignKey(ReceptionPoint, blank=True, null=True)
    isCompasUser = models.BooleanField()
    isDispatcher = models.BooleanField()
    isReciever = models.BooleanField()
    compasUser = models.ForeignKey(EpicPerson, blank=True, null=True)
    superUser = models.BooleanField()
    readerUser = models.BooleanField()
    audit_log = AuditLog()  
    
    class Meta:
        app_label = 'offliner'    
          
    def __unicode__(self):
        return "%s's profile" % self.user 


User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

                       
#class SiTracker(Model):
#    '''
#    SiTracker: #@todo: write Class definition
#    '''
#    lti = models.OneToOneField(LtiOriginal, primary_key=True, db_column='LTI')
#    number_units_left = models.DecimalField(decimal_places=3, max_digits=10)
#    number_units_start = models.DecimalField(decimal_places=3, max_digits=10)
#
#    class Meta:
#        app_label = 'offliner'
#
#    def updateUnits(self, ammount):
#        self.number_units_left -= ammount
#        self.save()
#
#    def updateUnitsRestore(self, ammount):
#        self.number_units_left += ammount
#        self.save()
#
#    def  __unicode__(self):
#        return self.number_units_left


class PackagingDescriptonShort(Model):
    '''
    PackagingDescriptonShort: Class that models a short packaging description.
    '''     
    packageCode = models.CharField(primary_key=True, max_length=5)
    packageShortName = models.CharField(max_length=10)

    class Meta:
        app_label = 'offliner'
    
    def __unicode__(self):
        return self.packageCode + ' - ' + self.packageShortName

                        
class loggerCompas(Model):
    '''
    loggerCompas: Class that models a logger of Compass.
    '''     
    timestamp = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User)
    action = models.CharField(max_length=50, blank=True)
    errorRec = models.CharField(max_length=2000, blank=True)
    errorDisp = models.CharField(max_length=2000, blank=True)
    wb = models.ForeignKey(Waybill, blank=True, primary_key=True)
    lti = models.CharField(max_length=50, blank=True)
    data_in = models.CharField(max_length=5000, blank=True)
    data_out = models.CharField(max_length=5000, blank=True)

    class Meta:
        app_label = 'offliner'
        
    
class SIWithRestant:
    '''
    SIWithRestant: #@todo: write Class definition
    '''     
    SINumber = ''
    StartAmount = 0.0
    CurrentAmount = 0.0
    CommodityName = ''
    
    def __init__(self, SINumber, StartAmount, CommodityName):
        self.SINumber = SINumber
        self.StartAmount = StartAmount
        self.CurrentAmount = StartAmount
        self.CommodityName = CommodityName
    
    def reduceCurrent(self, reduce):
        self.CurrentAmount = self.CurrentAmount - reduce
        
    def getCurrentAmount(self):   
        return self.CurrentAmount
    
    def getStartAmount(self):
        return self.StartAmount


import observers