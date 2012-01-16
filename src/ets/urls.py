
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail, object_list
from django.utils.translation import ugettext_lazy, ugettext as _
from django.db.models.aggregates import Count

from django.contrib import admin #@Reimport
admin.autodiscover()

from ets.forms import WaybillSearchForm, WaybillScanForm
from ets.models import Waybill
from ets.views import waybill_list, waybill_reception, ExportWaybillData, ImportData
from ets.decorators import receipt_view, dispatch_view, person_required, warehouse_related, receipt_compas, officer_required, waybill_user_related
import ets.models


class PrefixedPatterns:
    urlpatterns = patterns("ets.views",

        ( r'^$', direct_to_template, {
            'template': 'index.html',
            'extra_context': {'form_scan': WaybillScanForm, 'form': WaybillSearchForm },
        }, "index"),
        
        #Order list
        ( r'^orders/$', person_required(warehouse_related(object_list)), {
            'queryset': ets.models.Order.objects.all().order_by('-created'),
            'template_name': 'order/list.html',
        }, "orders"),
        
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
        
        #Listings
        ( r'^search/$', "waybill_search", {
            'queryset': ets.models.Waybill.objects.all(),
        }, "waybill_search" ),
        ( r'^dispatch/$', person_required(dispatch_view(waybill_list)), {
            "extra_context": {"extra_title": _("Waybills waiting for Dispatch signature")}
        }, "waybill_dispatch_list" ),
        ( r'^receive/$', person_required(receipt_view(waybill_list)), {
            "extra_context": {"extra_title": _("Expected Consignments")}
        }, "waybill_reception_list" ),
        
        ( r'^waybill/(?P<waybill_pk>[-\w]+)/$', 'waybill_view', {
            "template": 'waybill/detail.html',
            'queryset': ets.models.Waybill.objects.all(),
        }, "waybill_view" ),
        
        #Dispatch
        ( r'^order/(?P<order_pk>[-\w]+)/(?P<waybill_pk>[-\w]+)/$', "waybill_dispatch_edit", {
            'template': 'waybill/edit.html',
        }, "waybill_edit" ),
        
        ( r'^waybill/(?P<waybill_pk>[-\w]+)/sign_dispatch/$', "waybill_finalize_dispatch", 
          {}, "waybill_finalize_dispatch" ),
        
        #Reception pages
        
        ( r'^waybill/(?P<waybill_pk>[-\w]+)/receive/$', person_required(receipt_view(waybill_reception)), 
          {}, "waybill_reception"),
                            
        ( r'^waybill/(?P<scanned_code>[-+=/\w]+)/scanned_receive/$', "waybill_reception_scanned", {
            'queryset': ets.models.Waybill.objects.filter(transport_dispach_signed_date__isnull=False, 
                                                          receipt_signed_date__isnull=True)
        }, "waybill_reception_scanned"),
        
        ( r'^waybill/(?P<waybill_pk>[-\w]+)/sign_receipt/$', "waybill_finalize_receipt", 
          {}, "waybill_finalize_receipt" ),
        
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
        
        ( r'^compass_waybill_receipt/$', officer_required(waybill_user_related(object_list)), {
            "template_name": 'compas/list_waybills_compas_all.html',
            "queryset": Waybill.objects.filter(receipt_sent_compas__isnull=False),
            "extra_context": {
                "extra_title": _("Received"),
        }}, "compass_waybill_receipt" ),
                            
        ( r'^compass_waybill/$', officer_required(waybill_user_related(object_list)), {
            "template_name": 'compas/list_waybills_compas_all.html',
            "queryset": Waybill.objects.filter(sent_compas__isnull=False), 
        }, "compass_waybill" ),
        
        ( r'^stock/$', 'stock_items', {
            'queryset': ets.models.Warehouse.objects.all().annotate(stock_count=Count('stock_items'))\
                                                .filter(stock_count__gt=0).order_by('location', 'pk'),
            'template_name': 'stock/stocklist.html',
        }, "view_stock" ),
        ( r'^get_stock_data/$', "get_stock_data", {
            'queryset': ets.models.StockItem.objects.all().distinct(),
        }, "get_stock_data" ),
                 
        ( r'^waybill/report/select/$', "direct_to_template", {
            "template": 'reporting/select_report.html',
        }, "select_report" ),
                            
        ( r'^waybill_deserialize/$', "deserialize", {}, "deserialize" ),
    
        ( r'^qrcode/(?P<waybill_pk>[-\w]+)/$', "barcode_qr", {}, "barcode_qr" ),
        
        ( r'^sync_compas/$', "sync_compas", {}, "sync_compas"),
        ( r'^admin/sync_logs/$', "view_logs", {}, "view_logs"),
        
        ( r'^export_data/$', ExportWaybillData.as_view(), {}, "export_file" ),
        ( r'^import_data/$', ImportData.as_view(), {}, "import_file" ),
        
        ( r'^export_compas_file/$', 'export_compas_file', {}, 'export_compas_file' ),
        
    )
    
    urlpatterns += patterns('',
        ( r'^accounts/', include('django.contrib.auth.urls') ),
        ( r'^databrowse/(.*)', databrowse.site.root ),
        ( r'^rosetta/', include('rosetta.urls') ),
        ( r'^admin/', include( admin.site.urls ) ),
        ( r'^api/offline/', include('ets.offliner.api.urls')),
        ( r'^api/', include('ets.api.urls')),
        ( r'^offliner/', include('ets.offliner.urls')),                        
    )
    
    #Serve media fields
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )
    
    if settings.SERVE_STATIC:
        from django.contrib.staticfiles.urls import staticfiles_urlpatterns
        urlpatterns += staticfiles_urlpatterns()

    
urlpatterns = patterns('',
    (r'^%s/' % settings.URL_PREFIX, include(PrefixedPatterns)),
)
