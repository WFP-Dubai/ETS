from datetime import datetime, timedelta, date
from itertools import chain, izip
import decimal
from functools import wraps
import cStringIO as StringIO
import ho.pisa as pisa
from cgi import escape
import os.path

from django.template.loader import get_template, render_to_string
from django.template import Context
from django.conf import settings
from django.http import HttpResponse
from django.db import connections, transaction, models
from django.db.models import Q
from django.db.utils import DatabaseError
from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.core.exceptions import ValidationError
from django.core import serializers
from django.utils.translation import ugettext as _
from django.utils.decorators import available_attrs
from django.template import RequestContext

from compas.utils import call_db_procedure, reduce_compas_errors
import compas.models as compas_models
import models as ets_models
from ets.compress import compress_json, decompress_json

TOTAL_WEIGHT_METRIC = 1000
DEFAULT_ORDER_LIFE = getattr(settings, 'DEFAULT_ORDER_LIFE', 3)


def render_to_pdf(request, template_name, context, file_name):
    """Renders template with context to HTML, than to PDF"""
    
    context_dict = {"STATIC_URL": settings.STATIC_URL}
    context_dict.update(context)
    
    html = render_to_string(template_name, context_dict, RequestContext(request))
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode('utf-8')), 
                            result, debug=True, encoding='utf-8', show_error_as_pdf=True,
                            link_callback=fetch_resources, xhtml=False)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % file_name
        return response
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def fetch_resources(uri, rel):
    """
    Callback to allow pisa/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.STATIC_URL):
        path = os.path.abspath(os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, "")))
    elif uri.startswith(settings.MEDIA_URL):
        path = os.path.abspath(os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, "")))
    else:
        path = uri
    return path


def compas_importer(func=None, log_success=False):
    """ Decorator to wrap method that imports data from COMPAS. In case of error Importlogger object is created. """
    def _decorator(f):
        @wraps(f, assigned=available_attrs(func))
        def _wrapped(using):
            try: 
                with transaction.commit_on_success(using) as tr:
                    f(using)
            except Exception, err:
                ets_models.ImportLogger.objects.create(compas_id=using, 
                                                       status=ets_models.ImportLogger.FAILURE, 
                                                       message="%s: %s" % (f.__name__, unicode(err)))
                raise
        
        return _wrapped
    
    if func:
        return _decorator(func)
    
    return _decorator
    
    

def update_compas(using):
    """ Utility to run whole import process. If no fails Success ImportLogger is created."""
    try:
        #Import organizations
        #import_partners(using)
        
        #Update places
        #import_places(using)
        
        #Update persons
        import_persons(using)
        
        #Update loss, damage reasons
        #import_reasons(using)
        
        #Update stocks
        import_stock(using)
    
        #Update orders
        import_order(using)
        
    except Exception:
        #Since we already created log for this error simply pass here
        pass
    else:
        #If all process did not fail create success log
        ets_models.ImportLogger.objects.create(compas_id=using)

def update_compas_info(using):
    """ Utility to run special import process. If no fails Success ImportLogger is created."""
    try:
        #Import organizations
        import_partners(using)
        
        #Update places
        import_places(using)
                
        #Update loss, damage reasons
        import_reasons(using)
        
    except Exception:
        #Since we already created log for this error simply pass here
        pass
    else:
        #If all process did not fail create success log
        ets_models.ImportLogger.objects.create(compas_id=using)
       

def _get_places(compas):
    warehouses = tuple(ets_models.Warehouse.objects.filter(compas__pk=compas, start_date__lte=date.today)\
                                            .values_list('pk', flat=True))
    
    return compas_models.Place.objects.using(compas).filter(reporting_code=compas, org_code__in=warehouses)

@compas_importer
def import_partners(compas):
    """Imports organizations from COMPAS"""
    for partner in compas_models.Partner.objects.using(compas).all():
        ets_models.Organization.objects.get_or_create(code=partner.id, defaults={'name': partner.name})

@compas_importer
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
        }
        
        wh, created = ets_models.Warehouse.objects.get_or_create(code=place.org_code, defaults=defaults)
        
        if valid_warehouse != wh.valid_warehouse:
        	wh.valid_warehouse = valid_warehouse
        	wh.save()
        
        if not created and not wh.compas and compas:
            wh.compas = compas
            wh.save()


@compas_importer
def import_persons(compas):
    """Imports persons from COMPAS"""
    
    now = datetime.now()
    places = ets_models.Location.objects.all()#.filter(reporting_code=compas)
	#fix filtering #
	#expand it to do it lighter
    for person in compas_models.CompasPerson.objects.using(compas).filter(org_unit_code=compas, 
                                        location_code__in=places.values_list('code', flat=True)):
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
        
           
        for wh in ets_models.Warehouse.objects.filter(
                                               organization=p.organization, 
                                               location=p.location):
            p.warehouses.add(wh)
        
        p.updated = now
        p.save()
    
    #Disable deleted persons
    ets_models.Person.objects.filter(compas__pk=compas).exclude(updated=now).update(is_active=False)


@compas_importer
def import_reasons(compas):
    """Imports all possible loss/damage reasons"""
    return ets_models.LossDamageType.update(compas)


@compas_importer
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
            
            'updated': now,
        }
        
        rows = ets_models.StockItem.objects.filter(external_ident=stock.wh_pk, quality=stock.qualitycode).update(**defaults)
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
    country_code = places.count() and places[0].country_code or None
        
    #Get or Create location
    return ets_models.Location.objects.get_or_create(pk=code, defaults={
                    'name': name, 
                    'country': country_code
                    })[0]


@compas_importer
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
        
        
def send_dispatched(waybill, compas=None):
    """Submits dispatched and validated waybills to COMPAS"""
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
                
                call_db_procedure('write_waybill.dispatch', (
                    CURR_CODE, 
                    waybill.dispatch_date.strftime("%Y%m%d"), 
                    waybill.order.origin_type, 
                    waybill.order.warehouse.location.pk, 
                    waybill.order.warehouse.pk,
                    waybill.order.warehouse.name, 
                    waybill.order.location.pk,
                    waybill.destination.pk,
                    order_item.lti_id, 
                    waybill.loading_date.strftime("%Y%m%d"),
                    waybill.order.consignee.pk, 
                    
                    waybill.transaction_type, 
                    waybill.transport_vehicle_registration,
                   #waybill.transport_trailer_registration,
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
                    
                    waybill.destination.compas.pk,
                    
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
        waybill.save()
    else:
        ets_models.CompasLogger.objects.create(action=ets_models.CompasLogger.DISPATCH, 
                                               compas_id=compas, waybill=waybill,
                                               status=ets_models.CompasLogger.SUCCESS)
        
        waybill.sent_compas = datetime.now()
        waybill.save()
        

def send_received(waybill, compas=None):
    """Submits received and validated waybills to COMPAS"""
    if not compas:
        compas = waybill.destination.compas.pk
    
    try:
        with transaction.commit_on_success(using=compas) as tr:
            CURR_CODE = waybill.pk[len(compas):]

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
    
    waybill.save()
            

def changed_fields(model, next, previous, exclude=()):
    for field in model._meta.fields:
        if previous is not None \
        and getattr(next, field.name) != getattr(previous, field.name) \
        and field.name not in exclude:
            yield field.verbose_name, getattr(next, field.name)
    
    
def history_list(log_queryset, model, exclude=()):
    """Utility to generate history of actions at some objects"""
    ACTIONS = {
        'I': _('Created'),
        'U': _('Changed'),
        'D': _('Deleted'),
    }
    
    for next, prev in izip(log_queryset, chain(log_queryset[1:], (None,))):
        yield next.action_user, ACTIONS[next.action_type], next.action_date, changed_fields(model, next, prev, exclude)


def data_to_file_response(data, file_name):
    """Creates response with provided data and inserts Content-Disposition header with file name."""
    response = HttpResponse(data, content_type='application/data')
    response['Content-Disposition'] = 'attachment; filename=%s.data' % file_name
    return response


def import_file(f):
    """Reads file, decompresses serialized data,deserializes it and saves objects"""
    #File is supposed to be small (< 4Mb)
    
    data = decompress_json(f.read())
    total = 0
    
    for obj in serializers.deserialize("json", data, parse_float=decimal.Decimal):
        obj.save()
        total += 1
    
    return total


def get_compas_data(compas=None):
    """Fetches all COMPAS-imported data, serializes and compresses them"""
    
    #COMPAS stations themself
    compas_stations = ets_models.Compas.objects.all() 
    if compas is not None:
        compas_stations = ets_models.Compas.objects.filter(pk=compas)
    
    
    warehouses = ets_models.Warehouse.objects.filter(Q(end_date__gt=date.today) | Q(end_date__isnull=True), 
                                        start_date__lte=date.today, 
                                        compas__in=compas_stations)
    return chain(
        ets_models.Organization.objects.all(),
        ets_models.Location.objects.all(),
        ets_models.LossDamageType.objects.all(),
        ets_models.Commodity.objects.all(),
        ets_models.CommodityCategory.objects.all(),
        ets_models.Package.objects.all(),
        
        compas_stations,
        warehouses,
        ets_models.Person.objects.filter(warehouses__pk=warehouses.values_list('pk', flat=True)),
        ets_models.StockItem.objects.filter(warehouse__in=warehouses),
        ets_models.Order.objects.filter(expiry__lte=date.today, warehouse__in=warehouses),
        ets_models.OrderItem.objects.filter(order__expiry__lte=date.today, order__warehouse__in=warehouses),
    )

def compress_compas_data(compas=None):

    data = get_compas_data(compas)
    return compress_json( serializers.serialize('json', data, use_decimal=False) )
