
import zlib, base64, string
#from urllib import urlencode
from itertools import chain
from functools import wraps
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core import serializers
from django.conf import settings
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db import transaction

from audit_log.models.managers import AuditLog
from autoslug.fields import AutoSlugField
from autoslug.settings import slugify
import logicaldelete.models as ld_models 


from .country import COUNTRY_CHOICES

#name = "1234"
BULK_NAME = "BULK"

LETTER_CODE = getattr(settings, 'WAYBILL_LETTER', 'A')

# like a normal ForeignKey.
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^audit_log\.models\.fields\.LastUserField'])
except ImportError:
    pass

def capitalize_slug(func):
    @wraps(func)
    def wrapper(value):
        slug = func(value)
        return slug.upper()
    
    return wrapper


class Compas(models.Model):
    """ Compas station """
    
    code = models.CharField(_("Station code"), max_length=20, primary_key=True)
    officers = models.ManyToManyField(User, verbose_name=_("Officers"), related_name="compases")
    
    #Database settings
    db_engine = models.CharField(_("Database engine"), max_length=100)
    db_name = models.CharField(_("Database name"), max_length=100)
    db_user = models.CharField(_("Database user"), max_length=100, blank=True)
    db_password = models.CharField(_("Database password"), max_length=100, blank=True)
    db_host = models.CharField(_("Database host"), max_length=100, default='localhost')
    db_port = models.CharField(_("Database server port"), max_length=4, blank=True)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('Compas station')
        verbose_name_plural = _("compases")
        
    def __unicode__(self):
        return self.pk
    
class Location(models.Model):
    """Location model. City or region"""
    
    code = models.CharField(_("Geo point code"), max_length=4, primary_key=True)
    name = models.CharField(_("Name"), max_length=100)
    country = models.CharField( _("Country"), max_length=3, choices=COUNTRY_CHOICES)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('location')
        verbose_name_plural = _("locations")
    
    def __unicode__(self):
        return "%s %s" % (self.country, self.name)
    
class Organization(models.Model):
    """ Organization model"""
    
    code = models.CharField(_("code"), max_length=20, primary_key=True)
    name = models.CharField(_("Name"), max_length=100, blank=True)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('oranization')
        verbose_name_plural = _("organizations")
    
    def __unicode__(self):
        return self.name or self.code

class Warehouse(models.Model):
    """ Warehouse. dispatch or recipient."""
    code = models.CharField(_("code"), max_length = 13, primary_key=True) #origin_wh_code
    name = models.CharField(_("name"),  max_length = 50, blank = True ) #origin_wh_name
    location = models.ForeignKey(Location, verbose_name=_("location"), related_name="warehouses") #origin_location_code
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"), related_name="warehouses", 
                                     blank=True, null=True)
    compas = models.ForeignKey(Compas, verbose_name=_("COMPAS station"), related_name="warehouses")
    start_date = models.DateField(_("start date"), null=True, blank=True)
    
    
    class Meta:
        ordering = ('name',)
        order_with_respect_to = 'location'
        verbose_name = _('warehouse')
        verbose_name_plural = _("warehouses")
        
    def  __unicode__( self ):
        return "%s - %s - %s" % (self.code, self.location.name, self.name)

    @classmethod
    def get_warehouses(cls, location, organization=None):
        queryset = cls.objects.filter(location=location)
        objects = queryset.filter(organization=organization)
        if not objects.exists():
            objects = queryset.filter(organization__isnull=True)
        
        return objects
    
    @classmethod
    def filter_by_user(cls, user):
        return cls.objects.filter(location__persons__user=user, organization__persons__user=user,\
                                  compas__persons__user=user)

    
    #===================================================================================================================
    # def serialize(self):
    #    #wh = DispatchPoint.objects.get( id = warehouse )
    #    return serializers.serialize('json', list( LtiOriginal.objects.filter( origin_wh_code = self.origin_wh_code ) )\
    #                                        + list( EpicStock.objects.filter( wh_code = self.origin_wh_code ) ) )
    #===================================================================================================================

    
class Person(models.Model):
    """Person model"""
    
    user = models.OneToOneField(User, verbose_name=_("User"), related_name='person')
    
    external_ident = models.CharField(_("person identifier"), max_length=20, primary_key=True)
    title = models.CharField(_("title"), max_length=50, blank=True)
    code = models.CharField(_("code"), max_length=7)
    
    compas = models.ForeignKey('ets.Compas', verbose_name=_("compas station"), related_name="persons")
    organization = models.ForeignKey('ets.Organization', verbose_name=_("organization"), related_name="persons")
    location = models.ForeignKey('ets.Location', verbose_name=_("location"), related_name="persons")
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('person')
        verbose_name_plural = _("persons")
    
    def __unicode__(self):
        return "%s %s" % (self.code, self.title)

    def get_warehouses(self):
        return Warehouse.objects.filter(compas=self.compas, organization=self.organization, location=self.location)
        

class CommodityCategory(models.Model):
    """Commodity category"""
    code = models.CharField(_("Commodity Category Code"), max_length=9, primary_key=True)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('commodity category')
        verbose_name_plural = _("commodity categories")
        
    def __unicode__(self):
        return self.pk
    
class Commodity(models.Model):
    """Commodity model"""
    
    code = models.CharField(_("Commodity Code"), max_length=18, primary_key=True)
    name = models.CharField(_("Commodity Name"), max_length=100)
    category = models.ForeignKey(CommodityCategory, verbose_name=_("Commodity Category"), related_name="commodities")
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('Commodity')
        verbose_name_plural = _("Commodities")
    
    def __unicode__(self):
        return self.name

class Package(models.Model):
    """Packaging model"""
    
    code = models.CharField(_("code"), max_length=17, primary_key=True)
    name = models.CharField(_("name"), max_length=50)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('package')
        verbose_name_plural = _("packages")
    
    def __unicode__(self):
        return self.name

            
class StockManager( models.Manager ):
    
    def get_existing_units( self ):
        return super( StockManager, self ).get_query_set().filter( number_of_units__gt = 0 )

class StockItem( models.Model ):
    """Accessible stocks"""
    origin_id = models.CharField(_("Origin identifier"), max_length=23, primary_key=True)
    
    warehouse = models.ForeignKey(Warehouse, verbose_name=_("Warehouse"), related_name="stock_items")
    
    project_number = models.CharField(_("Project Number"), max_length=24, blank=True) #project_wbs_element
    si_code = models.CharField(_("shipping instruction code"), max_length=8)
    
    commodity = models.ForeignKey(Commodity, verbose_name=_("Commodity"), related_name="stocks")
    package = models.ForeignKey(Package, verbose_name=_("Package"), related_name="stocks")
    
    quality_code = models.CharField(_("Quality code"), max_length=1) #qualitycode
    quality_description = models.CharField(_("Quality description "), max_length=11, blank=True) #qualitydescr
    
    number_of_units = models.DecimalField(_("Number of units"), max_digits=12, decimal_places=3)
    unit_weight_net = models.DecimalField(_("Unit weight net"), max_digits=12, decimal_places=3)
    unit_weight_gross = models.DecimalField(_("Unit weight gross"), max_digits=12, decimal_places=3)
    
    is_bulk = models.BooleanField(_("Bulk"), default=False)
    
    updated = models.DateTimeField(_("update date"), default=datetime.now, editable=False)
    
    allocation_code = models.CharField(_("Allocation code"), max_length=10, editable=False)
    #si_record_id = models.CharField(_("SI record id "), max_length=25, editable=False)
    
    objects = StockManager()

    class Meta:
        ordering = ('si_code', 'commodity__name')
        order_with_respect_to = 'warehouse'
        verbose_name = _("stock item")
        verbose_name_plural = _("stocks")

    def  __unicode__( self ):
        return "%s-%s-%s" % (self.warehouse.name, self.commodity.pk, self.number_of_units)
        
    def coi_code(self):
        return self.origin_id[7:]
    
    #===================================================================================================================
    # def number_of_units_ordered(self, order):
    #    """Calculates maximum possible loading ordered amount"""
    #    order.get_stock_items().filter()
    #    return StockItem.objects.filter(warehouse__orders=self,
    #                                    project_number=F('project_number'),
    #                                    si_code = F('warehouse__orders__items__si_code'), 
    #                                    commodity_code = F('warehouse__orders__items__commodity_code'),
    #                                    ).order_by('-warehouse__orders__items__number_of_units')
    #===================================================================================================================

class LossDamageType(models.Model):
    
    LOSS = 'L'
    DAMAGE = 'D'
    
    TYPE_CHOICE = (
        (LOSS, _("Loss")),
        (DAMAGE, _("Damage")),
    )
    
    slug = AutoSlugField(populate_from=lambda instance: "%s%s" % (
                            instance.type, instance.category_id
                         ), unique=True, primary_key=True)
    type = models.CharField(_("Type"), max_length=1, choices=TYPE_CHOICE)
    category = models.ForeignKey(CommodityCategory, verbose_name=_("Commodity category"), 
                                 related_name="loss_damages", db_column='comm_category_code')
    cause = models.CharField(_("Cause"), max_length=100)

    class Meta:
        db_table = u'epic_lossdamagereason'
        verbose_name = _('Loss/Damages Reason')
        verbose_name_plural = _("Losses/Damages")
    
    def  __unicode__( self ):
        cause = self.cause
        length_c = len( cause ) - 10
        if length_c > 20:
            cause = "%s...%s" % (cause[0:20], cause[length_c:])
        return cause
    
    @classmethod
    def update(cls, using):
        with transaction.commit_on_success(using) as tr:
            for myrecord in cls.objects.using(using).values('type', 'category', 'cause'):
                cls.objects.get_or_create(type=myrecord['type'], cause=myrecord['cause'],
                                category_id=CommodityCategory.objects.get_or_create(pk=myrecord['category'])[0])


class Order(models.Model):
    """Delivery order"""
    
    code = models.CharField(_("Code"), max_length=40, primary_key=True, editable=False)
    
    created = models.DateField(_("Created date")) #lti_date
    expiry = models.DateField(_("expire date"), blank=True, null=True) #expiry_date
    dispatch_date = models.DateField(_("Requested Dispatch Date"), blank=True, null=True)
    
    transport_code = models.CharField(_("Transport Code"), max_length = 4, editable=False)
    transport_ouc = models.CharField(_("Transport ouc"), max_length = 13, editable=False)
    transport_name = models.CharField(_("Transport Name"), max_length = 30)
    
    origin_type = models.CharField(_("Origin Type"), max_length = 1, editable=False)
    
    project_number = models.CharField(_("Project Number"), max_length = 24, blank = True) #project_wbs_element
    
    warehouse = models.ForeignKey(Warehouse, verbose_name=_("dispatch warehouse"), related_name="orders")
    consignee = models.ForeignKey(Organization, verbose_name=_("consignee"), related_name="orders")
    location = models.ForeignKey(Location, verbose_name=_("consignee's location"), related_name="orders")
    
    updated = models.DateTimeField(_("update date"), default=datetime.now, editable=False)
    
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ('code',)
    
    def  __unicode__(self):
        return self.code
    
    @models.permalink
    def get_absolute_url(self):
        return ('order_detail', (), {'object_id': self.pk})
    
    def get_stock_items(self):
        """Retrieves stock items for current order through warehouse"""
        return StockItem.objects.filter(warehouse__orders=self,
                                        project_number=self.project_number,
                                        si_code = F('warehouse__orders__items__si_code'), 
                                        commodity = F('warehouse__orders__items__commodity'),
                                        ).order_by('-warehouse__orders__items__number_of_units')
    
    def get_percent_executed(self):
        return sum(item.get_percent_executed() for item in self.items.all()) / self.items.all().count()
    

class OrderItem(models.Model):
    """Order item with commodity and counters"""
    
    lti_pk = models.CharField(_("COMPAS LTI identifier"), max_length=50, editable=False, primary_key=True)
    order = models.ForeignKey(Order, verbose_name=_("Order"), related_name="items")
    
    si_code = models.CharField( _("Shipping Order Code"), max_length=8)
    
    commodity = models.ForeignKey(Commodity, verbose_name=_("Commodity"), related_name="order_items")
    
    number_of_units = models.DecimalField(_("Number of Units"), max_digits=12, decimal_places=3)
    
    class Meta:
        ordering = ('si_code',)
        order_with_respect_to = 'order'
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
    
    def  __unicode__( self ):
        return u"%s -  %.0f " % ( self.commodity, self.items_left() )

    def get_stock_items(self):
        """Retrieves stock items for current order item through warehouse"""
        return StockItem.objects.filter(warehouse__orders__items=self,
                                        project_number=self.order.project_number,
                                        si_code = self.si_code, 
                                        commodity = self.commodity,
                                        ).order_by('-number_of_units')      
    
    @staticmethod
    def sum_number( queryset ):
        return queryset.aggregate(units_count=Sum('number_of_units'))['units_count'] or 0
    
    def get_similar_dispatches(self):
        """Returns all loading details with such item within any orders"""
        return LoadingDetail.objects.filter(waybill__transport_dispach_signed_date__isnull=False, 
                                            waybill__order__project_number=self.order.project_number,
                                            waybill__date_removed__isnull=True,
                                            stock_item__si_code = self.si_code, 
                                            stock_item__commodity = self.commodity,
                                            ).order_by('-waybill__dispatch_date')
    
    def get_order_dispatches(self):
        """Returns dispatches of current order"""
        return self.get_similar_dispatches().filter(waybill__order=self.order)
    
    
    def get_available_stocks(self):
        """Calculates available stocks"""
        return self.sum_number(self.get_stock_items()) - self.sum_number(self.get_similar_dispatches())
        
    def get_percent_executed(self):
        """Calculates percent for executed"""
        return self.number_of_units and round(100 * self.sum_number(self.get_order_dispatches()) / self.number_of_units)
        
    def items_left( self ):
        """Calculates number of such items supposed to be delivered in this order"""
        return self.number_of_units - self.sum_number(self.get_order_dispatches())
    


class Waybill( ld_models.Model ):
    """
    Base waybill abstract class
    """
    
    TRANSACTION_TYPES = ( 
                        ( u'WIT', _(u'WFP Internal') ),
                        ( u'DEL',_( u'Delivery' )),
                        ( u'SWA', _(u'Swap' )),
                        ( u'REP', _(u'Repayment' )),
                        ( u'SAL', _(u'Sale' )),
                        ( u'ADR', _(u'Air drop' )),
                        ( u'INL', _(u'Inland Shipment' )),
                        ( u'DIS', _(u'Distribution' )),
                        ( u'LON', _(u'Loan' )),
                        ( u'DSP', _(u'Disposal' )),
                        ( u'PUR', _(u'Purchase' )),
                        ( u'SHU', _(u'Shunting' )),
                        ( u'COS', _(u'Costal Transshipment' )),
                )
    TRANSPORT_TYPES = ( 
                        ( u'02', _(u'Road' )),
                        ( u'01', _(u'Rail' )),
                        ( u'04', _(u'Air' )),
                        ( u'I', _(u'Inland Waterways' )),
                        ( u'C', _(u'Costal Waterways' )),
                        ( u'07', _(u'Multi-mode' )),
#                        (u'O', _(u'Other Please Specify'))
                )
    
    NEW = 1
    SIGNED = 2
    SENT = 3
    INFORMED = 4
    DELIVERED = 5
    COMPLETE = 6
    
    slug = AutoSlugField(populate_from=lambda instance: "%s%s%s" % (
                            instance.order.warehouse.pk, instance.date_created.strftime('%y'), LETTER_CODE
                         ), unique_with=('date_removed',), slugify=capitalize_slug(slugify),
                         sep='', primary_key=True)
    
    order = models.ForeignKey(Order, verbose_name=_("Order"), related_name="waybills")
    
    destination = models.ForeignKey(Warehouse, verbose_name=_("Receipt Warehouse"), related_name="receipt_waybills")
    
    #Dates
    loading_date = models.DateField(_("Date of loading"), default=datetime.now) #dateOfLoading
    dispatch_date = models.DateField( _("Date of dispatch"), default=datetime.now) #dateOfDispatch
    
    transaction_type = models.CharField(_("Transaction Type"), max_length=10, 
                                         choices=TRANSACTION_TYPES, default=TRANSACTION_TYPES[0][0]) #transactionType
    transport_type = models.CharField(_("Transport Type"), max_length=10, 
                                      choices=TRANSPORT_TYPES, default=u'02') #transportType
    
    #Dispatcher
    dispatch_remarks = models.CharField(_("Dispatch Remarks"), max_length=400, blank=True)
    dispatcher_person = models.ForeignKey(Person, verbose_name=_("Dispatch person"), 
                                          related_name="dispatch_waybills") #dispatcherName
    
    #Transporter
    transport_sub_contractor = models.CharField(_("Transport Sub contractor"), max_length=40, blank=True) #transportSubContractor
    transport_driver_name = models.CharField(_("Transport Driver Name"), max_length=40) #transportDriverName
    transport_driver_licence = models.CharField(_("Transport Driver LicenceID "), max_length=40) #transportDriverLicenceID
    transport_vehicle_registration = models.CharField(_("Transport Vehicle Registration "), max_length=40) #transportVehicleRegistration
    transport_trailer_registration = models.CharField( _("Transport Trailer Registration"), max_length=40, blank=True) #transportTrailerRegistration
    transport_dispach_signed_date = models.DateTimeField( _("Transport Dispach Signed Date"), null=True, blank=True) #transportDispachSignedTimestamp

    #Container        
    container_one_number = models.CharField(_("Container One Number"), max_length=40, blank=True) #containerOneNumber
    container_two_number = models.CharField( _("Container Two Number"), max_length=40, blank=True) #containerTwoNumber
    container_one_seal_number = models.CharField(_("Container One Seal Number"), max_length=40, blank=True) #containerOneSealNumber
    container_two_seal_number = models.CharField(_("Container Two Seal Number"), max_length=40, blank=True ) #containerTwoSealNumber
    container_one_remarks_dispatch = models.CharField( _("Container One Remarks Dispatch"), max_length=40, blank=True) #containerOneRemarksDispatch
    container_two_remarks_dispatch = models.CharField( _("Container Two Remarks Dispatch"), max_length=40, blank=True) #containerTwoRemarksDispatch

    #Extra Fields
    validated = models.BooleanField( _("Waybill Validated"), default=False) #waybillValidated
    sent_compas = models.DateTimeField(_("Waybill Sent to Compas"), blank=True, null=True)
    
    audit_log = AuditLog()

    objects = ld_models.managers.LogicalDeletedManager()
    
    class Meta:
        ordering = ('slug',)
        order_with_respect_to = 'order'
        verbose_name = _("waybill")
        verbose_name_plural = _("waybills")
    
    def  __unicode__( self ):
        return self.slug
    
    @models.permalink
    def get_absolute_url(self):
        return ('waybill_view', (), {'waybill_pk': self.pk})

    #===================================================================================================================
    # def errors(self):
    #    try:
    #        return CompasLogger.objects.get( wb = self )
    #    except CompasLogger.DoesNotExist:
    #        return ''
    #===================================================================================================================
    
    def clean(self):
        """Validates Waybill instance. Checks different dates"""
        if self.loading_date > self.dispatch_date:
            raise ValidationError(_("Cargo Dispatched before being Loaded"))
        
        #If second container exists, first must exist also
        if self.container_two_number and not self.container_one_number:
            raise ValidationError(_("Type container 1 number"))
    
    def check_lines( self ):
        lines = LoadingDetail.objects.filter( wbNumber = self )
        for line in lines:
            if not line.check_stock():
                return False
        return True

    def check_lines_receipt( self ):
        lines = LoadingDetail.objects.filter( wbNumber = self )
        for line in lines:
            if not line.check_receipt_item():
                return False
        return True

    @property
    def hasError( self ):
        myerror = self.errors()
        try:
            if ( myerror.errorRec != '' or myerror.errorDisp != '' ):
                return True
        except:
            return None

    def dispatch_sign(self, commit=True):
        """Signs the waybill as ready to be sent."""
        self.transport_dispach_signed_date = datetime.now()
        
        if commit:
            self.save()
    
    def get_receipt(self):
        """Returns receipt instance if exists or None otherwise"""
        try:
            receipt = self.receipt
        except ReceiptWaybill.DoesNotExist:
            receipt = None
        
        return receipt
    
    
    def serialize(self):
        """
        This method serializes the Waybill with related LoadingDetails, LtiOriginals and EpicStocks.
    
        @param self: the Waybill instance
        @return the serialized json data.
        """
        
        items = chain((self,), self.loading_details.all())
        
        receipt = self.get_receipt()
        if receipt:
            items = chain((receipt,), items)
        
        return serializers.serialize( 'json', items)
        
    def compress(self):
        """
        This method compress the Waybill using zipBase64 algorithm.
    
        @param self: the Waybill instance
        @return: a string containing the compressed representation of the Waybill with related LoadingDetails, LtiOriginals and EpicStocks
        """
        return base64.b64encode( zlib.compress( simplejson.dumps( self.serialize(), use_decimal=True ) ) )
    
    def decompress(self, data):
        data = string.replace( data, ' ', '+' )
        zippedData = base64.b64decode( data )
        return zlib.decompress( zippedData )
    
    
    @classmethod
    def dispatches(cls, user):
        """Returns all loaded but not signed waybills, and related to user"""
        return cls.objects.filter(transport_dispach_signed_date__isnull=True,
                                  order__warehouse__in=Warehouse.filter_by_user(user))
    
    @classmethod
    def receptions(cls, user):
        """Returns all waybills, that can be received, and related to user"""
        return cls.objects.filter(transport_dispach_signed_date__isnull=False, 
                                  #receipt__isnull=False,
                                  receipt__signed_date__isnull=True,
                                  destination__in=Warehouse.filter_by_user(user))
    
    def get_shortage_loading_details(self):
        return [loading_detail for loading_detail in self.loading_details.all() if loading_detail.get_shortage()]    

class ReceiptWaybill(models.Model):
    """Receipt data"""
    waybill = models.OneToOneField(Waybill, verbose_name=_("Waybill"), related_name="receipt")
    slug = AutoSlugField(populate_from='waybill', unique=True, sep='', primary_key=True, editable=False)
    
    person =  models.ForeignKey(Person, verbose_name=_("Recipient person"), related_name="recipient_waybills") #recipientName
    arrival_date = models.DateField(_("Recipient Arrival Date")) #recipientArrivalDate
    start_discharge_date = models.DateField(_("Recipient Start Discharge Date")) #recipientStartDischargeDate
    end_discharge_date = models.DateField(_("Recipient End Discharge Date")) #recipientEndDischargeDate
    distance = models.IntegerField(_("Recipient Distance (km)"), blank=True, null=True) #recipientDistance
    remarks = models.CharField(_("Recipient Remarks"), max_length=40, blank=True) #recipientRemarks
    signed_date = models.DateTimeField(_("Recipient Signed Date"), blank=True, null=True) #recipientSignedTimestamp
    
    container_one_remarks_reciept = models.CharField( _("Container One Remarks Reciept"), max_length=40, blank=True) #containerOneRemarksReciept
    container_two_remarks_reciept = models.CharField(_("Container Two Remarks Reciept"), max_length=40, blank=True) #containerTwoRemarksReciept
    
    validated = models.BooleanField(_("Waybill Receipt Validated"), default=False) #waybillReceiptValidated
    sent_compas = models.DateTimeField(_("Waybill Reciept Sent to Compas"), blank=True, null=True)
    
    class Meta:
        ordering = ('slug',)
        order_with_respect_to = 'waybill'
        verbose_name = _("reception")
        verbose_name_plural = _("reception")
    
    def __unicode__(self):
        return "Reception of waybill: %s" % self.waybill_id
    
    def sign(self, commit=True):
        """
        Signs the waybill as delivered. 
        After this system sends it to central server.
        """
        self.signed_date = datetime.now()
        
        if commit:
            self.save()
    
    def clean(self):
        """Validates Waybill instance. Checks different dates"""
    
        #===============================================================================================================
        # if self.arrival_date \
        # and self.arrival_date < self.waybill.dispatch_date:
        #    raise ValidationError(_("Cargo arrived before being dispatched"))
        #===============================================================================================================

        if self.start_discharge_date and self.arrival_date \
        and self.start_discharge_date < self.arrival_date:
            raise ValidationError(_("Cargo Discharge started before Arrival?"))

        if self.start_discharge_date and self.end_discharge_date \
        and self.end_discharge_date < self.start_discharge_date:
            raise ValidationError(_("Cargo finished Discharge before Starting?"))

    
class LoadingDetail(models.Model):
    """Loading details related to dispatch waybill"""
    waybill = models.ForeignKey(Waybill, verbose_name=_("Waybill Number"), related_name="loading_details")
    slug = AutoSlugField(populate_from='waybill', unique=True, sep='', primary_key=True)
    
    #Stock data
    stock_item = models.ForeignKey(StockItem, verbose_name=_("Stock item"), related_name="dispatches")
    
    number_of_units = models.DecimalField(_("Number of Units"), max_digits=7, decimal_places=3)

    #Number of delivered units
    number_units_good = models.DecimalField(_("number Units Good"), default=0, 
                                            max_digits=10, decimal_places=3) #numberUnitsGood
    number_units_lost = models.DecimalField(_("number Units Lost"), default=0, 
                                            max_digits=10, decimal_places=3 ) #numberUnitsLost
    number_units_damaged = models.DecimalField(_("number Units Damaged"), default=0, 
                                               max_digits=10, decimal_places=3 ) #numberUnitsDamaged
    
    #Reasons
    units_lost_reason = models.ForeignKey( LossDamageType, verbose_name=_("Lost Reason"), 
                                           related_name='lost_reason', #LD_LostReason 
                                           blank=True, null=True,
                                           limit_choices_to={'type': LossDamageType.LOSS}) #unitsLostReason
    units_damaged_reason = models.ForeignKey( LossDamageType, verbose_name=_("Damaged Reason"), 
                                            related_name='damage_reason', #LD_DamagedReason 
                                            blank=True, null=True,
                                            limit_choices_to={'type': LossDamageType.DAMAGE}) #unitsDamagedReason
    
    overloaded_units = models.BooleanField(_("overloaded Units"), default=False) #overloadedUnits
    over_offload_units = models.BooleanField(_("over offloaded Units"), default=False) #overOffloadUnits

    audit_log = AuditLog()

    class Meta:
        ordering = ('slug',)
        order_with_respect_to = 'waybill'
        verbose_name = _("loading detail")
        verbose_name_plural = _("waybill items")
        unique_together = ('waybill', 'stock_item')


    def get_shortage( self ):
        not_validated_sum = LoadingDetail.objects.filter(stock_item=self.stock_item, waybill__validated=False)\
                                .aggregate(Sum('number_of_units'))['number_of_units__sum']
        return max(0, not_validated_sum - self.stock_item.number_of_units)

    def get_order_item(self):
        """Retrieves stock items for current order item through warehouse"""
        return OrderItem.objects.get(order=self.waybill.order,
                                     order__project_number=self.stock_item.project_number,
                                     si_code = self.stock_item.si_code, 
                                     commodity = self.stock_item.commodity,)
    
    def calculate_total_net( self ):
        return ( self.number_of_units * self.stock_item.unit_weight_net ) / 1000

    def calculate_total_gross( self ):
        return ( self.number_of_units * self.stock_item.unit_weight_gross ) / 1000

    def calculate_net_received_good( self ):
        return ( self.number_units_good * self.stock_item.unit_weight_net ) / 1000

    def calculate_gross_received_good( self ):
        return ( self.number_units_good * self.stock_item.unit_weight_gross ) / 1000

    def calculate_net_received_damaged( self ):
        return ( self.number_units_damaged * self.stock_item.unit_weight_net ) / 1000

    def calculate_gross_received_damaged( self ):
        return ( self.number_units_damaged * self.stock_item.unit_weight_gross ) / 1000

    def calculate_net_received_lost( self ):
        return ( self.number_units_lost * self.stock_item.unit_weight_net ) / 1000

    def calculate_gross_received_lost( self ):
        return ( self.number_units_lost * self.stock_item.unit_weight_gross ) / 1000
    
    def calculate_total_received_units( self ):
        return self.number_units_good + self.number_units_damaged

    def calculate_total_received_net( self ):
        return self.calculate_net_received_good() + self.calculate_net_received_damaged()
    
    def  __unicode__( self ):
        return "%s - %s - %s" % (self.waybill, self.stock_item.si_code, self.number_of_units)
    
    def clean(self):
        
        #clean number of items
        if self.number_of_units \
        and (self.number_units_good or self.number_units_damaged or self.number_units_lost) \
        and (self.number_of_units > self.number_units_good + self.number_units_damaged + self.number_units_lost):
            raise ValidationError(_("%(loaded).3f Units loaded but %(offload).3f units accounted for") % {
                    "loaded" : self.number_of_units, 
                    "offload" : self.number_units_good + self.number_units_damaged + self.number_units_lost 
            })
        
        #overloaded units for dispatch
        if not self.waybill.transport_dispach_signed_date:
            order_item = self.get_order_item()
            if order_item.items_left() < self.number_of_units and not self.overloaded_units:
                raise ValidationError(_("Overloaded for %.3f units") % (self.number_of_units - order_item.items_left(),))
    
        #overloaded units for reception
        total = self.number_units_good + self.number_units_damaged + self.number_units_lost
        if total > self.number_of_units and not self.over_offload_units:
            raise ValidationError(_("Over offloaded for %.3f units") % (total - self.number_of_units,))
        
        #Clean units_lost_reason
        if self.number_units_lost and not self.units_lost_reason:
                raise ValidationError(_("You must provide a loss reason"))
        #Clean units_damaged_reason
        if self.number_units_damaged and not self.units_damaged_reason:
                raise ValidationError(_("You must provide a damaged reason"))
            
        #clean reasons
        if self.units_damaged_reason and self.units_damaged_reason.category != self.stock_item.commodity.category:
            raise ValidationError(_("You have chosen wrong damaged reason for current commodity category"))
        if self.units_lost_reason and self.units_lost_reason.category != self.stock_item.commodity.category:
            raise ValidationError(_("You have chosen wrong loss reason for current commodity category"))
        

class CompasLogger(models.Model):
    
    DISPATCH = 1
    RECEIPT = 2
    
    ACTIONS = (
        (DISPATCH, _("Dispatch")),
        (RECEIPT, _("Receipt"))           
    )
    
    SUCCESS = 0
    FAILURE = 1
    
    STATUSES = (
        (SUCCESS, _("Success")),
        (FAILURE, _("Failure"))
    )
    
    action = models.IntegerField(_("procedure name"), choices=ACTIONS)
    compas = models.ForeignKey(Compas, verbose_name=_("COMPAS"), related_name="logs")
    waybill = models.ForeignKey(Waybill, verbose_name=_("Waybill"), related_name="compass_loggers")
    when_attempted = models.DateTimeField(_("when attempted"), default=datetime.now)
    status = models.IntegerField(_("status"), choices=STATUSES, default=SUCCESS)
    message = models.CharField(_("error message"), max_length=512)
    
    class Meta:
        ordering = ('-when_attempted',)
        verbose_name = _("compas logger")
        verbose_name_plural = _("compas errors")
    
    def __unicode__(self):
        return "%s: %s" % (self.code, self.message)
    
