
import datetime
import zlib, base64, string

from django.db import models, connection
from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.db.models import Sum
from django.core import serializers
from django.forms.models import model_to_dict
from django.conf import settings
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from django.template.defaultfilters import stringfilter
from audit_log.models.fields import LastUserField
from audit_log.models.managers import AuditLog

name = "1234"

# Create your models here.
class Places( models.Model ):
    org_code = models.CharField( max_length = 7, primary_key = True )
    name = models.CharField( max_length = 100 )
    geo_point_code = models.CharField( max_length = 4 )
    geo_name = models.CharField( max_length = 100 )
    country_code = models.CharField( max_length = 3 )
    reporting_code = models.CharField( max_length = 7 )
    organization_id = models.CharField( max_length = 20 )

    def __unicode__( self ):
        return self.name

    class Meta:
        db_table = u'epic_geo'

    @classmethod
    def update(cls):
        """
        Executes Imports of Places
        """
        #TODO: omit try...except
        for country in settings.COUNTRIES:
            try:
                for the_geo in cls.objects.using( 'compas' ).filter( COUNTRY_CODE = country ):
                    the_geo.save( using = 'default' )
            except:
                pass
        return True
    
    

"""
Models based on compas Views & Tables
"""
"""
LTIs for office 
"""
class LtiOriginal( models.Model ):
    lti_pk = models.CharField( max_length = 50, primary_key = True, db_column = 'LTI_PK' )
    lti_id = models.CharField( max_length = 40, db_column = 'LTI_ID' )
    code = models.CharField( max_length = 40, db_column = 'CODE' )
    lti_date = models.DateField( db_column = 'LTI_DATE' )
    expiry_date = models.DateField( blank = True, null = True, db_column = 'EXPIRY_DATE' )
    transport_code = models.CharField( max_length = 4, db_column = 'TRANSPORT_CODE' )
    transport_ouc = models.CharField( max_length = 13, db_column = 'TRANSPORT_OUC' )
    transport_name = models.CharField( max_length = 30, db_column = 'TRANSPORT_NAME' )
    origin_type = models.CharField( max_length = 1, db_column = 'ORIGIN_TYPE' )
    origintype_desc = models.CharField( max_length = 12, blank = True, db_column = 'ORIGINTYPE_DESC' )
    origin_location_code = models.CharField( max_length = 10, db_column = 'ORIGIN_LOCATION_CODE' )
    origin_loc_name = models.CharField( max_length = 30, db_column = 'ORIGIN_LOC_NAME' )
    origin_wh_code = models.CharField( max_length = 13, blank = True, db_column = 'ORIGIN_WH_CODE' )
    origin_wh_name = models.CharField( max_length = 50, blank = True, db_column = 'ORIGIN_WH_NAME' )
    destination_location_code = models.CharField( max_length = 10, db_column = 'DESTINATION_LOCATION_CODE' )
    destination_loc_name = models.CharField( max_length = 30, db_column = 'DESTINATION_LOC_NAME' )
    consegnee_code = models.CharField( max_length = 12, db_column = 'CONSEGNEE_CODE' )
    consegnee_name = models.CharField( max_length = 80, db_column = 'CONSEGNEE_NAME' )
    requested_dispatch_date = models.DateField( blank = True, null = True, db_column = 'REQUESTED_DISPATCH_DATE' )
    project_wbs_element = models.CharField( max_length = 24, blank = True, db_column = 'PROJECT_WBS_ELEMENT' )
    si_record_id = models.CharField( max_length = 25, blank = True, db_column = 'SI_RECORD_ID' )
    si_code = models.CharField( max_length = 8, db_column = 'SI_CODE' )
    comm_category_code = models.CharField( max_length = 9, db_column = 'COMM_CATEGORY_CODE' )
    commodity_code = models.CharField( max_length = 18, db_column = 'COMMODITY_CODE' )
    cmmname = models.CharField( max_length = 100, blank = True, db_column = 'CMMNAME' )
    quantity_net = models.DecimalField( max_digits = 11, decimal_places = 3, db_column = 'QUANTITY_NET' )
    quantity_gross = models.DecimalField( max_digits = 11, decimal_places = 3, db_column = 'QUANTITY_GROSS' )
    number_of_units = models.DecimalField( max_digits = 7, decimal_places = 0, db_column = 'NUMBER_OF_UNITS' )
    unit_weight_net = models.DecimalField( max_digits = 8, decimal_places = 3, blank = True, null = True, db_column = 'UNIT_WEIGHT_NET' )
    unit_weight_gross = models.DecimalField( max_digits = 8, decimal_places = 3, blank = True, null = True, db_column = 'UNIT_WEIGHT_GROSS' )

    #objects = models.Manager()

    class Meta:
        db_table = u'epic_lti'

    def  __unicode__( self ):
        if self.valid():
            return u"%s -  %.0f " % ( self.cmmname, self.items_left )
        else:
            return u"Void %s -  %.0f " % ( self.cmmname, self.items_left )

    def mydesc( self ):
        return self.code

    def commodity( self ):
        return self.cmmname

    def valid( self ):
        return RemovedLtis.objects.filter( lti = self.lti_pk ).count() == 0 

    @property
    def items_left( self ):
        order_item = LtiWithStock.objects.filter( lti_line = self )
        used = 0
        for lines in order_item:
            wblines = LoadingDetail.objects.filter( order_item = lines )
            for line in wblines:
                if line.invalid == False and line.wbNumber.dispatcherSigned == True:
                    used += line.numberUnitsLoaded
        
        if self.is_bulk:
            return self.quantity_net - used
        else:
            return self.number_of_units - used

    def stock_items( self ):
        return EpicStock.objects.filter( wh_code = self.origin_wh_code, 
                                         si_code = self.si_code, 
                                         commodity_code = self.commodity_code 
                                         ).order_by( '-number_of_units' )

    def reduce_si( self, units ):
        self.sitracker.update_units( units )
        return self.items_left

    def restore_si( self, units ):
        self.sitracker.update_units_restore( units )
        return self.items_left()

    def packaging( self ):
        pack = 'Unknown'
        try:
            mypkg = self.stock_items()
            pack = str( mypkg[0].packagename )
        except:
            pass
        return pack

    @property
    def is_bulk( self ):
        return self.packaging() == 'BULK'

    def coi_code( self ):
        stock_items_qs = self.stock_items()
        if stock_items_qs.count() > 0:
            return str( stock_items_qs[0].coi_code() )
        else:
            stock_items_qs = EpicStock.objects.filter( wh_code = self.origin_wh_code, 
                                                       si_code = self.si_code, 
                                                       comm_category_code = self.comm_category_code 
                                                       ).order_by( '-number_of_units' )
            if stock_items_qs.count() > 0:
                return str( stock_items_qs[0].coi_code() )
            else:
                stock_items_qs = EpicStock.objects.filter( si_code = self.si_code, 
                                                           comm_category_code = self.comm_category_code 
                                                           ).order_by( '-number_of_units' )
                if stock_items_qs.count() > 0:
                    return str( stock_items_qs[0].coi_code() )
                else:
                    return 'No Stock '

    #===================================================================================================================
    # def related_stock( self ):
    #    return EpicStock.objects.filter( wh_code = self.origin_wh_code, 
    #                                     si_code = self.si_code, 
    #                                     commodity_code = self.commodity_code 
    #                                     ).order_by( '-number_of_units' )
    #===================================================================================================================

    def remove_lti( self ):
        all_removed = RemovedLtis.objects.all()
        this_lti = RemovedLtis()
        this_lti.lti = self
        if this_lti not in all_removed:
            this_lti.save()

    #===================================================================================================================
    # def get_stocks( self ):
    #    return EpicStock.objects.filter( wh_code = self.origin_wh_code, 
    #                                     si_code = self.si_code, 
    #                                     commodity_code = self.commodity_code )
    #===================================================================================================================

    @property
    def total_stock( self ):
        return self.stock_items().aggregate(units_count=Sum('number_of_units'))['units_count']
    
    

#=======================================================================================================================
# class RemovedLtisManager( models.Manager ):
#        def list( self ):
#            listExl = []
#            listOfExcluded = RemovedLtis.objects.all()
#            for exl in listOfExcluded:
#                listExl += [exl.lti.lti_pk]
#            return listExl
#=======================================================================================================================

class RemovedLtis( models.Model ):
    lti = models.ForeignKey( LtiOriginal, primary_key = True )
    #objects = RemovedLtisManager()
    
    class Meta:
        db_table = u'waybill_removed_ltis'
    
    def  __unicode__( self ):
        return self.lti.lti_id

class EpicPerson( models.Model ):
    person_pk = models.CharField( max_length = 20, blank = True, primary_key = True )
    org_unit_code = models.CharField( max_length = 13 )
    code = models.CharField( max_length = 7 )
    type_of_document = models.CharField( max_length = 2, blank = True )
    organization_id = models.CharField( max_length = 12 )
    last_name = models.CharField( max_length = 30 )
    first_name = models.CharField( max_length = 25 )
    title = models.CharField( max_length = 50, blank = True )
    document_number = models.CharField( max_length = 25, blank = True )
    e_mail_address = models.CharField( max_length = 100, blank = True )
    mobile_phone_number = models.CharField( max_length = 20, blank = True )
    official_tel_number = models.CharField( max_length = 20, blank = True )
    fax_number = models.CharField( max_length = 20, blank = True )
    effective_date = models.DateField( null = True, blank = True )
    expiry_date = models.DateField( null = True, blank = True )
    location_code = models.CharField( max_length = 10 )

    class Meta:
        db_table = u'epic_persons'
        verbose_name = 'COMPAS User'

    def  __unicode__( self ):
        return "%s, %s" % (self.last_name, self.first_name)
    
    @classmethod
    def update(cls):
        """
        Executes Imports of LTIs Persons
        """
    
        for my_person in cls.objects.using( 'compas' ).filter( org_unit_code = settings.COMPAS_STATION ):
            my_person.save( using = 'default' )

class StockManager( models.Manager ):
    
    def get_query_set( self ):
        return super( StockManager, self ).get_query_set().filter( number_of_units__gt = 0 )

class EpicStock( models.Model ):
    wh_pk = models.CharField( max_length = 90, blank = True, primary_key = True )
    wh_regional = models.CharField( max_length = 4, blank = True )
    wh_country = models.CharField( max_length = 15 )
    wh_location = models.CharField( max_length = 30 )
    wh_code = models.CharField( max_length = 13 )
    wh_name = models.CharField( max_length = 50, blank = True )
    project_wbs_element = models.CharField( max_length = 24, blank = True )
    si_record_id = models.CharField( max_length = 25 )
    si_code = models.CharField( max_length = 8 )
    origin_id = models.CharField( max_length = 23 )
    comm_category_code = models.CharField( max_length = 9 )
    commodity_code = models.CharField( max_length = 18 )
    cmmname = models.CharField( max_length = 100, blank = True )
    package_code = models.CharField( max_length = 17 )
    packagename = models.CharField( max_length = 50, blank = True )
    qualitycode = models.CharField( max_length = 1 )
    qualitydescr = models.CharField( max_length = 11, blank = True )
    quantity_net = models.DecimalField( null = True, max_digits = 12, decimal_places = 3, blank = True )
    quantity_gross = models.DecimalField( null = True, max_digits = 12, decimal_places = 3, blank = True )
    number_of_units = models.IntegerField()
    allocation_code = models.CharField( max_length = 10 )
    reference_number = models.CharField( max_length = 50 )
    
    objects = models.Manager()
    in_stock_objects = StockManager()

    class Meta:
        db_table = u'epic_stock'

    def  __unicode__( self ):
        return "%s\t%s\t%s\t%s" % (self.wh_name, self.cmmname, self.number_of_units, self.coi_code())

    def packaging_description_short( self ):
        try:
            return PackagingDescriptionShort.objects.get( pk = self.package_code ).packageShortName
        except:
            return self.packagename
        
    def coi_code( self ):
        return self.origin_id[7:]
    
    @classmethod    
    def update():
        """
        Executes Imports of Stock
        """
        originalStock = EpicStock.objects.using( 'compas' )
        for myrecord in originalStock:
            myrecord.save( using = 'default' )
            
        EpicStock.objects.exclude(pk__in=originalStock.values_list('pk', flat=True))\
                         .update(number_of_units=0)


class EpicLossDamages( models.Model ):
    type = models.CharField( max_length = 1 )
    comm_category_code = models.CharField( max_length = 9 )
    cause = models.CharField( max_length = 100 )

    class Meta:
        db_table = u'epic_lossdamagereason'
        verbose_name = 'Loss/Damages Reason'
    
    def  __unicode__( self ):
        cause = self.cause
        length_c = len( cause ) - 10
        if length_c > 20:
            cause = "%s...%s" % (cause[0:20], cause[length_c:])
        return cause


class LtiWithStock( models.Model ):
    lti_line = models.ForeignKey( LtiOriginal )
    stock_item = models.ForeignKey( EpicStock )
    lti_code = models.CharField( max_length = 20, db_index = True )
    
    def  __unicode__( self ):
        item_name = u"%s - %s (%s)" % (self.coi_code(), self.stock_item.cmmname, self.lti_line.items_left)
        return self.lti_line.valid() and item_name or 'Void %s' % item_name

    def coi_code( self ):
        return self.stock_item.coi_code()

class SiTracker( models.Model ):
    LTI = models.OneToOneField( LtiOriginal, primary_key = True )
    number_units_left = models.DecimalField( decimal_places = 3, max_digits = 10 )
    number_units_start = models.DecimalField( decimal_places = 3, max_digits = 10 )

    def update_units( self, ammount ):
        self.number_units_left -= ammount
        self.save()
        
    def update_units_restore( self, ammount ):
        self.number_units_left += ammount
        self.save()
        
    def  __unicode__( self ):
        return self.number_units_left

class PackagingDescriptionShort( models.Model ):
    packageCode = models.CharField( primary_key = True, max_length = 5 )
    packageShortName = models.CharField( max_length = 10 )
    
    def  __unicode__( self ):
        return "%s - %s" % (self.packageCode, self.packageShortName)


class CompasLogger( models.Model ):
    timestamp = models.DateTimeField( null = True, blank = True )
    user = models.ForeignKey( User )
    action = models.CharField( max_length = 50, blank = True )
    errorRec = models.CharField( max_length = 2000, blank = True )
    errorDisp = models.CharField( max_length = 2000, blank = True )
    wb = models.ForeignKey( Waybill, blank = True, primary_key = True )
    lti = models.CharField( max_length = 50, blank = True )
    data_in = models.CharField( max_length = 5000, blank = True )
    data_out = models.CharField( max_length = 5000, blank = True )
    #loggercompas
    
    class Meta:
        db_table = u'loggercompas'

class SIWithRestant:
    SINumber = ''
    StartAmount = 0.0
    CurrentAmount = 0.0
    CommodityName = ''
    InStock = 0
    COI_Code = ''

    def __init__( self, SINumber, StartAmount, CommodityName ):
        self.SINumber = SINumber
        self.StartAmount = StartAmount
        self.CurrentAmount = StartAmount
        self.CommodityName = CommodityName

    def reduce_current( self, reduce ):
        self.CurrentAmount = self.CurrentAmount - reduce
        
    def get_current_amount( self ):
        return self.CurrentAmount
    
    def get_start_amount( self ):
        return self.StartAmount


# TODO: Importing of old waybills....
class DispatchMaster( models.Model ):
    code = models.CharField( max_length = 25, primary_key = True )
    document_code = models.CharField( max_length = 2 )
    dispatch_date = models.DateField()
    origin_type = models.CharField( max_length = 1 )
    origin_location_code = models.CharField( max_length = 13 )
    intvyg_code = models.CharField( max_length = 25, blank = True )
    intdlv_code = models.IntegerField( null = True, blank = True )
    origin_code = models.CharField( max_length = 13, blank = True )
    origin_descr = models.CharField( max_length = 50, blank = True )
    destination_location_code = models.CharField( max_length = 10 )
    destination_code = models.CharField( max_length = 13, blank = True )
    pro_activity_code = models.CharField( max_length = 6, blank = True )
    activity_ouc = models.CharField( max_length = 13, blank = True )
    lndarrm_code = models.CharField( max_length = 25, blank = True )
    lti_id = models.CharField( max_length = 25, blank = True )
    loan_id = models.CharField( max_length = 25, blank = True )
    loading_date = models.DateField()
    organization_id = models.CharField( max_length = 12 )
    tran_type_code = models.CharField( max_length = 4 )
    tran_type_descr = models.CharField( max_length = 50, blank = True )
    modetrans_code = models.CharField( max_length = 2 )
    comments = models.CharField( max_length = 250, blank = True )
    person_code = models.CharField( max_length = 7 )
    person_ouc = models.CharField( max_length = 13 )
    certifing_title = models.CharField( max_length = 50, blank = True )
    trans_contractor_code = models.CharField( max_length = 4 )
    supplier1_ouc = models.CharField( max_length = 13 )
    trans_subcontractor_code = models.CharField( max_length = 4, blank = True )
    supplier2_ouc = models.CharField( max_length = 13, blank = True )
    nmbplt_id = models.CharField( max_length = 25, blank = True )
    nmbtrl_id = models.CharField( max_length = 25, blank = True )
    driver_name = models.CharField( max_length = 50, blank = True )
    license = models.CharField( max_length = 20, blank = True )
    vehicle_registration = models.CharField( max_length = 20, blank = True )
    trailer_plate = models.CharField( max_length = 20, blank = True )
    container_number = models.CharField( max_length = 15, blank = True )
    atl_li_code = models.CharField( max_length = 8, blank = True )
    notify_indicator = models.CharField( max_length = 1, blank = True )
    customised = models.CharField( max_length = 50, blank = True )
    org_unit_code = models.CharField( max_length = 13 )
    printed_indicator = models.CharField( max_length = 1, blank = True )
    notify_org_unit_code = models.CharField( max_length = 13, blank = True )
    offid = models.CharField( max_length = 13, blank = True )
    send_pack = models.BigIntegerField( null = True, blank = True )
    recv_pack = models.BigIntegerField( null = True, blank = True )
    last_mod_user = models.CharField( max_length = 30, blank = True )
    last_mod_date = models.DateField( null = True, blank = True )
    
    class Meta:
        db_table = u'dispatch_masters'
    
    def  __unicode__( self ):
        return self.code


class DispatchDetail( models.Model ):
    code = models.ForeignKey( DispatchMaster )
    document_code = models.CharField( max_length = 2 )
    si_record_id = models.CharField( max_length = 25, blank = True, null = True )
    origin_id = models.CharField( max_length = 23, blank = True )
    comm_category_code = models.CharField( max_length = 9 )
    commodity_code = models.CharField( max_length = 18 )
    package_code = models.CharField( max_length = 17 )
    allocation_destination_code = models.CharField( max_length = 10 )
    quality = models.CharField( max_length = 1 )
    quantity_net = models.DecimalField( max_digits = 11, decimal_places = 3 )
    quantity_gross = models.DecimalField( max_digits = 11, decimal_places = 3 )
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField( null = True, max_digits = 8, decimal_places = 3, blank = True )
    unit_weight_gross = models.DecimalField( null = True, max_digits = 8, decimal_places = 3, blank = True )
    lonmst_id = models.CharField( max_length = 25, blank = True )
    londtl_id = models.IntegerField( null = True, blank = True )
    rpydtl_id = models.IntegerField( null = True, blank = True )
    offid = models.CharField( max_length = 13, blank = True )
    send_pack = models.BigIntegerField( null = True, blank = True )
    recv_pack = models.BigIntegerField( null = True, blank = True )
    last_mod_user = models.CharField( max_length = 30, blank = True )
    last_mod_date = models.DateField( null = True, blank = True )
    
    class Meta:
        db_table = u'dispatch_details'


