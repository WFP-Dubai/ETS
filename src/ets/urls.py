
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required

from django.contrib import admin #@Reimport
admin.autodiscover()

from ets.models import LtiOriginal, Waybill, EpicStock

databrowse.site.register( Waybill )
databrowse.site.register( EpicStock )
databrowse.site.register( LtiOriginal )

info_dict_lti = {
    'queryset': LtiOriginal.objects.all()
}
info_dict_waybill = {
    'queryset': Waybill.objects.all()
}

info_dict_waybill_reception = {
    'queryset': Waybill.objects.all(),
    'template_name': 'waybill/reception_list.html'
}


urlpatterns = patterns("ets.views",
                        
    ( r'^$', "select_action", {
        'template': 'select_action.html',
    }, "select_action" ),
    
    ( r'^waybill/viewlog/', "viewLogView" ),
    ( r'^waybill/create/(.*)/$', "waybillCreate", {}, "waybillCreate" ),
    ( r'^waybill/deserialize/$', "deserialize", {}, "deserialize" ),
    ( r'^waybill/dispatch/$', "dispatch" ),
    ( r'^waybill/edit/(.*)/$', "waybill_edit", {}, "waybill_edit" ),
    ( r'^waybill/edit/$', "waybill_edit" ),
    ( r'^waybill/findwb/$', "waybill_search", {}, "waybill_search" ),
    ( r'^waybill/import/$', "import_ltis", {}, "import_ltis" ),
    ( r'^waybill/info/(.*)/$', "lti_detail_url", {}, "lti_detail_url" ),
    ( r'^waybill/list/(.*)/$', "listOfLtis", {}, "listOfLtis" ),
    ( r'^waybill/list/$', "ltis", {}, "ltis"),
    ( r'^waybill/print_original_receipt/(.*)/$', "waybill_finalize_receipt",{},"waybill_finalize_receipt" ),
    ( r'^waybill/print_original/(.*)/$', "waybill_finalize_dispatch", {}, "waybill_finalize_dispatch" ),
    ( r'^waybill/receive/(.*)/$', "waybill_reception", {}, "waybill_reception" ),
    ( r'^waybill/receive/$', "object_list", {
        "template_name": 'waybill/reception_list.html',
        "queryset": Waybill.objects.filter( invalidated = False, recipientSigned = False ),
    }, "waybill_reception_list" ),
    ( r'^waybill/serialize/(.*)/$', "serialize" ),
    ( r'^waybill/test/$', 'object_list', info_dict_lti ),
    ( r'^waybill/validate/$', "direct_to_template", {'template': 'selectValidateAction.html'} ),
    ( r'^waybill/validate_dispatch/$', "waybill_validate_dispatch_form", {}, "waybill_validate_dispatch_form" ),
    ( r'^waybill/validate_receipt_form/$', "waybill_validate_receipt_form", {}, "waybill_validate_receipt_form" ),
    ( r'^waybill/validate/(.*)/$', "waybill_validate_form_update", {}, "waybill_validate_form_update" ),
    #===================================================================================================================
    # ( r'^waybill/viewwb_reception_edit/(.*)/$', waybill_view_reception ),
    #===================================================================================================================
    ( r'^waybill/viewwb_reception/(.*)/$', "waybill_view_reception", {}, "waybill_view_reception" ),
    ( r'^waybill/viewwb/(.*)/$', "waybill_view", {}, "waybill_view" ),
    ( r'^waybill/commit_to_compas_receipt/$', "receiptToCompas" ),
    ( r'^waybill/commit_to_compas_dispatch_one/(.*)/$', "singleWBDispatchToCompas" ),
    ( r'^waybill/commit_to_compas_receipt_one/(.*)/$', "singleWBReceiptToCompas" ),
    #===================================================================================================================
    # ( r'^waybill/reset_waybill/$', waybill_search),
    #===================================================================================================================
    ( r'^waybill/compass_waybill/$', "direct_to_template", {
        "template": 'compas/list_waybills_compas_all.html',
        "extra_context": {
            'waybill_list': Waybill.objects.filter( invalidated = False, waybillSentToCompas = True ).all, 
            'waybill_list_rec': Waybill.objects.filter( invalidated = False, waybillRecSentToCompas = True ).all,
    }}, "compass_waybill" ),
    ( r'^waybill/invalidate_waybill/(.*)/$', "invalidate_waybill",{},"invalidate_waybill" ),
    ( r'^waybill/view_stock/$', "direct_to_template", {
        "template": 'stock/stocklist.html',
        "extra_context": {
            'stocklist': EpicStock.objects.all,
    }}, "view_stock" ),
    ( r'^waybill/report/ltis/$', "ltis_report", {}, "ltis_report" ),
    ( r'^waybill/report/select/$', "direct_to_template", {
        "template": 'reporting/select_report.html',
    }, "select_report" ),
    ( r'^waybill/report/dispatch/(.*)/$', "dispatch_report_wh" ),
    ( r'^waybill/report/receipt/(.*)/(.*)/$', "receipt_report_wh", {}, "receipt_report_wh" ),
    ( r'^waybill/report/receipt/(.*)/$', "receipt_report_cons", {}, "receipt_report_cons" ),
    ( r'^waybill/images/qrcode/(.*)/$', "barcode_qr" ),
    ( r'^waybill/synchro/upload/', "post_synchronize_waybill" ),
    
    # download services
    ( r'^waybill/data/select/$', "select_data", {}, "select_data" ),
    ( r'^waybill/synchro/download/', "get_synchronize_waybill" ),
    ( r'^waybill/synchro/download2/', "get_synchronize_waybill2" ),

    ( r'^stock/synchro/download/', "get_synchronize_stock" ),
    ( r'^lti/synchro/download/', "get_synchronize_lti" ),
    # Additional data
    ( r'^all/synchro/download/file/', "get_all_data_download" ),
    ( r'^all/synchro/download/', "get_all_data" ),
    ( r'^all/download/stock_ets/', "get_wb_stock" ),
    
    ( r'^accounts/profile', "profile" ),
    
)

urlpatterns += patterns('',
    ( r'^accounts/', include('django.contrib.auth.urls') ),
    ( r'^databrowse/(.*)', login_required(databrowse.site.root) ),
    ( r'^rosetta/', include('rosetta.urls') ),
    ( r'^admin/', include( admin.site.urls ) ),                    
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
