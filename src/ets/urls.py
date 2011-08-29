
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail

from django.contrib import admin #@Reimport
admin.autodiscover()

from ets.forms import WaybillSearchForm
from ets.models import Waybill
import ets.models

info_dict_waybill = {
    'queryset': Waybill.objects.all()
}

urlpatterns = patterns("ets.views",
                        
    ( r'^$', login_required(direct_to_template), {
        'template': 'index.html',
        'extra_context': {
            'form': WaybillSearchForm,
    }}, "index" ),
    
    #Order list
    ( r'^orders/(?P<warehouse_pk>[-\w]+)/$', "order_list", {}, "orders" ),
    ( r'^orders/$', "order_list", {}, "orders"),
    
    #Order detail
    ( r'^order/(?P<object_id>[-\w]+)/$', login_required(object_detail), {
        'queryset': ets.models.Order.objects.all(),
        'template_name': 'order/detail.html',
    }, "order_detail" ),
    
    #Waybill pages
    ( r'^order/(?P<order_pk>[-\w]+)/add/$', "waybill_create_or_update", {}, "waybill_create" ),
    ( r'^order/(?P<order_pk>[-\w]+)/(?P<waybill_pk>[-\w]+)/$', "waybill_create_or_update", {
        'template': 'waybill/edit.html',
        'waybill_queryset': ets.models.Waybill.objects.filter(status__lt=ets.models.Waybill.SIGNED)
    }, "waybill_edit" ),
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/$', 'waybill_view', {
        'queryset': ets.models.Waybill.objects.all(),
        "template": 'waybill/detail.html',
    }, "waybill_view" ),
    
    
    ( r'^waybill/(?P<waybill_pk>[-\w]+)/print_original/$', "waybill_finalize_dispatch", {
        'queryset': Waybill.objects.filter(status=Waybill.NEW),
    }, "waybill_finalize_dispatch" ),
    
    ( r'^waybill/viewlog/', "viewLogView", {}, "viewLogView" ),
    ( r'^search/$', "waybill_search", {}, "waybill_search" ),
    
    #Reception pages
    ( r'^receive/$', "waybill_search", {
        "queryset": Waybill.objects.filter(status=Waybill.INFORMED)#, destination__pk=COMPAS_STATION),
    }, "waybill_reception_list" ),
    
    ( r'^receive/(?P<waybill_pk>[-\w]+)/$', "waybill_reception", {
       'queryset': Waybill.objects.filter(status__in=(Waybill.SENT, Waybill.INFORMED))#,destination__pk=COMPAS_STATION),
    }, "waybill_reception"),
                       
    
    ( r'^waybill/print_original_receipt/(?P<waybill_pk>[-\w]+)/$', "waybill_finalize_receipt", {
        'queryset': Waybill.objects.filter(status=Waybill.INFORMED)#, destination__pk=COMPAS_STATION),
    }, "waybill_finalize_receipt" ),
    
    ( r'^validate_dispatch/$', "waybill_validate", {
        'template': 'validate/dispatch.html',
        'formset_model': ets.models.Waybill,
        'queryset': ets.models.Waybill.objects.filter(sent_compas=False, 
                                   status__gte=ets.models.Waybill.SIGNED),
    }, "waybill_validate_dispatch_form" ),
    ( r'^validate_receipt_form/$', "waybill_validate", {
        'template': 'validate/receipt.html',
        'formset_model': ets.models.ReceiptWaybill,
        'queryset': ets.models.ReceiptWaybill.objects.filter(sent_compas=False, 
                                   waybill__status__gte=ets.models.Waybill.DELIVERED)#,waybill__destination=settings.COMPAS_STATION),
    }, "waybill_validate_receipt_form" ),
                       
    ( r'^validate/(?P<waybill_pk>[-\w]+)/$', "waybill_validate_form_update", {
        'queryset': Waybill.objects.all(),
    }, "waybill_validate_form_update" ),
                       
    #( r'^waybill/viewwb_reception/(?P<waybill_pk>[-\w]+)/$', "waybill_view_reception", {}, "waybill_view_reception" ),
    #===================================================================================================================
    # ( r'^waybill/commit_to_compas_receipt/$', "receiptToCompas", {}, "receiptToCompas" ),
    # ( r'^waybill/commit_to_compas_dispatch_one/(?P<waybill_pk>[-\w]+)/$', "singleWBDispatchToCompas", 
    #  {}, "singleWBDispatchToCompas" ),
    # ( r'^waybill/commit_to_compas_receipt_one/(?P<waybill_pk>[-\w]+)/$', "singleWBReceiptToCompas", 
    #  {}, "singleWBReceiptToCompas" ),
    #===================================================================================================================
    ( r'^waybill/compass_waybill/$', "direct_to_template", {
        "template": 'compas/list_waybills_compas_all.html',
        "extra_context": {
            'waybill_list': Waybill.objects.filter(sent_compas=True).all, 
            'waybill_list_rec': Waybill.objects.filter(receipt__sent_compas=True).all,
    }}, "compass_waybill" ),
    
    ( r'^waybill/waybill_delete/(?P<waybill_pk>[-\w]+)/(?P<redirect_to>[-\w]+)/$', "waybill_delete",{},"waybill_delete" ),
    ( r'^waybill/waybill_delete/(?P<waybill_pk>[-\w]+)/$', "waybill_delete",{},"waybill_delete" ),
    ( r'^view_stock/(?P<warehouse_pk>[-\w]+)/$', "direct_to_template", {
        "template": 'stock/stocklist.html',
        "extra_context": {
            'stocklist': ets.models.StockItem.objects.all,
    }}, "view_stock" ),
    ( r'^waybill/report/select/$', "direct_to_template", {
        "template": 'reporting/select_report.html',
    }, "select_report" ),
    #===================================================================================================================
    # ( r'^waybill/images/qrcode/(.*)/$', "barcode_qr", {}, "barcode_qr" ),
    #===================================================================================================================
    ( r'^waybill/synchro/upload/', "post_synchronize_waybill", {}, "post_synchronize_waybill" ),
    
    #===================================================================================================================
    # ( r'^waybill/serialize/(?P<waybill_pk>[-\w]+)/$', "serialize" ),
    #===================================================================================================================
    ( r'^waybill/deserialize/$', "deserialize", {}, "deserialize" ),
        
)

urlpatterns += patterns('',
    ( r'^accounts/', include('django.contrib.auth.urls') ),
    ( r'^databrowse/(.*)', login_required(databrowse.site.root) ),
    ( r'^rosetta/', include('rosetta.urls') ),
    ( r'^admin/', include( admin.site.urls ) ),
    ( r'^api/', include('ets.api.urls')),                    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

    #===================================================================================================================
    # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # urlpatterns += staticfiles_urlpatterns()
    #===================================================================================================================
