
from django.db import models
from django.utils.translation import ugettext_lazy as _

#name = "1234"
BULK_NAME = "BULK"

#=======================================================================================================================
# Models based on compas Views & Tables
#=======================================================================================================================

class Partner(models.Model):
    """Partner organization"""
    id = models.CharField(max_length=100, primary_key=True) 
    name = models.CharField(_("Name"), max_length=100)
    
    class Meta:
        db_table = 'organizations'
        verbose_name=_("partner")
        verbose_name_plural = _("partners")
    

class Place( models.Model ):
    """
    Location model.
    Model based on compas Views & Tables
    """

    org_code = models.CharField(_("Org code"), max_length = 7, primary_key = True )
    name = models.CharField(_("Name"), max_length = 100 )
    geo_point_code = models.CharField(_("Geo point code"), max_length = 4 )
    geo_name = models.CharField(_("Geo name"), max_length = 100 )
    country_code = models.CharField( _("Country code"), max_length = 3 )
    reporting_code = models.CharField(_("COMPAS station code"), max_length = 7 )
    organization_id = models.CharField( _("Organization id"), max_length = 20, blank=True )

    class Meta:
        db_table = u'epic_geo'
        ordering = ('name',)
        verbose_name=_("place")
        verbose_name_plural = _("places")

    def __unicode__( self ):
        return self.name


class CompasPerson( models.Model ):
    """Compas CompasPerson. We import them directly from compas Oracle using database view"""
    person_pk = models.CharField(_("person identifier"), max_length=20, blank=True, primary_key=True)
    title = models.CharField(_("title"), max_length=50, blank=True)
    last_name = models.CharField(_("last name"), max_length=30)
    first_name = models.CharField(_("first name"), max_length=25)
    code = models.CharField(_("code"), max_length=7)
    #type_of_document = models.CharField(_("type of document"), max_length=2, blank=True)
    #document_number = models.CharField(_("document number"), max_length=25, blank=True)
    email = models.CharField(_("e_mail address"), max_length=100, blank=True, db_column='e_mail_address')
    #mobile_phone_number = models.CharField(_("cell phone number"), max_length=20, blank=True)
    #official_tel_number = models.CharField(_("official telephone number"), max_length=20, blank=True)
    #fax_number = models.CharField(_("fax_number"), max_length=20, blank=True)
    #effective_date = models.DateField(_("effective date"), null=True, blank=True)
    #expiry_date = models.DateField(_("expiry date "), null=True, blank=True)
    
    org_unit_code = models.CharField(_("compas station"), max_length=10)
    organization_id = models.CharField(_("organization identifier"), max_length=12)
    location_code = models.CharField(_("location"), max_length=12)

    class Meta:
        db_table = u'epic_persons'
    
    def  __unicode__( self ):
        return "%s, %s" % (self.last_name, self.first_name)
  
    
class EpicStock( models.Model ):
    """COMPAS stock. We retrieve it from Oracle database view."""
    
    wh_pk = models.CharField(_("warehouse primary key"), max_length = 90, blank = True, primary_key = True)
    wh_regional = models.CharField(_("warehouse regional"), max_length = 4, blank = True )
    wh_country = models.CharField(_("warehouse country"), max_length = 15 )
    wh_location = models.CharField(_("warehouse location"), max_length = 30 )
    wh_code = models.CharField(_("warehouse code"), max_length = 13 )
    wh_name = models.CharField(_("warehouse name"), max_length = 50, blank = True )
    
    project_wbs_element = models.CharField(_("Project wbs element"), max_length = 24, blank = True )
    si_record_id = models.CharField(_("SI record id "), max_length = 25 )
    si_code = models.CharField(_("SI code"), max_length = 8 )
    origin_id = models.CharField(_("Origin id"), max_length = 23 )
    
    comm_category_code = models.CharField(_("commodity category code"), max_length = 9 )
    commodity_code = models.CharField(_("commodity code "), max_length = 18 )
    cmmname = models.CharField(_("commodity name"), max_length = 100, blank = True )
    
    package_code = models.CharField(_("Package code"), max_length = 17 )
    packagename = models.CharField(_("Package name"), max_length = 50, blank = True )
    
    qualitycode = models.CharField(_("Quality code"), max_length = 1 )
    qualitydescr = models.CharField(_("Quality descr "), max_length = 11, blank = True )
    quantity_net = models.DecimalField(_("Quantity net"), max_digits = 12, decimal_places = 3, blank = True, null=True)
    quantity_gross = models.DecimalField(_("Quantity gross"), null = True, max_digits = 12, decimal_places = 3, blank = True )
    number_of_units = models.DecimalField(_("Number of units"), max_digits=12, decimal_places=3)
    
    allocation_code = models.CharField(_("Allocation code"), max_length = 10 )
    reference_number = models.CharField( _("Reference number"),max_length = 50 )
    
    class Meta:
        db_table = u'epic_stock'
        #managed = False
    
    def is_bulk(self):
        return self.packagename == BULK_NAME and self.quantity_net
    
 
class LtiOriginal( models.Model ):
    """LTIs for office"""
    
    lti_pk = models.CharField( _("LTI primary key"),max_length = 50, primary_key = True, db_column = 'LTI_PK' )
    lti_id = models.CharField(_("LTI ID"), max_length = 40, db_column = 'LTI_ID' )
    code = models.CharField( _("Code"),max_length = 40, db_column = 'CODE' )
    lti_date = models.DateField( _("LTI Date"),db_column = 'LTI_DATE' )
    expiry_date = models.DateField(_("Expiry Date"), blank = True, null = True, db_column = 'EXPIRY_DATE' )
    transport_code = models.CharField(_("Transport Code"), max_length = 4, db_column = 'TRANSPORT_CODE' )
    transport_ouc = models.CharField(_("Transport ouc"), max_length = 13, db_column = 'TRANSPORT_OUC' )
    transport_name = models.CharField(_("Transport Name"), max_length = 30, db_column = 'TRANSPORT_NAME' )
    origin_type = models.CharField(_("Origin Type"), max_length = 1, db_column = 'ORIGIN_TYPE' )
    origintype_desc = models.CharField(_("Origin Type Desc"), max_length = 12, blank = True, db_column = 'ORIGINTYPE_DESC' )
    
    #Warehouse
    origin_location_code = models.CharField( _("Origin location code"),max_length = 10, db_column = 'ORIGIN_LOCATION_CODE' )
    origin_loc_name = models.CharField(_("Origin location name"), max_length = 30, db_column = 'ORIGIN_LOC_NAME' )
    origin_wh_code = models.CharField( _("Origin warehouse code"),max_length = 13, blank = True, db_column = 'ORIGIN_WH_CODE' )
    origin_wh_name = models.CharField( _("Origin warehouse name"),max_length = 50, blank = True, db_column = 'ORIGIN_WH_NAME' )
    
    #Location
    destination_location_code = models.CharField( _("Destination Location Code"),max_length = 10, db_column = 'DESTINATION_LOCATION_CODE' )
    destination_loc_name = models.CharField(_("Destination Loc Name"), max_length = 30, db_column = 'DESTINATION_LOC_NAME' )
    
    #Organization
    consegnee_code = models.CharField(_("Consignee Code"), max_length = 12, db_column = 'CONSEGNEE_CODE' )
    consegnee_name = models.CharField(_("Consignee Name"), max_length = 80, db_column = 'CONSEGNEE_NAME' )
    
    #Remarks
    #remarks = models.TextField(_("Remarks"), blank=True, db_column = 'REMARKS')
    #remarks_b = models.TextField(_("RemarksBB"), blank=True, db_column = 'REMARKS_B')
    
    requested_dispatch_date = models.DateField(_("Requested Dispatch Date"), blank = True, null = True, db_column = 'REQUESTED_DISPATCH_DATE' )
    project_wbs_element = models.CharField(_("Project work breakdown structure element"), max_length = 24, blank = True, db_column = 'PROJECT_WBS_ELEMENT' )
    si_record_id = models.CharField( _("SI Record ID "),max_length = 25, blank = True, db_column = 'SI_RECORD_ID' )
    si_code = models.CharField( _("SI Code"),max_length = 8, db_column = 'SI_CODE' )
    comm_category_code = models.CharField(_("Commodity Category Code"), max_length = 9, db_column = 'COMM_CATEGORY_CODE' )
    commodity_code = models.CharField(_("Commodity Code "), max_length = 18, db_column = 'COMMODITY_CODE' )
    cmmname = models.CharField(_("Commodity Name"), max_length = 100, blank = True, db_column = 'CMMNAME' )
    
    number_of_units = models.DecimalField( _("Number of Units"),max_digits = 12, decimal_places = 3, db_column = 'NUMBER_OF_UNITS' )
    quantity_net = models.DecimalField(_("Quantity Net"), max_digits = 11, decimal_places = 3, db_column = 'QUANTITY_NET' )
    quantity_gross = models.DecimalField( _("Quantity Gross"),max_digits = 11, decimal_places = 3, db_column = 'QUANTITY_GROSS' )
    unit_weight_net = models.DecimalField( _("Unit Weight Net"),max_digits = 8, decimal_places = 3, blank = True, null = True, db_column = 'UNIT_WEIGHT_NET' )
    unit_weight_gross = models.DecimalField( _("Unit Weight Gross"),max_digits = 8, decimal_places = 3, blank = True, null = True, db_column = 'UNIT_WEIGHT_GROSS' )

    class Meta:
        db_table = u'epic_lti'
        #managed = False


# TODO: Importing of old waybills....
class DispatchMaster( models.Model ):
    code = models.CharField(_("Code"), max_length = 25, primary_key = True )
    document_code = models.CharField(_("Document code"), max_length = 2 )
    dispatch_date = models.DateField(_("Dispatch date"))
    origin_type = models.CharField(_("Origin type"), max_length = 1 )
    origin_location_code = models.CharField(_("Origin location code"), max_length = 13 )
    intvyg_code = models.CharField(_("Intvyg code"), max_length = 25, blank = True )
    intdlv_code = models.IntegerField(_("Intdlv code"), null = True, blank = True )
    origin_code = models.CharField(_("Origin code"), max_length = 13, blank = True )
    origin_descr = models.CharField(_("Origin description"), max_length = 50, blank = True )
    destination_location_code = models.CharField(_("Destination location code"), max_length = 10 )
    destination_code = models.CharField(_("Destination code"), max_length = 13, blank = True )
    pro_activity_code = models.CharField(_("Pro activity code"), max_length = 6, blank = True )
    activity_ouc = models.CharField(_("Activity ouc"), max_length = 13, blank = True )
    lndarrm_code = models.CharField(_("Lndarrm code"), max_length = 25, blank = True )
    lti_id = models.CharField(_("LTI id "), max_length = 25, blank = True )
    loan_id = models.CharField(_("Loan id "), max_length = 25, blank = True )
    loading_date = models.DateField(_("Loading date"))
    organization_id = models.CharField(_("Organization id "), max_length = 12 )
    tran_type_code = models.CharField(_("Tran type code"), max_length = 4 )
    tran_type_descr = models.CharField(_("Tran type descr"), max_length = 50, blank = True )
    modetrans_code = models.CharField(_("Modetrans code"), max_length = 2 )
    comments = models.CharField(_("Comments"), max_length = 250, blank = True )
    person_code = models.CharField(_("Person code"), max_length = 7 )
    person_ouc = models.CharField(_("Person ouc"), max_length = 13 )
    certifing_title = models.CharField(_("Certifing title"), max_length = 50, blank = True )
    trans_contractor_code = models.CharField(_("Trans contractor code"), max_length = 4 )
    supplier1_ouc = models.CharField(_("Supplier1 ouc"), max_length = 13 )
    trans_subcontractor_code = models.CharField(_("Trans subcontractor code"), max_length = 4, blank = True )
    supplier2_ouc = models.CharField(_("Supplier2 ouc "), max_length = 13, blank = True )
    nmbplt_id = models.CharField(_("Nmbplt id"), max_length = 25, blank = True )
    nmbtrl_id = models.CharField(_("Nmbtrl id "), max_length = 25, blank = True )
    driver_name = models.CharField(_("Driver name"), max_length = 50, blank = True )
    license = models.CharField(_("license"), max_length = 20, blank = True )
    vehicle_registration = models.CharField(_("Vehicle registration"), max_length = 20, blank = True )
    trailer_plate = models.CharField(_("Trailer plate"), max_length = 20, blank = True )
    container_number = models.CharField(_("Container number"), max_length = 15, blank = True )
    atl_li_code = models.CharField(_("Atl li code"), max_length = 8, blank = True )
    notify_indicator = models.CharField(_("Notify indicator"), max_length = 1, blank = True )
    customised = models.CharField(_("Customised"), max_length = 50, blank = True )
    org_unit_code = models.CharField(_("Org unit code"), max_length = 13 )
    printed_indicator = models.CharField(_("Printed indicator"), max_length = 1, blank = True )
    notify_org_unit_code = models.CharField(_("Notify org unit code"), max_length = 13, blank = True )
    offid = models.CharField( _("Offid"), max_length = 13, blank = True )
    send_pack = models.BigIntegerField( _("Send pack"), null = True, blank = True )
    recv_pack = models.BigIntegerField( _("Recv pack"), null = True, blank = True )
    last_mod_user = models.CharField( _("Last mod user"), max_length = 30, blank = True )
    last_mod_date = models.DateField( _("Last mod date"), null = True, blank = True )
    
    class Meta:
        db_table = u'dispatch_masters'
    
    def  __unicode__( self ):
        return self.code


class DispatchDetail( models.Model ):
    code = models.ForeignKey(DispatchMaster ,verbose_name=_("Code"))
    document_code = models.CharField( _("Document code "), max_length = 2 )
    si_record_id = models.CharField( _("SI record id"), max_length = 25, blank = True, null = True )
    origin_id = models.CharField( _("Origin id"), max_length = 23, blank = True )
    comm_category_code = models.CharField( _("Commodity category code"), max_length = 9 )
    commodity_code = models.CharField( _("Commodity code"), max_length = 18 )
    package_code = models.CharField( _("Package code"), max_length = 17 )
    allocation_destination_code = models.CharField( _("Allocation destination code"), max_length = 10 )
    quality = models.CharField( _("Quality"), max_length = 1 )
    quantity_net = models.DecimalField( _("Quantity net"), max_digits = 11, decimal_places = 3 )
    quantity_gross = models.DecimalField( _("Quantity gross"), max_digits = 11, decimal_places = 3 )
    number_of_units = models.IntegerField( _("Number of units "))
    unit_weight_net = models.DecimalField( _("Unit Weight net"), null = True, max_digits = 8, decimal_places = 3, blank = True )
    unit_weight_gross = models.DecimalField( _("Unit Weight Gross"), null = True, max_digits = 8, decimal_places = 3, blank = True )
    lonmst_id = models.CharField( _("Lonmst id"), max_length = 25, blank = True )
    londtl_id = models.IntegerField( _("Londtl id"), null = True, blank = True )
    rpydtl_id = models.IntegerField( _("Rpydtl id"), null = True, blank = True )
    offid = models.CharField( _("Offid"), max_length = 13, blank = True )
    send_pack = models.BigIntegerField( _("Send pack"),null = True, blank = True )
    recv_pack = models.BigIntegerField( _("Recv pack"), null = True, blank = True )
    last_mod_user = models.CharField( _("Last mod user"),max_length = 30, blank = True )
    last_mod_date = models.DateField( _("Last modified date"), null = True, blank = True )
    
    class Meta:
        db_table = u'dispatch_details'
