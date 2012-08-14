
import decimal, cStringIO, pyqrcode
#from urllib import urlencode
from itertools import chain
from functools import wraps
from datetime import datetime, date
import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core import serializers
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.cache import cache

from autoslug.fields import AutoSlugField
from autoslug.settings import slugify
import logicaldelete.models as ld_models

from ets.compress import compress_json, decompress_json
from ets.country import COUNTRY_CHOICES

#name = "1234"
BULK_NAME = "BULK"
LETTER_CODE = getattr(settings, 'WAYBILL_LETTER', 'A')
ACCURACY = 1
MINIMUM_AGE = 5

def capitalize_slug(func):
    @wraps(func)
    def wrapper(value):
        slug = func(value)
        return slug.upper()
    
    return wrapper


class Compas(ld_models.Model):
    """
    Compas station
        - **code** -- station code
        - **officers** -- officers related to compas
        - **description** -- station description
        - **read_only** -- access to compas station
        - **db_engine** -- database engine
        - **db_name** -- name for related database
        - **db_user** -- database user
        - **db_password** -- password of database user
        - **db_host** -- database host
        - **db_port** -- database server port 
    """
    
    cache_prefix = "sync_compas"
    
    code = models.CharField(_("Station code"), max_length=20, primary_key=True)
    officers = models.ManyToManyField(User, verbose_name=_("Officers"), related_name="compases", db_index=True)
    description = models.CharField(_("Description"), max_length=20, blank=True)
    read_only = models.BooleanField(_("Read-only compas station"), default=False)
    is_base = models.BooleanField(_("Base station"), default=False, 
                                  help_text=_("Import of administrative table is possible"))
    
    #Database settings
    db_engine = models.CharField(_("Database engine"), max_length=100, default="django.db.backends.oracle")
    db_name = models.CharField(_("Database name"), max_length=100)
    db_user = models.CharField(_("Database user"), max_length=100, blank=True)
    db_password = models.CharField(_("Database password"), max_length=100, blank=True)
    db_host = models.CharField(_("Database host"), max_length=100, default='localhost')
    db_port = models.CharField(_("Database server port"), max_length=4, blank=True)

    class Meta:
        ordering = ('code',)
        verbose_name = _('Compas station')
        verbose_name_plural = _("Compas stations")
        
    def __unicode__(self):
        return self.pk

    def sync_last_attempt(self):
        """Returns last attempt of updating or default value"""
        try:
            last_attempt = ImportLogger.objects.filter(compas=self).order_by('-when_attempted')[0].when_attempted
        except (ImportLogger.DoesNotExist, IndexError):
            last_attempt = datetime(1900, 1, 1)
        return last_attempt
    
    def get_last_attempt(self):
        """Returns last attempt of updating or raises exception"""
        return self.import_logs.order_by('-when_attempted')[0]
    
    def get_cache_key(self, methods):
        """Returns cache key for update method"""
        return "%s_%s_%s" % (self.cache_prefix, "".join([m.__name__ for m in methods]), self.pk)
    
    def get_update_methods(self, base=False):
        """Returns methods depending on base import or update"""
        from ets import utils
        methods = {
            True: (utils.import_partners, utils.import_places, utils.import_reasons, utils.import_persons),
            False: (utils.import_stock, utils.import_order)
        }
        return methods[base]
    
    def is_locked(self, base=False):
        """Checks for executing update"""
        return cache.get(self.get_cache_key(self.get_update_methods(base)), False)
    
    def update(self, base=False):
        """Utility to run whole import process. If no fails Success ImportLogger is created."""
        
        methods = self.get_update_methods(base)
        
        cache_key = self.get_cache_key(methods)
        
        if cache.get(cache_key, False):
            return
        
        cache.set(cache_key, True, MINIMUM_AGE*60)
        try:
            for func in methods:
                
                try: 
                    with transaction.commit_on_success(self.pk) as tr:
                        func(self.pk)
                except Exception, err:
                    self.import_logs.create(status=ImportLogger.FAILURE,
                                            message="%s: %s" % (func.__name__, unicode(err)))
                    raise
        except Exception:
            #Since we already created log for this error simply pass here
            pass
        else:
            self.import_logs.create()
        finally:
            cache.delete(cache_key)
    
    
class Location(models.Model):
    """
    Location model. City or region
        - **code** -- GEO point code of location
        - **name** -- name of location
        - **country** -- name of related country
    """
    
    code = models.CharField(_("Geo point code"), max_length=4, primary_key=True)
    name = models.CharField(_("Name"), max_length=100)
    country = models.CharField( _("Country"), max_length=3, choices=COUNTRY_CHOICES, blank=True, null=True)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('location')
        verbose_name_plural = _("locations")
    
    def __unicode__(self):
        return "%s %s" % (self.country, self.name)
    
class Organization(models.Model):
    """
    Organization model
        - **code** -- unique identifier in COMPAS
        - **name** -- organization title
    """
    
    code = models.CharField(_("code"), max_length=20, primary_key=True)
    name = models.CharField(_("Name"), max_length=100, blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('organization')
        verbose_name_plural = _("organizations")
    
    def __unicode__(self):
        return self.name or self.code

class Warehouse(models.Model):
    """
    Warehouse. dispatch or recipient.
        - **code** -- unique identifier in COMPAS
        - **name** -- origin name of warehouse
        - **location** -- foreign key to location of warehouse
        - **organization** -- foreign key to related organization
        - **compas** -- foreign key to COMPAS station
        - **compas_text** -- text input for COMPAS station for not managed warehouses
        - **valid_warehouse** -- validity of warehouse
        - **start_date** -- start date of the warehouse
        - **end_date** -- end date of the warehouse
    """
    code = models.CharField(_("code"), max_length = 13, primary_key=True) #origin_wh_code
    name = models.CharField(_("name"),  max_length = 50, blank = True ) #origin_wh_name
    location = models.ForeignKey(Location, verbose_name=_("location"), related_name="warehouses") #origin_location_code
    organization = models.ForeignKey(Organization, verbose_name=_("Organization"), related_name="warehouses", 
                                     blank=True, null=True)
    compas = models.ForeignKey(Compas, verbose_name=_("COMPAS station"), related_name="warehouses", blank=True, null=True)
    compas_text = models.CharField(_("COMPAS Station (Text)"), max_length = 13, blank=True, null=True) #COMPAS station for not managed WH
    valid_warehouse = models.BooleanField(_("Is Warehouse"), default=True)
    start_date = models.DateField(_("Start date"), blank=True, null=True, db_index=True)
    end_date = models.DateField(_("End date"), blank=True, null=True, db_index=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = _('warehouse')
        verbose_name_plural = _("warehouses")
        
    def  __unicode__( self ):
        return "%s - %s - %s" % (self.code, self.location.name, self.name)

    
    @classmethod
    def get_active_warehouses(cls):
        """Returns active warehouses"""
        return cls.objects.filter(valid_warehouse=True).filter(compas__in=Compas.objects.all()).filter(start_date__lte=date.today).filter(end_date__isnull=True)

    @classmethod
    def get_active_warehouses_with_stock(cls):
        """Returns active warehouses"""
        whws = StockItem.objects.filter(number_of_units__gt =0).values_list('warehouse').order_by('warehouse').distinct('warehouse')
        wh = cls.objects.filter(valid_warehouse=True).filter(compas__in=Compas.objects.all()).filter(start_date__lte=date.today).filter(end_date__isnull=True).filter(code__in=whws)
        
        return wh


    @classmethod
    def get_warehouses(cls, location, organization=None):
        """Returns warehouses related to location or organization"""
        queryset = cls.get_active_warehouses().filter(location=location)

        #Check wh for specific organization
        if organization and queryset.filter(organization=organization).exists():
            return queryset.filter(organization=organization)
        
        return queryset

    #===================================================================================================================
    # @classmethod
    # def filter_by_user(cls, user):
    #    return cls.objects.filter(location__persons__username=user.username, 
    #                              organization__persons__username=user.username,
    #                              compas__persons__username=user.username,
    #                              start_date__lte=date.today)\
    #            .filter(models.Q(end_date__gt=date.today) | models.Q(end_date__isnull=True))\
    #===================================================================================================================

    def get_persons(self):
        """Returns related persons"""
        return Person.objects.filter(compas=self.compas, organization=self.organization, location=self.location)

    
class Person(User):
    """
    Person model
        - **code** -- identifier in COMPAS
        - **title** -- title of person
        - **compas** -- foreign key to related Compas
        - **organization** -- foreign key to related organization
        - **location**
        - **warehouses** -- many-to-many relation to warehouses
        - **dispatch** -- can person dispatch waybills
        - **receive** -- can person receive waybills
        - **updated** -- update date
    """
    
    code = models.CharField(_("code"), max_length=7)
    title = models.CharField(_("title"), max_length=50, blank=True)
    
    compas = models.ForeignKey('ets.Compas', verbose_name=_("compas station"), related_name="persons")
    organization = models.ForeignKey('ets.Organization', verbose_name=_("organization"), related_name="persons")
    location = models.ForeignKey('ets.Location', verbose_name=_("location"), related_name="persons")
    
    warehouses = models.ManyToManyField('ets.Warehouse', verbose_name=_("Warehouses"), related_name="persons", db_index=True)
    
    dispatch = models.BooleanField(_("Can dispatch"), default=False, db_index=True)
    receive = models.BooleanField(_("Can receive"), default=False, db_index=True)
    
    updated = models.DateTimeField(_("update date"), default=datetime.now, editable=False)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('person')
        verbose_name_plural = _("persons")
        unique_together = ('compas', 'code')
    
    def __unicode__(self):
        return "%s %s" % (self.code, self.title)

    #===================================================================================================================
    # def get_warehouses(self):
    #    return Warehouse.objects.filter(compas=self.compas, organization=self.organization, location=self.location) \
    #                            .filter(start_date__lte=date.today)\
    #                            .filter(models.Q(end_date__gt=date.today) | models.Q(end_date__isnull=True))
    #===================================================================================================================
        

class CommodityCategory(models.Model):
    """
    Commodity category
        - **code**
    """
    code = models.CharField(_("Commodity Category Code"), max_length=9, primary_key=True)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('Commodity Category')
        verbose_name_plural = _("Commodity Categories")
        
    def __unicode__(self):
        return self.pk
    
class Commodity(models.Model):
    """
    Commodity model
        - **code** -- unique identifier
        - **name** -- commodity title
        - **category** -- related commodity category
    """
    
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
    """
    Packaging model
        - **code** -- unique identifier
        - **name** -- name of package
    """
    
    code = models.CharField(_("code"), max_length=17, primary_key=True)
    name = models.CharField(_("name"), max_length=50)
    
    class Meta:
        ordering = ('code',)
        verbose_name = _('Packaging')
        verbose_name_plural = _("Packaging")
    
    def __unicode__(self):
        return self.name

            
class StockManager( models.Manager ):
    
    def get_existing_units( self ):
        return super( StockManager, self ).get_query_set().filter( number_of_units__gt = 0 )

class StockItem( models.Model ):
    """
    Accessible stocks
        - **code** -- simplified and encoded external ident
        - **warehouse** -- title of person
        - **project_number**
        - **si_code** -- shipping instruction code
        - **commodity** -- commodity of stock item
        - **package** -- package
        - **external_ident** -- external identifier
        - **quality** -- Quality
        - **quantity_net** -- Net MT
        - **quantity_gross** -- Gross MT
        - **number_of_units** -- Number of units
        - **unit_weight_net** -- Unit weight net
        - **unit_weight_gross** -- unit weight gross
        - **is_bulk** -- stock is bulk or not
        - **updated** -- last update date
        - **si_record_id** -- SI record id
        - **origin_id** -- origin identifier
        - **allocation_code** -- allocation code
        - **virtual** -- virtual stock
    """
    
    GOOD_QUALITY = 'G'
    GOOD_QUALITY_LABEL = _("Good")
    
    QUALITY_CHOICE = (
        (GOOD_QUALITY, GOOD_QUALITY_LABEL), 
        ('D', u'Damaged'), 
        ('S', u'Spoiled'), 
        ('U', u'Unavailable'),
    )
    
    code = AutoSlugField(populate_from="external_ident", slugify=capitalize_slug(slugify), 
                         max_length=128, unique=True, sep='', 
                         editable=True, primary_key=True)
    
    warehouse = models.ForeignKey(Warehouse, verbose_name=_("Warehouse"), related_name="stock_items")
    
    project_number = models.CharField(_("Project Number"), max_length=24, blank=True, db_index=True) #project_wbs_element
    si_code = models.CharField(_("shipping instruction code"), max_length=8, db_index=True)
    
    commodity = models.ForeignKey(Commodity, verbose_name=_("Commodity"), related_name="stocks")
    package = models.ForeignKey(Package, verbose_name=_("Package"), related_name="stocks")
    
    external_ident = models.CharField(_("External Identifier"), max_length=128, default="111")
    quality = models.CharField(_("Quality"), max_length=1, choices=QUALITY_CHOICE) #qualitycode
    quantity_net =  models.DecimalField(_("Net MT"), max_digits=12, decimal_places=3)
    quantity_gross =  models.DecimalField(_("Gross MT"), max_digits=12, decimal_places=3)
    
    number_of_units = models.DecimalField(_("Number of units"), max_digits=12, decimal_places=3)
    unit_weight_net = models.DecimalField(_("Unit weight net"), max_digits=12, decimal_places=3,default='0')
    unit_weight_gross = models.DecimalField(_("Unit weight gross"), max_digits=12, decimal_places=3,default='0')
    
    is_bulk = models.BooleanField(_("Bulk"), default=False)
    
    updated = models.DateTimeField(_("update date"), default=datetime.now, editable=False)
    
    si_record_id = models.CharField(_("SI record id"), max_length=25, primary_key=False)
    origin_id = models.CharField(_("Origin identifier"), max_length=23)
    allocation_code = models.CharField(_("Allocation code"), max_length=10, editable=False)
    
    virtual = models.BooleanField(_("Virtual stock"), default=False)
    
    objects = StockManager()

    class Meta:
        ordering = ('si_code', 'commodity__name')
        verbose_name = _("Stock Item")
        verbose_name_plural = _("Stock Items")
        unique_together = ('external_ident', 'quality')

    def  __unicode__( self ):
        name = "%s-%s" % (self.origin_id, self.commodity.name)
        if self.quality != self.GOOD_QUALITY:
            return "%s (%s)" % (name, self.get_quality_display())
        return name
        
    def coi_code(self):
        """Returns coi code from origin identifier"""
        return self.origin_id[7:]
    
    def calculate_total_gross(self):
        return self.quantity_gross

    def get_order_item(self, order_pk):
        """Retrieves stock items for current order item through warehouse"""
        return OrderItem.objects.filter(order__pk=order_pk,
                                     project_number=self.project_number,
                                     si_code=self.si_code, 
                                     commodity=self.commodity,
                                     )[0]
    
    def get_order_quantity(self, order_pk):
        """Retrieves stock items for current order item through warehouse"""
        return  "%.3f (MT)" % (self.get_order_item(order_pk).tonnes_left())
        
    
class LossDamageType(models.Model):
    """
    Type of loss/damage
        - **slug** -- simplified and encoded title for proper URL
        - **type** -- loss/damage type
        - **category** -- commodity category
        - **cause** -- description of reasons for difference
    """
    
    LOSS = 'L'
    DAMAGE = 'D'
    
    TYPE_CHOICE = (
        (LOSS, _("Loss")),
        (DAMAGE, _("Damage")),
    )
    
    slug = AutoSlugField(populate_from=lambda instance: "%s%s" % (
                            instance.type, instance.category_id
                         ), unique=True, editable=True, primary_key=True)
    type = models.CharField(_("Type"), max_length=1, choices=TYPE_CHOICE)
    category = models.ForeignKey(CommodityCategory, verbose_name=_("Commodity category"), 
                                 related_name="loss_damages", db_column='comm_category_code')
    cause = models.CharField(_("Cause"), max_length=100)

    class Meta:
        db_table = u'epic_lossdamagereason'
        verbose_name = _('Loss/Damages Reason')
        verbose_name_plural = _("Losses/Damages")
    
    def  __unicode__( self ):
        return self.cause
        
    @classmethod
    def update(cls, using):
        with transaction.commit_on_success(using) as tr:
            for myrecord in cls.objects.using(using).values('type', 'category', 'cause'):
                cls.objects.get_or_create(type=myrecord['type'], cause=myrecord['cause'],
                                category_id=CommodityCategory.objects.get_or_create(pk=myrecord['category'])[0])


class Order(models.Model):
    """
    Delivery order
        - **code** -- identifier in COMPAS
        - **created** -- date of creating
        - **expiry** -- expire date of order
        - **dispatch_date** -- shipping instruction code
        - **transport_code** -- transport identifier
        - **transport_ouc** -- transport ouc
        - **transport_name** -- name of transport
        - **origin_type** -- origin type
        - **warehouse** -- dispatch warehouse
        - **consignee** -- consignee
        - **location** -- consignee's location
        - **remarks** -- some description of order
        - **remarks_b** -- more complete remarks
        - **updated** -- last update date
        - **percentage** -- percentage of executing 
    """
    
    code = models.CharField(_("Code"), max_length=40, primary_key=True)
    
    created = models.DateField(_("Created date"), default=date.today, db_index=True) #lti_date
    expiry = models.DateField(_("expire date"), default=date.today, db_index=True) #expiry_date
    dispatch_date = models.DateField(_("Requested Dispatch Date"), blank=True, null=True, db_index=True)
    
    transport_code = models.CharField(_("Transport Code"), max_length = 4, editable=False)
    transport_ouc = models.CharField(_("Transport ouc"), max_length = 13, editable=False)
    transport_name = models.CharField(_("Transport Name"), max_length = 30)
    
    origin_type = models.CharField(_("Origin Type"), max_length = 1, editable=False)
    
    warehouse = models.ForeignKey(Warehouse, verbose_name=_("dispatch warehouse"), related_name="orders")
    consignee = models.ForeignKey(Organization, verbose_name=_("consignee"), related_name="orders")
    location = models.ForeignKey(Location, verbose_name=_("consignee's location"), related_name="orders")
    
    remarks = models.TextField(_("Remarks"), blank=True)
    remarks_b = models.TextField(_("More Remarks"), blank=True)
    
    updated = models.DateTimeField(_("update date"), default=datetime.now, editable=False)

    percentage = models.IntegerField(_("Percentage of Executing"), default=0, db_index=True)
    
    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")
        ordering = ('-created',)
    
    def  __unicode__(self):
        return self.code
    
    @models.permalink
    def get_absolute_url(self):
        return ('order_detail', (), {'object_id': self.pk})
    
    def get_stock_items(self):
        """Retrieves stock items for current order through warehouse"""
        try:
            stockItem = chain(*(item.stock_items().values_list('pk', flat=True) for item in self.items.all()))
        except:
            return StockItem.objects.filter(pk = 0)
        else:
            return StockItem.objects.filter(pk__in=stockItem)
        
    def get_percent_executed(self):
        """Returns percent of execution"""
        return sum(item.get_percent_executed() for item in self.items.all()) / self.items.count()
    
    def has_waybill_creation_permission(self, user):
        return (not hasattr(user, 'person') or user.person.dispatch) and self.warehouse.persons.filter(pk=user.pk).exists()

    def is_expired(self):
        """Checks expiration of order"""
        return self.expiry < date.today()

    def is_executed(self):
        """Checks completion of order"""
        return self.percentage == 100

class OrderItem(models.Model):
    """
    Order item with commodity and counters
        - **order** -- identifier in COMPAS
        - **lti_id** -- LTI identifier
        - **si_code** -- shipping order code
        - **project_number** -- project number
        - **commodity** -- commodity of item
        - **number_of_units** -- number of units
        - **unit_weight_net** -- weight net of one unit in kg
        - **unit_weight_gross** -- weight gross of one unit in kg
        - **total_weight_net** -- total weight net of item in ton
        - **total_weight_gross** -- total weight gross of item in ton
    """
    
    order = models.ForeignKey(Order, verbose_name=_("Order"), related_name="items")
    
    lti_id = models.CharField(_("LTI ID"), max_length=40, db_index=True)
    si_code = models.CharField( _("Shipping Order Code"), max_length=8, db_index=True)
    project_number = models.CharField(_("Project Number"), max_length = 24, blank=True, db_index=True) #project_wbs_element
    commodity = models.ForeignKey(Commodity, verbose_name=_("Commodity"), related_name="order_items")
    
    number_of_units = models.IntegerField(_("Number of Units"), db_index=True)
    
    unit_weight_net = models.DecimalField(_("Unit weight net"), max_digits=12, decimal_places=3, 
                                          editable=False, blank=True, null=True)
    unit_weight_gross = models.DecimalField(_("Unit weight gross"), max_digits=12, decimal_places=3, 
                                            editable=False, blank=True, null=True)
    
    total_weight_net = models.DecimalField(_("Total weight net"), max_digits=12, decimal_places=3,
                                           editable=False, blank=True, null=True)
    total_weight_gross = models.DecimalField(_("Total weight gross"), max_digits=12, decimal_places=3,
                                             editable=False, blank=True, null=True)
    
    class Meta:
        ordering = ('si_code',)
        verbose_name = _("order item")
        verbose_name_plural = _("order items")
    
    def  __unicode__( self ):
        return u"%s -  %.0f " % ( self.commodity, self.tonnes_left() )


    def stock_items(self):
        """Retrieves stock items for current order item through warehouse"""
        return StockItem.objects.filter(
                        warehouse=self.order.warehouse,
                        project_number=self.project_number,
                        si_code=self.si_code, 
                        commodity=self.commodity,
                        ).order_by('-number_of_units')
    
    
    @staticmethod
    def sum_number(queryset, field_name='number_of_units'):
        return queryset.aggregate(field_sum=Sum(field_name))['field_sum'] or 0
        

    def get_similar_dispatches(self):
        """Returns all loading details with such item within any orders"""
        return LoadingDetail.objects.filter(waybill__transport_dispach_signed_date__isnull=False, 
                                            waybill__date_removed__isnull=True,
                                            stock_item__in=self.stock_items(),
                                            ).order_by('-waybill__dispatch_date')
    
    def get_order_dispatches(self):
        """Returns dispatches of current order"""
        return self.get_similar_dispatches().filter(waybill__order=self.order)
    
    
    def get_available_stocks(self):
        """Calculates available stocks"""
        return self.sum_number(self.stock_items()) \
             - self.sum_number(self.get_similar_dispatches().filter(waybill__sent_compas__isnull=True))

    def get_available_stocks_mt(self):
        """Calculates available stocks"""
        return self.sum_number(self.stock_items(), 'quantity_net')

    def get_dispatched_not_yet_counted_of_stock(self):
        """Calculates available stocks"""
        return self.sum_number(self.get_similar_dispatches().filter(waybill__sent_compas__isnull=True), 'total_weight_net')
        
    def get_percent_executed(self):
        """Calculates percent for executed"""
        return self.total_weight_net and round(100 * self.sum_number(self.get_order_dispatches(), 'total_weight_net') / self.total_weight_net) or 0
        
    def items_left( self ):
        """Calculates number of such items supposed to be delivered in this order"""
        return max(0, self.number_of_units - self.sum_number(self.get_order_dispatches()))

    def tonnes_left( self ):
        """Calculates number of such items supposed to be delivered in this order"""
        return max(0, self.total_weight_net - self.sum_number(self.get_order_dispatches(), 'total_weight_net'))
    

def waybill_slug_populate(waybill):
    #Calculate number of similar waybills to ensure uniqueness even for deleted ones
    count = Waybill.objects.all_with_deleted().filter(order__warehouse__compas=waybill.order.warehouse.compas, 
                                                      date_created__year=waybill.date_created.year
                                                      ).count()
    return "%s%s%s%06d" % (waybill.order.warehouse.compas.pk, waybill.date_created.strftime('%y'), 
                           LETTER_CODE, count+1)

class Waybill( ld_models.Model ):
    """
    Base waybill abstract class
        - **slug** -- unique identifier for waybill
        - **order** -- LTI identifier
        - **destination** -- destination warehouse
        - **loading_date** -- date of load
        - **dispatch_date** -- date of dispatch
        - **transaction_type** -- type of transaction
        - **transport_type** -- type of transport
        - **dispatch_remarks** -- some description for dispatch
        - **dispatcher_person** -- foreign key to person which create dispatch
        - **receipt_remarks** -- some description for receipt
        - **receipt_person** -- foreign key to person which received
        - **total_weight_gross** -- toatal weight graoss
        - **container_one_number** -- number of first container
        - **container_two_number** -- number of second container
        - **container_one_seal_number** -- seal number of first container
        - **container_two_seal_number** -- seal number of second container
        - **container_one_remarks_dispatch** -- some description for dispatch of first container
        - **container_two_remarks_dispatch** -- some description for dispatch of second container
        - **container_one_remarks_reciept** -- some description for receipt of first container
        - **container_two_remarks_reciept** -- some description for receipt of second container
        - **arrival_date** -- date of arrival
        - **start_discharge_date** -- date of discharging start
        - **end_discharge_date** --date of discharging end
        - **distance** -- distance covered in km
        - **transport_dispach_signed_date** -- date of confirmation of dispatch
        - **receipt_warehouse** -- receipt warehouse
        - **receipt_signed_date** -- date of confirmation of receipt
        - **validated** -- validation of dispatch eWaybill
        - **sent_compas** -- date of sending dispatch eWaybill to Compas
        - **receipt_validated** -- validation of receipt eWaybill
        - **receipt_sent_compas** -- date of sending receipt eWaybill to Compas
        - **barcode** -- barcode
    """
    
    INTERNAL_TRANSFER = u'WIT'
    DELIVERY = u'DEL'
    DISTIBRUTION= u'DIS'
    SHUNTING= u'SHU'
    
    TRANSACTION_TYPES = ( 
                        ( INTERNAL_TRANSFER, _(u'WFP Internal Transfer') ),
                        ( DELIVERY, _( u'Delivery' )),
                        #( u'SWA', _(u'Swap' )),
                        #( u'REP', _(u'Repayment' )),
                        #( u'SAL', _(u'Sale' )),
                        (DISTIBRUTION, _(u'Distribution' )),
                        #( u'LON', _(u'Loan' )),
                        ( u'DSP', _(u'Disposal' )),
                        ( u'PUR', _(u'Purchase' )),
                        (SHUNTING, _(u'Shunting' )),
                )
    TRANSPORT_TYPES = ( 
                        ( u'02', _(u'Road' )),
                        ( u'01', _(u'Rail' )),
                        ( u'04', _(u'Air' )),
                        #( u'I', _(u'Inland Waterways' )),
                        #( u'C', _(u'Costal Waterways' )),
                        #( u'07', _(u'Multi-mode' )),
#                        (u'O', _(u'Other Please Specify'))
                )
    
    NEW = 1
    SIGNED = 2
    SENT = 3
    INFORMED = 4
    DELIVERED = 5
    COMPLETE = 6
    
    slug = AutoSlugField(populate_from=waybill_slug_populate, unique=True, 
                         slugify=capitalize_slug(slugify),
                         sep='', primary_key=True)
    
    order = models.ForeignKey(Order, verbose_name=_("Order"), related_name="waybills")
    
    destination = models.ForeignKey(Warehouse, verbose_name=_("Destination Warehouse"), blank=True, null=True, related_name="receipt_waybills")
    receipt_warehouse = models.ForeignKey(Warehouse, verbose_name=_("Receiving Warehouse"), blank=True, null=True, related_name="receipt_waybills2")
    #Dates
    loading_date = models.DateField(_("Loading Date"), default=datetime.now, db_index=True) #dateOfLoading
    dispatch_date = models.DateField( _("Dispatch Date"), default=datetime.now, db_index=True) #dateOfDispatch
    
    transaction_type = models.CharField(_("Transaction Type"), max_length=10, 
                                         choices=TRANSACTION_TYPES, default=TRANSACTION_TYPES[0][0]) #transactionType
    transport_type = models.CharField(_("Transport Type"), max_length=10, 
                                      choices=TRANSPORT_TYPES, default=u'02') #transportType
    
    #Dispatcher
    dispatch_remarks = models.TextField(_("Dispatch Remarks"), blank=True)
    dispatcher_person = models.ForeignKey(Person, verbose_name=_("Dispatch person"), 
                                          related_name="dispatch_waybills") #dispatcherName
    
    #Recepient
    receipt_person =  models.ForeignKey(Person, verbose_name=_("Recipient person"), 
                                        related_name="recipient_waybills", 
                                        blank=True, null=True) #recipientName
    receipt_remarks = models.TextField(_("Receipt Remarks"), blank=True) #recipientRemarks
    
    #Transporter
    transport_sub_contractor = models.CharField(_("Transport Sub Contractor"), max_length=40, blank=True) #transportSubContractor
    transport_driver_name = models.CharField(_("Driver Name"), max_length=40) #transportDriverName
    transport_driver_licence = models.CharField(_("Driver License or National ID"), max_length=40) #transportDriverLicenceID
    transport_vehicle_registration = models.CharField(_("Vehicle Registration"), max_length=40) #transportVehicleRegistration
    transport_trailer_registration = models.CharField( _("Trailer Registration"), max_length=40, blank=True) #transportTrailerRegistration

    #Container        
    container_one_number = models.CharField(_("Container One Number"), max_length=40, blank=True) #containerOneNumber
    container_two_number = models.CharField( _("Container Two Number"), max_length=40, blank=True) #containerTwoNumber
    container_one_seal_number = models.CharField(_("Container One Seal Number"), max_length=40, blank=True) #containerOneSealNumber
    container_two_seal_number = models.CharField(_("Container Two Seal Number"), max_length=40, blank=True ) #containerTwoSealNumber
    container_one_remarks_dispatch = models.CharField( _("Container One Dispatch Remarks"), max_length=40, blank=True) #containerOneRemarksDispatch
    container_two_remarks_dispatch = models.CharField( _("Container Two Dispatch Remarks"), max_length=40, blank=True) #containerTwoRemarksDispatch
    container_one_remarks_reciept = models.CharField( _("Container One Receipt Remarks"), max_length=40, blank=True) #containerOneRemarksReciept
    container_two_remarks_reciept = models.CharField(_("Container Two Receipt Remarks"), max_length=40, blank=True) #containerTwoRemarksReciept

    arrival_date = models.DateField(_("Arrival Date"), blank=True, null=True) #recipientArrivalDate
    start_discharge_date = models.DateField(_("Start Unloading Date"), blank=True, null=True) #recipientStartDischargeDate
    end_discharge_date = models.DateField(_("End Unloading Date"), blank=True, null=True) #recipientEndDischargeDate

    distance = models.IntegerField(_("Distance Covered (km)"), blank=True, null=True) #recipientDistance
    
    transport_dispach_signed_date = models.DateTimeField( _("Transport Dispach Signed Date"), null=True, blank=True, db_index=True) #transportDispachSignedTimestamp
    receipt_signed_date = models.DateTimeField(_("Recipient Signed Date"), blank=True, null=True, db_index=True) #recipientSignedTimestamp
    
    validated = models.BooleanField( _("eWaybill Validated"), default=False, db_index=True) #waybillValidated
    sent_compas = models.DateTimeField(_("eWaybill Sent to Compas"), blank=True, null=True, db_index=True)
    
    receipt_validated = models.BooleanField(_("eWaybill Receipt Validated"), default=False, db_index=True) #waybillReceiptValidated
    receipt_sent_compas = models.DateTimeField(_("eWaybill Reciept Sent to Compas"), blank=True, null=True, db_index=True)
    
    barcode = models.ImageField(_("Image"), upload_to=lambda instance, file_name: instance.default_update_to(file_name),
                       blank=True, null=True,
                       max_length=255, editable=False)
    
    objects = ld_models.managers.LogicalDeletedManager()
    
    class Meta:
        ordering = ('slug',)
        verbose_name = _("waybill")
        verbose_name_plural = _("waybills")
    
    def  __unicode__( self ):
        return self.slug
    
    def default_update_to(self, file_name):
        return 'uploads/waybills/%s/%s/%s' % (
                    self.order.pk, self.slug, file_name
        )
    
    @models.permalink
    def get_absolute_url(self):
        return ('waybill_view', (), {'waybill_pk': self.pk})
    
    def save(self, force_insert=False, force_update=False, using=None):
        self.date_modified = datetime.now()
        if self.pk:
            self.barcode.save("%s.gif" % self.pk, self.barcode_qr(), save=False)
        super(Waybill, self).save(force_insert=force_insert, force_update=force_update, using=using)
        if not self.barcode:
            self.barcode.save("%s.gif" % self.pk, self.barcode_qr(), save=False)
            super(Waybill, self).save(force_insert=force_insert, force_update=force_update, using=using)

    def regenerate_bc(self):
            self.barcode.save("%s.gif" % self.pk, self.barcode_qr(), save=False)
        
    def clean(self):
        """Validates Waybill instance. Checks different dates"""
        if self.loading_date > self.dispatch_date:
            raise ValidationError(_("Cargo Dispatched before being Loaded"))

        if self.order.dispatch_date and self.loading_date < self.order.dispatch_date:
            raise ValidationError(_("Loading date should not be prior to the requested dispatch date"))
        
        #If second container exists, first must exist also
        if self.container_two_number and not self.container_one_number:
            raise ValidationError(_("Type container 1 number"))
        
        if self.arrival_date and self.arrival_date < self.dispatch_date:
            raise ValidationError(_("Cargo arrived before being dispatched"))

        if self.start_discharge_date and self.arrival_date \
        and self.start_discharge_date < self.arrival_date:
            raise ValidationError(_("Cargo Discharge started before Arrival?"))

        if self.start_discharge_date and self.end_discharge_date \
        and self.end_discharge_date < self.start_discharge_date:
            raise ValidationError(_("Cargo finished Discharge before Starting?"))

        if self.transaction_type not in [self.DELIVERY, self.DISTIBRUTION] and not self.destination:
            raise ValidationError(_("Choose Destination Warehouse or another Transaction Type"))
    
    def dispatch_sign(self):
        """Signs the waybill as ready to be sent."""
        self.transport_dispach_signed_date = datetime.now()
        self.save()
    
    def receipt_sign(self):
        """Signs the receipt waybill as ready to be sent."""
        if self.is_received():
            
            self.receipt_signed_date = datetime.now()
            self.save()
            
            #Create virtual stock item
            for item in self.loading_details.all():
                filters = {
                    'warehouse': self.receipt_warehouse,
                    'project_number': item.stock_item.project_number,
                    'si_code': item.stock_item.si_code, 
                    'commodity': item.stock_item.commodity,
                }
                if not StockItem.objects.filter(**filters).exists():
                    filters.update({
                        'external_ident': "%s%s" % (self.receipt_warehouse, item.stock_item.pk),
                        'quality': item.stock_item.quality,
                        'package': item.stock_item.package,
                        'number_of_units': item.number_of_units,
                        'unit_weight_net': item.stock_item.unit_weight_net, 
                        'unit_weight_gross': item.stock_item.unit_weight_gross, 
                        'is_bulk': item.stock_item.is_bulk,
                        'si_record_id': item.stock_item.si_record_id,
                        'origin_id': item.stock_item.origin_id,
                        'allocation_code': item.stock_item.allocation_code,
                        'virtual': True,
                        'quantity_net':item.total_weight_net_received,
                        'quantity_gross':item.total_weight_gross_received
                        
                    }) 
                    StockItem.objects.create(**filters)
                
    def serialize(self):
        """
        This method serializes the Waybill with related LoadingDetails, LtiOriginals and EpicStocks.
    
        @param self: the Waybill instance
        @return the serialized json data.
        """
        
        return serializers.serialize('json', chain((self,), self.loading_details.all()), use_decimal=False)
    
    
    def compress(self):
        """
        This method compress the Waybill using zipBase64 algorithm.
    
        @param self: the Waybill instance
        @return: a string containing the compressed representation of the Waybill with items
        """
        #Collect all related objects
        objects = set([
            #Waybill itself
            self, 
            
            #Dispatch person
            self.dispatcher_person, self.dispatcher_person.location, 
            self.dispatcher_person.organization, self.dispatcher_person.compas,
            
            #Order
            self.order, self.order.location, self.order.consignee, 
            
            #Warehouse
            self.order.warehouse, self.order.warehouse.compas, 
            self.order.warehouse.location, self.order.warehouse.organization,

        ])
        
        if self.receipt_person:
            objects.update((
                self.receipt_person, self.receipt_person.location, 
                self.receipt_person.organization, self.receipt_person.compas,
            ))
        if self.destination:
            objects.update((
                self.destination, self.destination.location,
                self.destination.organization, self.destination.compas,
            ))
        if self.receipt_warehouse:
            objects.update((
                self.receipt_warehouse, self.receipt_warehouse.location,
                self.receipt_warehouse.organization, self.receipt_warehouse.compas,
            ))
        
        #Loading details
        for ld in self.loading_details.select_related():
            objects.update((
                ld, ld.stock_item, ld.stock_item.package, 
                ld.stock_item.commodity, ld.stock_item.commodity.category,
            ))
            if ld.units_damaged_reason:
                objects.update((ld.units_damaged_reason, ld.units_damaged_reason.category,))
            if ld.units_lost_reason:
                objects.update((ld.units_lost_reason, ld.units_lost_reason.category,))
        
        #Serialize
        data = serializers.serialize('json', filter(None, objects), use_decimal=False)
        
        return compress_json(data)
        
    
    @classmethod
    def decompress(cls, data):
        wb_serialized = decompress_json(data)

        if wb_serialized:
            waybill = None
            for obj in serializers.deserialize("json", wb_serialized, parse_float=decimal.Decimal):
                #Save object if it does not exist
                if not obj.object.__class__.objects.filter(pk=obj.object.pk).exists():
                    obj.save()
                        
                #Remember waybill instance to return from the method
                if isinstance(obj.object, cls):
                    waybill = obj.object
            
            return waybill
                    
    def barcode_qr(self):
        """Bar code generator. This view uses 'pyqrcode' for back-end. It returns image file in response."""
        
        file_out = cStringIO.StringIO()
        
        image = pyqrcode.MakeQRImage(self.compress(), minTypeNumber=40,
                                     errorCorrectLevel=pyqrcode.QRErrorCorrectLevel.L,
                                      block_in_pixels=1)
        image.save(file_out, 'GIF')
        file_out.reset()
        
        return ContentFile(file_out.read())
    
    def get_nocached_barcode(self):
        """Returns full barcode url and prevents cache"""
        return "%s?hash=%s" % (self.barcode.url, random.random())
    
    @classmethod
    def dispatches(cls, user):
        """Returns all loaded but not signed waybills, and related to user"""
        return cls.objects.filter(transport_dispach_signed_date__isnull = True,
                                  order__warehouse__persons__pk = user.pk)


    @classmethod
    def receptions(cls, user):
        """Returns all waybills, that can be received, and related to user"""
        return cls.objects.filter(transport_dispach_signed_date__isnull = False, 
                                  receipt_signed_date__isnull = True,
                                  destination__persons__pk = user.pk)

    def get_shortage_loading_details(self):
        return [loading_detail for loading_detail in self.loading_details.all() if loading_detail.get_shortage()]   
    
    def is_received(self):
        return all(d.is_received() for d in self.loading_details.all()) and self.receipt_person is not None
    
    def has_receive_permission(self, user):
        return (not hasattr(user, 'person') or user.person.receive) and Waybill.receptions(user).filter(pk=self.pk).exists()
    
    def has_dispatch_permission(self, user):
        return (not hasattr(user, 'person') or user.person.dispatch) and Waybill.dispatches(user).filter(pk=self.pk).exists()

    def has_delete_permission(self, user):
        is_dispatcher = self.dispatcher_person.username == user.username
        is_compas_here = self.order.warehouse.compas.officers.filter(username=user).exists()
        can_delete = is_dispatcher or is_compas_here
        return (not hasattr(user, 'person') or can_delete) and Waybill.dispatches(user).filter(pk=self.pk).exists()
    

class LoadingDetail(models.Model):
    """
    Loading details related to dispatch waybill
        - **waybill** -- foreign key to parent waybill
        - **slug** -- simplified and encoded title for proper URL
        - **stock_item** -- foreign key to related stock item
        - **number_of_units** -- number of units
        - **unit_weight_net** -- weight net of one unit in kg
        - **unit_weight_gross** -- weight gross of one unit in kg
        - **total_weight_net** -- ordered total weight net of item in ton
        - **total_weight_gross** -- ordered total weight gross of item in ton
        - **total_weight_net_received** -- received total weight net in ton
        - **total_weight_gross_received** -- received total weight gross in ton
        - **number_units_good** -- number of good delivered units
        - **number_units_lost** -- number of lost delivered units
        - **number_units_damaged** -- number of damaged delivered units
        - **units_lost_reason** -- cause of lost items
        - **units_damaged_reason** -- cause of damaged items
        - **overloaded_units** -- the existence of overloaded units
        - **over_offload_units** -- the existence of over offloaded units
    """
    waybill = models.ForeignKey(Waybill, verbose_name=_("eWaybill Number"), related_name="loading_details")
    slug = AutoSlugField(populate_from='waybill', unique=True, sep='', editable=True, primary_key=True)
    
    #Stock data
    stock_item = models.ForeignKey(StockItem, verbose_name=_("Stock item"), related_name="dispatches")
    
    number_of_units = models.IntegerField(_("Number of Units"), db_index=True)
    
    unit_weight_net = models.DecimalField(_("Unit weight net"), max_digits=12, decimal_places=3, default=0)
    unit_weight_gross = models.DecimalField(_("Unit weight gross"), max_digits=12, decimal_places=3, default=0)
    
    total_weight_net = models.DecimalField(_("Total weight net"), max_digits=12, decimal_places=5, default=0)
    total_weight_gross = models.DecimalField(_("Total weight gross"), max_digits=12, decimal_places=5, default=0)
    
    total_weight_net_received = models.DecimalField(_("Total weight net received"), 
                                                    max_digits=12, decimal_places=3, default=0)

    total_weight_gross_received = models.DecimalField(_("Total Weight Gross Received"), 
                                                    max_digits=12, decimal_places=3, default=0)
    
    #Number of delivered units
    number_units_good = models.DecimalField(_("Units (Good)"), default=0, 
                                            max_digits=12, decimal_places=3) #numberUnitsGood
    number_units_lost = models.DecimalField(_("Units (Lost)"), default=0, 
                                            max_digits=12, decimal_places=3 ) #numberUnitsLost
    number_units_damaged = models.DecimalField(_("Units (Damaged)"), default=0, 
                                               max_digits=12, decimal_places=3 ) #numberUnitsDamaged
    
    #Net Delivered items
    received_net_lost = models.DecimalField(_("Net (Lost)"), default=0, 
                                            max_digits=12, decimal_places=3 ) #numberUnitsLost
    received_net_damaged = models.DecimalField(_("Net (Damaged)"), default=0, 
                                               max_digits=12, decimal_places=3 ) #numberUnitsDamaged

    #Gross Delivered items
    received_gross_lost = models.DecimalField(_("Gross (Lost)"), default=0, 
                                         max_digits=12, decimal_places=3 ) #numberUnitsLost
    received_gross_damaged = models.DecimalField(_("Gross (Damaged)"), default=0, 
                                               max_digits=12, decimal_places=3 ) #numberUnitsDamaged
    
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

    class Meta:
        ordering = ('slug',)
        verbose_name = _("loading detail")
        verbose_name_plural = _("waybill items")
        unique_together = ('waybill', 'stock_item')


    def get_shortage( self ):
        """Returns shortage for item"""
        not_validated_sum = LoadingDetail.objects.filter(stock_item=self.stock_item, 
                                                         waybill__validated=False, 
                                                         waybill__transport_dispach_signed_date__isnull=False,
                                                         waybill__date_removed__isnull=True)\
                                .aggregate(Sum('number_of_units'))['number_of_units__sum']
        return max(0, not_validated_sum - self.stock_item.number_of_units)

    def get_order_item(self):
        """Retrieves stock items for current order item through warehouse"""
        return self.stock_item.get_order_item(self.waybill.order.pk)
    
    def calculate_net_received_good( self ):
        """Returns weight net for good units"""
        if self.total_weight_net_received:
            return self.total_weight_net_received
        else:
            return ( self.number_units_good * self.unit_weight_net ) / 1000

    def calculate_gross_received_good( self ):
        """Returns weight gross for good units"""
        if self.total_weight_net_received:
            return self.total_weight_gross_received
        else:
            return ( self.number_units_good * self.unit_weight_gross ) / 1000

    def calculate_net_received_damaged( self ):
        """Returns weight net for damaged units"""
        if self.received_net_damaged:
            return self.received_net_damaged
        else:
            return ( self.number_units_damaged * self.unit_weight_net ) / 1000

    def calculate_gross_received_damaged( self ):
        """Returns weight gross for damaged units"""
        if self.received_gross_damaged:
            return self.received_gross_damaged
        else:
            return ( self.number_units_damaged * self.unit_weight_gross ) / 1000

    def calculate_net_received_lost( self ):
        """Returns weight net for lost units"""
        if self.received_net_lost:
            return self.received_net_lost
        else:
            return ( self.number_units_lost * self.unit_weight_gross ) / 1000

    def calculate_gross_received_lost( self ):
        """Returns weight gross for good units"""
        if self.received_gross_lost:
            return self.received_gross_lost
        else:
            return ( self.number_units_lost * self.unit_weight_gross ) / 1000
    
    def calculate_total_received_units( self ):
        """Returns total count of received units"""
        return self.number_units_good + self.number_units_damaged


    def calculate_total_received_net( self ):
        """Returns total weight net for received units"""
        
        return ( self.calculate_net_received_good() + self.calculate_net_received_damaged()).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)

    def calculate_total_received_gross( self ):
        """Returns total weight gross for received units"""
        return (self.calculate_gross_received_good() + self.calculate_gross_received_damaged()).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)
    
    def  __unicode__( self ):
        return "%s - %s - %s" % (self.waybill, self.stock_item.si_code, self.number_of_units)
    
    def is_received(self):
        """Checks for receipt completion of item"""
        if self.over_offload_units:
            return self.number_of_units <= self.number_units_good + self.number_units_damaged + self.number_units_lost
        else:
            return self.number_of_units == self.number_units_good + self.number_units_damaged + self.number_units_lost 
                
    def clean(self):
        """Validates LoadingDetail instance."""
        super(LoadingDetail, self).clean()

        #clean number of items
        if self.number_of_units \
        and (self.number_units_good or self.number_units_damaged or self.number_units_lost) \
        and (self.number_of_units > self.number_units_good + self.number_units_damaged + self.number_units_lost):
            raise ValidationError(_("%(loaded).3f Units loaded but %(offload).3f units accounted for") % {
                    "loaded" : self.number_of_units, 
                    "offload" : self.number_units_good + self.number_units_damaged + self.number_units_lost 
            })
        
        #Dispath: overloaded units and changed weights
        if self.stock_item_id and not self.waybill.transport_dispach_signed_date:
            order_item = self.get_order_item()
#            if order_item.items_left() < self.number_of_units and not self.overloaded_units:
#                raise ValidationError(_("Overloaded for %.3f units") % (self.number_of_units - order_item.items_left(),))
            
            #available_stocks = order_item.get_available_stocks_mt() - order_item.get_dispatched_not_yet_counted_of_stock()
            available_stocks = order_item.tonnes_left()
            if available_stocks < self.total_weight_net and not self.overloaded_units:
                raise ValidationError(_("Overloaded for %.3f tons") % (self.total_weight_net - available_stocks))
            
            if self.overloaded_units and not self.waybill.dispatch_remarks:
                raise ValidationError(_("Since you set 'overloaded' flag 'Dispatch Remarks' field becomes required."))
            
            if self.unit_weight_net != self.stock_item.unit_weight_net and not self.waybill.dispatch_remarks:
                raise ValidationError(_("Since you changed unit weight net 'Dispatch Remarks' field becomes required."))
            
            if self.unit_weight_gross != self.stock_item.unit_weight_gross and not self.waybill.dispatch_remarks:
                raise ValidationError(_("Since you changed unit weight gross 'Dispatch Remarks' field becomes required."))
            
            #expected_total_net = (self.stock_item.unit_weight_net * self.number_of_units / 1000).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)
            #if self.total_weight_net != expected_total_net and not self.waybill.dispatch_remarks:
            #    raise ValidationError(_("Since you changed total weight net 'Dispatch Remarks' field becomes required."))
            
            expected_total_gros = (self.stock_item.unit_weight_gross * self.number_of_units / 1000).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_HALF_UP)
            if self.total_weight_gross != expected_total_gros and not self.waybill.dispatch_remarks:
                raise ValidationError(_("Since you changed total weight gross 'Dispatch Remarks' field becomes required."))
    
        #overloaded units for reception
        total = self.number_units_good + self.number_units_damaged + self.number_units_lost
        if self.number_of_units and total > self.number_of_units and not self.over_offload_units:
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
        
        #Total received weight net
        if self.total_weight_net_received != self.calculate_total_received_net() and not self.waybill.receipt_remarks:
            raise ValidationError(_("Since you changed total weight net 'Recipient Remarks' field becomes required."))

        #Total received weight gross
        if self.total_weight_gross_received != self.calculate_total_received_gross() and not self.waybill.receipt_remarks:
            raise ValidationError(_("Since you changed total weight gross 'Recipient Remarks' field becomes required."))
            
        
class ImportLogger(models.Model):
    """
    Logger for import operation
        - **compas** -- foreign key to COMPAS which received data
        - **when_attempted** -- time of action
        - **status** -- status of action in result
        - **message** -- description of error
    """
    
    SUCCESS = 0
    FAILURE = 1
    
    STATUSES = (
        (SUCCESS, _("Success")),
        (FAILURE, _("Failure"))
    )
    
    compas = models.ForeignKey(Compas, verbose_name=_("COMPAS"), related_name="import_logs")
    when_attempted = models.DateTimeField(_("when attempted"), default=datetime.now, db_index=True)
    status = models.IntegerField(_("status"), choices=STATUSES, default=SUCCESS, db_index=True)
    message = models.TextField(_("error message"), blank=True)
    
    class Meta:
        ordering = ('-when_attempted',)
        verbose_name = _("COMPAS import logger")
        verbose_name_plural = _("COMPAS import log")
    
    def __unicode__(self):
        return "%s: %s" % (self.get_status_display(), self.message)


class CompasLogger(models.Model):
    """
    Logger for sending to compas
        - **action** -- action type
        - **compas** -- foreign key to COMPAS which received waybill
        - **waybill** -- foreign key to sended waybill
        - **when_attempted** -- time of action
        - **status** -- status of action in result
        - **message** -- description of error
    """
    
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
    waybill = models.ForeignKey(Waybill, verbose_name=_("eWaybill"), related_name="compass_loggers")
    when_attempted = models.DateTimeField(_("when attempted"), default=datetime.now, db_index=True)
    status = models.IntegerField(_("status"), choices=STATUSES, default=SUCCESS)
    message = models.TextField(_("error message"))
    
    class Meta:
        ordering = ('-when_attempted',)
        verbose_name = _("COMPAS logger")
        verbose_name_plural = _("COMPAS log")
    
    def __unicode__(self):
        return "%s: %s" % (self.get_status_display(), self.message)
