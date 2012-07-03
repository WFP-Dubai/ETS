from datetime import datetime, timedelta, date
from itertools import chain
import decimal, copy
from functools import wraps

from django.conf import settings
from django.http import HttpResponse
from django.db import transaction, models
from django.db.models import Q
from django.db.models.aggregates import Max
from django.core.exceptions import ValidationError
from django.core import serializers
from django.utils.translation import ugettext as _
from django.utils.decorators import available_attrs
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_unicode
from django.core.cache import cache
from django.contrib.admin.models import LogEntry
from django.http import QueryDict
from django.core.urlresolvers import reverse

from compas.utils import call_db_procedure, reduce_compas_errors, get_version
import compas.models as compas_models
import models as ets_models
from ets.compress import compress_json, decompress_json
from ets.datatables import get_sorted_columns, get_searchable_columns, get_search_filter

TOTAL_WEIGHT_METRIC = 1000
DEFAULT_ORDER_LIFE = getattr(settings, 'DEFAULT_ORDER_LIFE', 3)

LOGENTRY_CREATE_WAYBILL = 1
LOGENTRY_EDIT_DISPATCH = 21
LOGENTRY_EDIT_RECEIVE = 22
LOGENTRY_SIGN_DISPATCH = 4
LOGENTRY_SIGN_RECEIVE = 5
LOGENTRY_DELETE_WAYBILL = 3
LOGENTRY_VALIDATE_DISPATCH = 6
LOGENTRY_VALIDATE_RECEIVE = 7

ACTION_TYPES = (
    (LOGENTRY_CREATE_WAYBILL, _("Created dispatch waybill")),
    (LOGENTRY_EDIT_DISPATCH, _("Edited dispatch waybill")),
    (LOGENTRY_DELETE_WAYBILL, _("Deleted dispatch waybill")),
    (LOGENTRY_SIGN_DISPATCH, _("Signed dispatch waybill")),
    (LOGENTRY_EDIT_RECEIVE, _("Edited receive waybill")),
    (LOGENTRY_SIGN_RECEIVE, _("Signed receive waybill")),
    (LOGENTRY_VALIDATE_DISPATCH, _("Validated dispatch waybill")),
    (LOGENTRY_VALIDATE_RECEIVE, _("Validated receive waybill")),
)

LOGENTRY_WAYBILL_ACTIONS = dict(ACTION_TYPES)

def get_dispatch_compas_filters(user):
    """filter for dispatch waybills prepared for sending to COMPAS"""
    return {
        "transport_dispach_signed_date__isnull": False, 
        "sent_compas__isnull": True, 
        "order__warehouse__compas__officers__pk": user.pk
    }

def get_receipt_compas_filters(user):
    """filter for receipt waybills prepared for sending to COMPAS"""
    return {
        "transport_dispach_signed_date__isnull": False, 
        "receipt_signed_date__isnull": False, 
        "receipt_sent_compas__isnull": True,
        #"sent_compas__isnull": False, 
        "destination__compas__officers__pk": user.pk
    }


def filter_for_orders():
    """filter for not expired and not executed orders"""
    return {
        "expiry__gt": (datetime.now() - timedelta(days=settings.ORDER_SHOW_AFTER_EXP_DAYS)),
        "percentage__lt": 100,
    }

def _get_places(compas):
    warehouses = tuple(ets_models.Warehouse.objects.filter(compas__pk=compas, start_date__lte=date.today)\
                                            .values_list('pk', flat=True))

    return compas_models.Place.objects.using(compas).filter(reporting_code=compas, org_code__in=warehouses)

def import_partners(compas):
    """Imports organizations from COMPAS"""
    for partner in compas_models.Partner.objects.using(compas).all():
        ets_models.Organization.objects.get_or_create(code=partner.id, defaults={'name': partner.name})

def import_places(compas):
    """Imports warehouses with locations from COMPAS"""
    for place in compas_models.Place.objects.using(compas):

        #Create location
        location, created = ets_models.Location.objects.get_or_create(code=place.geo_point_code, defaults={
            'name': place.geo_name,
            'country': place.country_code,
        })


        #Set country if it's null
        if not created and location.country is None:
            location.country = place.country_code
            location.save()

        compas_text = place.reporting_code

        try:
            compas = ets_models.Compas.objects.get(pk=place.reporting_code)
        except ets_models.Compas.DoesNotExist:
            compas = None


        valid_warehouse = True
        if place.compas_indicator == 'T':
            valid_warehouse = False

        #Update warehouse
        defaults = {
            'name': place.name,
            'location': location,
            'organization': ets_models.Organization.objects.get_or_create(code=place.organization_id)[0] if place.organization_id else None,
            'compas': compas,
            'valid_warehouse': valid_warehouse,
            'compas_text':compas_text,
        }

        wh, created = ets_models.Warehouse.objects.get_or_create(code=place.org_code, defaults=defaults)

        if valid_warehouse != wh.valid_warehouse:
            wh.valid_warehouse = valid_warehouse
            wh.save()
        if wh.compas_text != compas_text:
            wh.compas_text = compas_text
            wh.save()

        if not created and not wh.compas and compas:
            wh.compas = compas
            wh.save()


def import_persons(compas):
    """Imports persons from COMPAS"""

    now = datetime.now()
    places = compas_models.Place.objects.using(compas)#.filter(reporting_code=compas)
    #fix filtering #
    #expand it to do it lighter
    for person in compas_models.CompasPerson.objects.using(compas).filter(org_unit_code=compas, 
                                        location_code__in=places.values_list('geo_point_code', flat=True)):
        try:
            p = ets_models.Person.objects.get(code=person.code, compas__pk=person.org_unit_code)
            if not p.organization_id:
                if p.organization_id != person.organization_id:
                    p.organization_id = person.organization_id
                    p.save()
        except ets_models.Person.DoesNotExist:
            p = ets_models.Person(title=person.title,
                                   code=person.code, compas_id=person.org_unit_code, 
                                   organization_id=person.organization_id, 
                                   location_id=person.location_code, username=person.person_pk, 
                                   email=person.email,
                                   first_name = person.first_name, last_name = person.last_name, 
                                   is_staff=True, is_active=False, is_superuser=False)
            p.set_password(person.person_pk)

            p.save()
            
        p.updated = now
        p.save()

    #Disable deleted persons
    ets_models.Person.objects.filter(compas__pk=compas).exclude(updated=now).update(is_active=False)


def import_reasons(compas):
    """Imports all possible loss/damage reasons"""
    return ets_models.LossDamageType.update(compas)


def import_stock(compas):
    """Imports stock items or updates quantity"""

    now = datetime.now()
    ## Why places from compas and not from locations
    places = _get_places(compas)

    for stock in compas_models.EpicStock.objects.using(compas)\
                    .filter(wh_code__in=places.values_list('org_code', flat=True)):

        #Create commodity's category
        category = ets_models.CommodityCategory.objects.get_or_create(pk=stock.comm_category_code)[0]

        #Create commodity
        commodity = ets_models.Commodity.objects.get_or_create(pk=stock.commodity_code, defaults={
            'name': stock.cmmname,
            'category': category, 
        })[0]

        #Create package
        package = ets_models.Package.objects.get_or_create(pk=stock.package_code, 
                                                           defaults={'name': stock.packagename})[0]

        #Check package type. If 'BULK' then modify number and weight
        number_of_units = stock.quantity_net*TOTAL_WEIGHT_METRIC if stock.is_bulk() \
                                else stock.number_of_units

        quantity_net =  stock.quantity_net
        quantity_gross = stock.quantity_gross


        warehouse = ets_models.Warehouse.objects.get(pk=stock.wh_code)

        defaults = {
            'warehouse': warehouse,
            'project_number': stock.project_wbs_element,
            'si_code': stock.si_code,
            'commodity': commodity,
            'package': package,
            'number_of_units': number_of_units,
            'unit_weight_net': number_of_units and TOTAL_WEIGHT_METRIC*stock.quantity_net/number_of_units,
            'unit_weight_gross': number_of_units and TOTAL_WEIGHT_METRIC*stock.quantity_gross/number_of_units,

            'allocation_code': stock.allocation_code,
            'si_record_id': stock.si_record_id,
            'origin_id': stock.origin_id,
            'is_bulk': stock.is_bulk(),
            'quantity_net': quantity_net,
            'quantity_gross': quantity_gross,
            'updated': now,
        }

        rows = ets_models.StockItem.objects.filter(external_ident=stock.wh_pk, 
                                                    quality=stock.qualitycode).update(**defaults)
        if not rows:

            #Clean virtual stocks
            ets_models.StockItem.objects.filter(warehouse=warehouse, project_number=stock.project_wbs_element,
                                                si_code=stock.si_code, commodity=commodity,
                                                virtual=True).delete()

            ets_models.StockItem.objects.create(external_ident=stock.wh_pk, quality=stock.qualitycode, **defaults)

    #Flush empty stocks
    ets_models.StockItem.objects.filter(number_of_units__gt=0, warehouse__compas__pk=compas, virtual=False)\
                                .exclude(updated=now).update(number_of_units=0)


def _get_destination_location(compas, code, name):
    """Finds or creates a location by code and name"""
    places = compas_models.Place.objects.using(compas).filter(geo_point_code=code)
    country_code = places.exists() and places[0].country_code or None

    #Get or Create location
    return ets_models.Location.objects.get_or_create(pk=code, defaults={
                    'name': name, 
                    'country': country_code
                    })[0]


def import_order(compas):
    """Imports all LTIs from COMPAS"""
    now = datetime.now()
    today = date.today()
    places = _get_places(compas)
    
    for lti_code in tuple(compas_models.LtiOriginal.objects.using(compas).distinct()\
                        .filter(models.Q(expiry_date__gte=today) | models.Q(expiry_date__isnull=True),
                                lti_date__gte=date(year=2012, month=1, day=1),
                                origin_wh_code__in=places.values_list('org_code', flat=True),
                                )\
                        .values_list('code', flat=True)):
        order_items = []
        for lti in compas_models.LtiOriginal.objects.using(compas).filter(code=lti_code):
            #Create Order
            defaults = {
                'created': lti.lti_date,
                'expiry': lti.expiry_date or lti.lti_date + timedelta(30*DEFAULT_ORDER_LIFE),
                'dispatch_date': lti.requested_dispatch_date,
                'transport_code': lti.transport_code,
                'transport_ouc': lti.transport_ouc,
                'transport_name': lti.transport_name,
                'origin_type': lti.origin_type,
                'warehouse': ets_models.Warehouse.objects.get(code=lti.origin_wh_code),
                'consignee': ets_models.Organization.objects.get(pk=lti.consegnee_code),
                'location': _get_destination_location(compas, lti.destination_location_code, lti.destination_loc_name),
                'updated': now,
                'remarks': lti.remarks,
                'remarks_b': lti.remarks_b,
            }

            order, created = ets_models.Order.objects.get_or_create(code=lti.code, defaults=defaults)

            #Update order. IT's not supposed to happen. In this case system might break.
            if not created:
                ets_models.Order.objects.filter(code=lti.code).update(**defaults)

            #Commodity
            commodity = ets_models.Commodity.objects.get_or_create(pk=lti.commodity_code, defaults={
                'name': lti.cmmname,
                'category': ets_models.CommodityCategory.objects.get_or_create(pk=lti.comm_category_code)[0],
            })[0]

            #Create order item
            key_data = {
                'order': order,
                'si_code': lti.si_code,
                'commodity': commodity,
                'lti_id': lti.lti_id,
                'project_number': lti.project_wbs_element,
            }
            defaults = {
                'number_of_units': lti.number_of_units,
                'unit_weight_net': lti.unit_weight_net,
                'unit_weight_gross': lti.unit_weight_gross,
                'total_weight_net': lti.quantity_net,
                'total_weight_gross': lti.quantity_gross,
            }

            order_item, created = ets_models.OrderItem.objects.get_or_create(defaults=defaults, **key_data)

            if not created:
                ets_models.OrderItem.objects.filter(**key_data).update(**defaults)

            order_items.append(order_item.pk)

        #Emptying deleted order items
        ets_models.OrderItem.objects.filter(order__code=lti_code).exclude(pk__in=order_items).update(number_of_units=0, total_weight_net=0, total_weight_gross=0)
        #check missing
        #get all orders lti_ids filter by compas
        #order_items = ets_models.OrderItem.filter(order__warehouse__compas__pk = compas)


def send_dispatched(waybill, compas=None, cache_prefix='send_dispatched'):
    """Submits dispatched and validated waybills to COMPAS"""
    cache_key = "%s_%s" % (cache_prefix, waybill.pk)
    sending = cache.get(cache_key, False)
    if sending:
        return
    
    cache.set(cache_key, True)
    
    if not compas:
        compas = waybill.order.warehouse.compas.pk
    try:
        with transaction.commit_on_success(using=compas) as tr:
            CURR_CODE = waybill.pk[len(compas):]



            CONTAINER_NUMBER = waybill.container_one_number

            special_case = waybill.loading_details.count() == 2 and waybill.container_two_number
            code_letter = u'A'

            for index, loading in enumerate( waybill.loading_details.all() ):

                if special_case:
                    CURR_CODE = u"%s%s" % (code_letter, waybill.pk)
                    code_letter = u'B'
                    if index == 1:
                        CONTAINER_NUMBER = waybill.container_two_number

                is_bulk = loading.stock_item.is_bulk

                try:
                    order_item = loading.get_order_item()
                except ets_models.OrderItem.DoesNotExist:
                    raise ValidationError("System can not find order item. Check database.")
                try:
                    DestCompas = waybill.destination.compas.pk
                except:
                    try:
                        DestCompas = waybill.destination.compas_text
                    except:
                        DestCompas = ''
                try:
                    Destination = waybill.destination.pk
                except:
                    Destination = ''

                IsValid = False
                if order_item.lti_id != 1:
                    if bool(compas_models.LtiOriginal.objects.using(compas).filter(lti_id = order_item.lti_id)):
                        IsValid = True
                    else:
                        IsValid = False
                else:
                    IsValid = False

                if not IsValid:
                    message = "The LTI %s is not available in the COMPAS Station %s"%( waybill.order.code, compas)
                    waybill.validated = False
                    waybill.save()
                    raise ValidationError(message)
                    return 

                call_db_procedure('write_waybill.dispatch', (
                    CURR_CODE, 
                    waybill.dispatch_date.strftime("%Y%m%d"), 
                    waybill.order.origin_type, 
                    waybill.order.warehouse.location.pk, 
                    waybill.order.warehouse.pk,
                    waybill.order.warehouse.name, 
                    waybill.order.location.pk,
                    Destination,
                    order_item.lti_id, 
                    waybill.loading_date.strftime("%Y%m%d"),
                    waybill.order.consignee.pk, 

                    waybill.transaction_type, 
                    waybill.transport_vehicle_registration,
                    waybill.transport_trailer_registration,
                    waybill.transport_type,
                    waybill.dispatch_remarks, 

                    waybill.dispatcher_person.code, 
                    waybill.dispatcher_person.compas.pk, 
                    waybill.dispatcher_person.title, 

                    waybill.order.transport_code, 
                    waybill.order.transport_ouc,

                    waybill.transport_driver_name, 
                    waybill.transport_driver_licence,

                    CONTAINER_NUMBER,

                    DestCompas,

                    loading.stock_item.origin_id, 
                    loading.stock_item.commodity.category.pk, 
                    loading.stock_item.commodity.pk, 
                    loading.stock_item.package.pk, 
                    loading.stock_item.allocation_code, 
                    loading.stock_item.quality,

                    u'%.3f' % loading.total_weight_net, 
                    u'%.3f' % loading.total_weight_gross, 
                    u'%.3f' % (1 if is_bulk else loading.number_of_units), 
                    u'%.3f' % (1 if is_bulk else loading.unit_weight_net), 
                    u'%.3f' % (1 if is_bulk else loading.unit_weight_gross), 

                    None, #p_odaid
                    None, #p_losstype
                    None, #p_lossreason
                    '', #p_loannumber
                ), compas)

    except Exception, err:

        message = hasattr(err, 'messages') and u"\n".join(err.messages) or unicode(err)
        for error_message in reduce_compas_errors(message):
            ets_models.CompasLogger.objects.create(action=ets_models.CompasLogger.DISPATCH, 
                                                   compas_id=compas, waybill=waybill,
                                                   status=ets_models.CompasLogger.FAILURE, 
                                                   message=error_message)
        waybill.validated = False
    else:
        ets_models.CompasLogger.objects.create(action=ets_models.CompasLogger.DISPATCH, 
                                               compas_id=compas, waybill=waybill,
                                               status=ets_models.CompasLogger.SUCCESS)

        waybill.sent_compas = datetime.now()
        
        return True
    
    finally:
        waybill.save()
        cache.set(cache_key, False)

def send_received(waybill, compas=None, cache_prefix='send_received'):
    """Submits received and validated waybills to COMPAS"""
    cache_key = "%s_%s" % (cache_prefix, waybill.pk)
    sending = cache.get(cache_key, False)
    if sending:
        return
    
    cache.set(cache_key, True)
    
    if not compas:
        compas = waybill.destination.compas.pk

    try:
        with transaction.commit_on_success(using=compas) as tr:
            CURR_CODE = waybill.pk[len(compas):]

            ## Check if dispatch_master is there...
            if not compas_models.DispatchMaster.objects.using(compas) \
                                .filter(code__contains=waybill.pk, destination_code=waybill.destination.pk) \
                                .exists():  
                #Push dispatched waybill to COMPAS station 
                if not send_dispatched(waybill, compas) and not send_dispatched(waybill, waybill.destination.compas):
                    raise ValidationError(_("The Dispatch %s is not available in the COMPAS Station %s") % ( waybill.pk, compas))
                
                
            ## check if containers = 2 & lines = 2
            special_case = waybill.loading_details.count() == 2 and waybill.container_two_number
            code_letter = u'A'

            for loading in waybill.loading_details.all():

                if special_case:
                    CURR_CODE = u"%s%s" % (code_letter, waybill.pk)
                    code_letter = u'B'

                call_db_procedure('write_waybill.receipt', (
                    CURR_CODE, 
                    waybill.receipt_person.compas.pk, 
                    waybill.receipt_person.code, 
                    waybill.arrival_date.strftime("%Y%m%d"),

                    loading.number_units_good and u'%.3f' % loading.number_units_good or None,
                    loading.units_damaged_reason and loading.units_damaged_reason.cause or None, 
                    loading.number_units_damaged and u'%.3f' % loading.number_units_damaged or None, 
                    loading.units_lost_reason and loading.units_lost_reason.cause or None, 
                    loading.number_units_lost and u'%.3f' % loading.number_units_lost or None, 

                    loading.stock_item.origin_id, 
                    loading.stock_item.commodity.category.pk,
                    loading.stock_item.commodity.pk, 
                    loading.stock_item.package.pk, 
                    loading.stock_item.allocation_code, 
                    loading.stock_item.quality
                ), compas)

    except Exception, err:
        message = hasattr(err, 'messages') and u"\n".join(err.messages) or unicode(err)
        ets_models.CompasLogger.objects.create(action=ets_models.CompasLogger.RECEIPT, 
                                               compas_id=compas, waybill=waybill,
                                               status=ets_models.CompasLogger.FAILURE, 
                                               message=message)

        waybill.receipt_validated = False
    else:
        ets_models.CompasLogger.objects.create(action=ets_models.CompasLogger.RECEIPT, 
                                               compas_id=compas, waybill=waybill,
                                               status=ets_models.CompasLogger.SUCCESS)

        waybill.receipt_sent_compas = datetime.now()
        
        return True
    finally:
        waybill.save()
        cache.set(cache_key, False)


def changed_fields(model, next, previous, exclude=()):
    """Detects changed fields"""
    for field in model._meta.fields:
        if previous is not None \
        and getattr(next, field.name) != getattr(previous, field.name) \
        and field.name not in exclude:
            yield field.verbose_name, getattr(next, field.name)


def get_compases(user):
    """Returns user's related compases"""
    queryset = ets_models.Compas.objects.all()
    if not user.is_superuser:
        queryset = queryset.filter(Q(warehouses__persons__pk=user.id) | Q(officers__pk=user.id))
        
    return queryset


def data_to_file_response(data, file_name, type):
    """Creates response with provided data and inserts Content-Disposition header with file name."""
    response = HttpResponse(data, content_type='application/%s' % type)
    response['Content-Disposition'] = 'attachment; filename=%s.%s' % (file_name, type)
    return response


def import_file(f):
    """Reads file, decompresses serialized data,deserializes it and saves objects"""
    #File is supposed to be small (< 4Mb)

    data = decompress_json(f.read())
    total = 0

    for obj in serializers.deserialize("json", data, parse_float=decimal.Decimal):
        if "LogEntry" == obj.object._meta.object_name:
            if not LogEntry.objects.filter(content_type__id=ContentType.objects.get_for_model(ets_models.Waybill).pk,
                                                   action_time=obj.object.action_time,
                                                   user=obj.object.user,
                                                   object_id=obj.object.object_id).exists():
                obj.object.pk = None
                models.Model.save_base(obj.object, raw=True, force_insert=True)
        else:    
            obj.save()
        total += 1

    return total


def get_compas_data(compas=None, warehouse=None):
    """Fetches all COMPAS-imported data"""

    #COMPAS stations themself
    compas_stations = ets_models.Compas.objects.all() 
    if compas is not None:
        compas_stations = ets_models.Compas.objects.filter(pk=compas)

    if warehouse:
        compas_stations = compas_stations.filter(pk=warehouse.compas.pk)

    warehouses = ets_models.Warehouse.objects.filter(Q(end_date__gt=date.today) | Q(end_date__isnull=True), 
                                        start_date__lte=date.today, 
                                        compas__in=compas_stations)

    if warehouse:
        warehouses = warehouses.filter(pk=warehouse.pk)

    persons = ets_models.Person.objects.filter(warehouses__pk=warehouses.values_list('pk', flat=True))

    return chain(
        ets_models.Organization.objects.all(),
        ets_models.Location.objects.all(),
        ets_models.LossDamageType.objects.all(),
        ets_models.Commodity.objects.all(),
        ets_models.CommodityCategory.objects.all(),
        ets_models.Package.objects.all(),

        compas_stations,
        warehouses,
        persons,
        User.objects.filter(pk__in=persons.values_list('pk', flat=True)),
        ets_models.StockItem.objects.filter(warehouse__in=warehouses),
        ets_models.Order.objects.filter(expiry__gte=date.today, warehouse__in=warehouses),
        ets_models.OrderItem.objects.filter(order__expiry__gte=date.today, order__warehouse__in=warehouses),
    )

def compress_compas_data(compas=None, warehouse=None):
    """Returns compressed and serialized data for compas, warehouse"""
    data = get_compas_data(compas, warehouse)
    return compress_json( serializers.serialize('json', data, use_decimal=False) )


def get_date_from_string(some_date, date_templates=None, default=None, message="Failed: date must be in one of such formats"):
    """Extracts date from string"""
    DATE_FORMATS = (
        "%Y-%m-%d",
    )
    
    def extract_date_by_template(some_date, date_template):
        try:
            return datetime.strptime(some_date, date_template), True 
        except:
            return None, False

    def get_results(result, flag, iterable=False):
        if flag:
            pass
        elif default:
            result = default
        else:
            templates = "; ".join([item.replace('%', "") for item in date_templates]) if iterable else date_templates.replace('%', "")
            result = " ".join([message, templates])
        return result, flag
    
    if date_templates is None:
        date_templates = DATE_FORMATS
    elif isinstance(some_date, str):
        return get_results(extract_date_by_template(some_date, date_templates))
    elif getattr(date_templates, '__iter__', False):
        return "date_templates must be a string or list of strings", False

    for template in date_templates:
        result, flag = extract_date_by_template(some_date, template)
        if flag:
            return get_results(result, flag)
    return get_results(None, False, iterable=True)


def create_logentry(request, obj, flag, message=""):
    """Creates log entry"""
    if flag in (LOGENTRY_EDIT_DISPATCH, LOGENTRY_EDIT_RECEIVE, 
                LOGENTRY_VALIDATE_DISPATCH, LOGENTRY_VALIDATE_RECEIVE):
        message = "%s: %s" % (LOGENTRY_WAYBILL_ACTIONS[flag], message)
    elif not message:
        message = LOGENTRY_WAYBILL_ACTIONS[flag]
        
    LogEntry.objects.log_action(
        user_id = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id = obj.pk,
        object_repr = force_unicode(obj),
        action_flag = flag,
        change_message = message
    )


def construct_change_message(request, form, formsets):
    """
    Construct a change message from a changed object.
    """
    change_message = []
    if form.changed_data:
        change_message.append(_('Changed %s.') % ", ".join(['"%s": %s' % (field, form.cleaned_data[field]) for field in form.changed_data]))

    if formsets:
        for formset in formsets:
            for added_object in formset.new_objects:
                change_message.append(_('Added %(name)s "%(object)s".')
                                      % {'name': force_unicode(added_object._meta.verbose_name),
                                         'object': force_unicode(added_object)})
            for changed_object, changed_fields in formset.changed_objects:
                change_message.append(_('Changed %(list)s for %(name)s "%(object)s".')
                                      % {'list': ", ".join(['"%s": %s' % (field, getattr(changed_object, field)) for field in changed_fields]),
                                         'name': force_unicode(changed_object._meta.verbose_name),
                                         'object': force_unicode(changed_object)})
            for deleted_object in formset.deleted_objects:
                change_message.append(_('Deleted %(name)s "%(object)s".')
                                      % {'name': force_unicode(deleted_object._meta.verbose_name),
                                         'object': force_unicode(deleted_object)})
    change_message = ' '.join(change_message)
    return change_message or _('No fields changed.')

def get_api_url(request, column_index_map, url_name, url_params=None, request_params=None):
    """Returns url with datatables filters"""
    data_format = request.GET.get('data_format', '')
    if data_format:
        _url_params = url_params or {}
        params = QueryDict('', mutable=True)
        searchable_columns = get_searchable_columns(request, column_index_map, len(column_index_map))
        sortable_columns = get_sorted_columns(request, column_index_map)
        params.update(request_params or {})
        params.update({ 'sSearch': request.GET.get('sSearch', '').encode('utf-8') })
        params.setlist('sortable', list(set(sortable_columns)))
        params.setlist('searchable', list(set(searchable_columns)))
        if data_format == 'excel':
            _url_params.update({'format': data_format})
        redirect_url = "?".join([reverse(url_name, kwargs=_url_params), params.urlencode()])
        return redirect_url

def get_datatables_filtering(request, queryset):
    """Datatables filtering with searchable and sortable fields"""
    search_string = request.GET.get("search_string", "")
    if search_string:
        queryset = queryset.filter(pk__icontains=search_string)
    sortable_columns = request.GET.getlist('sortable')
    if sortable_columns:
        queryset = queryset.order_by(*sortable_columns)
    sortable_columns = request.GET.getlist('searchable')
    filtering = get_search_filter(request, sortable_columns)
    if filtering:
        queryset = queryset.filter(filtering)
    return queryset
