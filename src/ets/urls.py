from datetime import datetime, timedelta, date
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail, object_list
from django.utils.translation import ugettext_lazy, ugettext as _
from django.db.models.aggregates import Count
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.db import models
from django.views.static import serve
from django.contrib import admin #@Reimport
admin.autodiscover()

serve.authentication = False

from ets.forms import WaybillSearchForm, WaybillScanForm
from ets.models import Waybill
from ets.views import waybill_list, waybill_reception, ImportData, table_waybills, table_compas_waybills
from ets.decorators import receipt_view, dispatch_view, person_required, warehouse_related, receipt_compas, officer_required
from ets.decorators import officer_required, waybill_user_related, waybill_officer_related, dispatcher_required, recipient_required
import ets.models

dated =  datetime.now() - timedelta( days = 10 )
urlpatterns = patterns("ets.views",

    ( r'^$', direct_to_template, {
        'template': 'index.html',
        'extra_context': {'form_scan': WaybillScanForm, 'form': WaybillSearchForm },
    }, "index"),
    
    #Order list
    ( r'^orders/$', person_required(direct_to_template), {
        'template': 'order/list.html',
    }, "orders"),
    ( r'^datatables/orders/$', "table_orders", {
        'queryset': ets.models.Order.objects.all().order_by('-created')
    }, "table_orders"),
    
    #Order detail
    ( r'^order/(?P<object_id>[-\w]+)/$', object_detail, {
        'queryset': ets.models.Order.objects.all().order_by('-created'),
        'template_name': 'order/detail.html',
    }, "order_detail" ),
    
    #Create waybill                   
    ( r'^order/(?P<order_pk>[-\w]+)/add/$', "waybill_create", {
        'queryset': ets.models.Order.objects.all(),
        'template': 'waybill/create.html',
    }, "waybill_create" ),
    
    #Waybill pages

    ( r'^datatables/waybills/(?P<filtering>dispatches)/$', dispatch_view(table_waybills), {}, "table_waybills" ),
    ( r'^datatables/waybills/(?P<filtering>receptions)/$', receipt_view(table_waybills), {}, "table_waybills" ),
    ( r'^datatables/waybills/(?P<filtering>user_related)/$', waybill_user_related(table_waybills), {
        'queryset': ets.models.Waybill.objects.all(),
    }, "table_waybills" ),
                       
    #Listings
    ( r'^search/$', "waybill_search", {}, "waybill_search" ),
    
    ( r'^dispatch/$', dispatcher_required(direct_to_template), {
        "template": 'waybill/list2.html',
        "extra_context": {
            "extra_title": _("eWaybills Waiting For Dispatch Signature"),
            "ajax_source_url": "/datatables/waybills/dispatches/"
        }
    }, "waybill_dispatch_list" ),
    ( r'^receive/$', recipient_required(direct_to_template), {
        "template": 'waybill/list2.html',
        "extra_context": {
            "extra_title": _("Expected Consignments"),
            "ajax_source_url": "/datatables/waybills/receptions/"
        }
    }, "waybill_reception_list" ),

    ( r'^waybill/(?P<scanned_code>[-+=/\w]+)/scanned_receive/$', "waybill_reception_scanned", {
        'queryset': ets.models.Waybill.objects.filter(transport_dispach_signed_date__isnull=False,
                                                      receipt_signed_date__isnull=True)
    }, "waybill_reception_scanned"),

    ( r'^waybill/(?P<waybill_pk>[-\w]+)/$', 'waybill_view', {
        "template": 'waybill/detail.html',
        'queryset': ets.models.Waybill.objects.all(),
    }, "waybill_view" ),
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/simple/$', 'waybill_view', {
        "template": 'waybill/print/detail.html',
        'queryset': ets.models.Waybill.objects.all(),
    }, "waybill_view_simple" ),
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+).pdf$', 'waybill_pdf', {
        "template": 'waybill/print/detail.html',
        'queryset': ets.models.Waybill.objects.all(),
    }, "waybill_pdf" ),
    
    #Dispatch
    ( r'^order/(?P<order_pk>[-\w]+)/(?P<waybill_pk>[-\w]+)/$', "waybill_dispatch_edit", {
        'template': 'waybill/edit.html',
    }, "waybill_edit" ),
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/sign_dispatch/$', "waybill_finalize_dispatch", {
        'template_name': 'waybill/print/detail.html',
    }, "waybill_finalize_dispatch" ),
    
    #Reception pages
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/receive/$', recipient_required(receipt_view(waybill_reception)), 
      {}, "waybill_reception"),
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/sign_receipt/$', "waybill_finalize_receipt", {
        'template_name': 'waybill/print/detail.html',
    }, "waybill_finalize_receipt" ),
    
    #Validation pages
    
    ( r'^validate_dispatch/(?P<waybill_pk>[-\w]+)/$', "validate_dispatch", {
        'queryset': ets.models.Waybill.objects.all(),
    }, "validate_dispatch" ),
    ( r'^validate_receipt/(?P<waybill_pk>[-\w]+)/$', "validate_receipt", {
        'queryset': ets.models.Waybill.objects.all(),
    }, "validate_receipt" ),
    
    
    ( r'^dispatch_validates/$', 'dispatch_validates', {
        'template': 'validate/dispatch.html',
        'queryset': ets.models.Waybill.objects.all(),
    }, "dispatch_validates" ),
    ( r'^receipt_validates/$', 'receipt_validates', {
        'template': 'validate/receipt.html',
        'queryset': ets.models.Waybill.objects.all(),
    }, "receipt_validates" ),

    ( r'^datatables/waybills/(?P<filtering>validate_dispatch)/$', 'table_validate_waybills', {
        "queryset": ets.models.Waybill.objects.filter(validated=False)
    }, "table_validate_waybill" ),
    ( r'^datatables/waybills/(?P<filtering>validate_receipt)/$', 'table_validate_waybills', {
        "queryset": ets.models.Waybill.objects.filter(receipt_validated=False),
    }, 'table_validate_waybill' ),
    ( r'^datatables/waybills/(?P<filtering>dispatch_validated)/$', 'table_validate_waybills', {
        "queryset": ets.models.Waybill.objects.filter(validated=True)
    }, "table_validate_waybill" ),
    ( r'^datatables/waybills/(?P<filtering>receipt_validated)/$', 'table_validate_waybills', {
        "queryset": ets.models.Waybill.objects.filter(receipt_validated=True),
    }, 'table_validate_waybill' ),
    
    #Submit waybills to compas
    ( r'^send_dispatched/$', 'send_dispatched_view', {
        'queryset': ets.models.Waybill.objects.filter(validated=True),
    }, "send_dispatched" ),
    ( r'^send_received/$', 'send_received_view', {
        'queryset': ets.models.Waybill.objects.filter(receipt_validated=True),
    }, "send_received" ),
    
    #Delete functionality
    ( r'^waybill/delete/(?P<waybill_pk>[-\w]+)/(?P<redirect_to>[-\w]+)/$', 
      "waybill_delete", {}, "waybill_delete" ),
    ( r'^waybill/delete/(?P<waybill_pk>[-\w]+)/$', "waybill_delete", {}, "waybill_delete" ),
 
    ( r'^compas_waybill_receipt/$', officer_required(direct_to_template), {
        "template": 'compas/list_waybills_compas_all2.html',
        "extra_context": {
            "extra_title": _("Received"),
            "ajax_source_url": "/datatables/waybills/compas_receipt/"
    }}, "compas_waybill_receipt" ),
    ( r'^datatables/waybills/(?P<filtering>compas_receipt)/$', 'table_compas_waybills', {
        "queryset": Waybill.objects.filter(receipt_sent_compas__isnull=False)
    }, "table_compass_waybill" ),

    ( r'^datatables/waybills/(?P<filtering>compas_dispatch)/$', 'table_compas_waybills', {
        "queryset": Waybill.objects.filter(sent_compas__isnull=False),
    }, 'table_compass_waybill' ),
    ( r'^compas_waybill/$', officer_required(direct_to_template), {
        "template": 'compas/list_waybills_compas_all2.html',
        "extra_context": {
            "ajax_source_url": "/datatables/waybills/compas_dispatch/"
    }}, 'compas_waybill' ),


    ( r'^warehouses/$', direct_to_template, { "template": 'stock/warehouses.html' }, 'warehouses_list'),
    ( r'^stocks/(?P<object_id>[-\w]+)/$', object_detail, {
        "queryset": ets.models.Warehouse.get_active_warehouses(),
        "template_name": 'stock/stock_list.html',
        "extra_context": {
            "good_quality": ets.models.StockItem.GOOD_QUALITY_LABEL,
    }}, 'stock_list'),
    ( r'^datatables/warehouses/$', 'table_warehouses', {
        'queryset': ets.models.Warehouse.get_active_warehouses(),
    }, 'table_warehouses' ),
    ( r'^datatables/stock/param/(?P<param_name>[-\w]+)/$', 'table_stock_items', {}, 'table_stock_items' ),
    ( r'^datatables/stock/(?P<warehouse_pk>[-\w]+)/$', 'table_stock_items', {}, 'table_stock_items' ),
    ( r'^stock/$', 'stock_items', {
        'queryset': ets.models.Warehouse.get_active_warehouses(),
        'template_name': 'stock/stocklist.html',
    }, 'view_stock' ),

    ( r'^get_stock_data_li/(?P<order_pk>[-\w]+)/$', "get_stock_data_li", {
        'queryset': ets.models.StockItem.objects.all().distinct(),
    }, "get_stock_data_li" ),
             

    ( r'^get_stock_data/(?P<order_pk>[-\w]+)/$', "get_stock_data", {
        'queryset': ets.models.StockItem.objects.all().distinct(),
    }, "get_stock_data" ),
             
    ( r'^waybill/report/select/$', "direct_to_template", {
        "template": 'reporting/select_report.html',
    }, "select_report" ),
                        
    ( r'^waybill_deserialize/$', "deserialize", {}, "deserialize" ),

    ( r'^waybill_errors/(?P<waybill_pk>[-\w]+)/(?P<logger_action>[-\w]+)/$', "waybill_errors", {}, "waybill_errors"),

    ( r'^qrcode/(?P<waybill_pk>[-\w]+).jpg$', "barcode_qr", {}, "barcode_qr" ),
     ( r'^sync_compas/$', "sync_compas", {}, "sync_compas"),
    ( r'^sync_compas/(?P<compas_pk>[-\w]+)/$', "handle_sync_compas", {
        'queryset': ets.models.Compas.objects.all(),
    }, "handle_sync_compas"),
                       
    ( r'^import_data/$', officer_required(ImportData.as_view()), {}, "import_file" ),
    ( r'^export/compas/(?P<data_type>data)/(?P<compas>[-\w]+)/$', 'export_compas_file', {}, 'export_compas_file' ),
    ( r'^export/compas/(?P<data_type>data)/$', 'export_compas_file', {}, 'export_compas_file' ),
    ( r'^export/compas/(?P<compas>[-\w]+)/$', 'export_compas_file', {}, 'export_compas_file' ),
    ( r'^export/compas/$', 'export_compas_file', {}, 'export_compas_file' ),
    ( r'^export/warehouse/(?P<data_type>data)/(?P<warehouse>[-\w]+)/$', 'export_compas_file', {}, 'export_warehouse_file' ),
    ( r'^export/warehouse/(?P<warehouse>[-\w]+)/$', 'export_compas_file', {}, 'export_warehouse_file' ),
    
)

urlpatterns += patterns('',
    ( r'^accounts/', include('django.contrib.auth.urls') ),
    ( r'^rosetta/', include('rosetta.urls') ),
    (r'^ajax_select/', include('ajax_select.urls')),
    ( r'^admin/', include( admin.site.urls ) ),
    ( r'^api/', include('ets.api.urls')),
)

#Serve media fields
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
)
urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
)
