
from django.conf.urls.defaults import patterns, url
#from django.views.generic.simple import direct_to_template, redirect_to
#from django.views.generic.list_detail import object_list
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout, password_change, password_change_done

from ets.waybill.models import LtiOriginal, Waybill, EpicStock

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

urlpatterns = patterns( '',
    ( r'^$', 'django.views.generic.simple.redirect_to', {'url':'select-action'} ),
    ( r'^accounts/login/$', login ),
    ( r'^accounts/logout/$', logout ),
    ( r'^accounts/change_password', password_change ),
    ( r'^accounts/change_password_done', password_change_done ),
) 
urlpatterns += patterns("ets.waybill.views",
                        
    ( r'^accounts/profile', "profile" ),
                        
    url( r'^select-action/$', "select_action", {
        'template': 'select_action.html',
    }, name="select_action" ),
    
    ( r'^waybill/viewlog', "viewLogView" ),
    ( r'^waybill/create/(.*)/$', "waybillCreate" ),
    ( r'^waybill/deserialize/$', "deserialize" ),
    ( r'^waybill/dispatch/$', "dispatch" ),
    ( r'^waybill/edit/(.*)/$', "waybill_edit" ),
    ( r'^waybill/edit/$', "waybill_edit" ),
    url( r'^waybill/findwb/$', "waybill_search", name="waybill_search" ),
    ( r'^waybill/import/$', "import_ltis" ),
    url( r'^waybill/info/(.*)/$', "lti_detail_url", name="lti_detail_url" ),
    url( r'^waybill/list/(.*)/$', "listOfLtis", name="listOfLtis" ),
    ( r'^waybill/list/$', "ltis" ),
    ( r'^waybill/print_original_receipt/(.*)/$', "waybill_finalize_receipt" ),
    ( r'^waybill/print_original/(.*)/$', "waybill_finalize_dispatch" ),
    url( r'^waybill/receive/(.*)/$', "waybill_reception", name="waybill_reception" ),
    url( r'^waybill/receive/$', "django.views.generic.list_detail.object_list", {
        "template_name": 'waybill/reception_list.html',
        "queryset": Waybill.objects.filter( invalidated = False, recipientSigned = False ),
    }, name="waybill_reception_list" ),
    ( r'^waybill/serialize/(.*)/$', "serialize" ),
    ( r'^waybill/test/$', 'django.views.generic.list_detail.object_list', info_dict_lti ),
    ( r'^waybill/validate/$', "django.views.generic.simple.direct_to_template", {'template': 'selectValidateAction.html'} ),
    url( r'^waybill/validate_dispatch/$', "waybill_validate_dispatch_form", name="waybill_validate_dispatch_form" ),
    ( r'^waybill/validate_receipt_form/$', "waybill_validate_receipt_form" ),
    ( r'^waybill/validate/(.*)/$', "waybill_validate_form_update" ),
    #===================================================================================================================
    # ( r'^waybill/viewwb_reception_edit/(.*)/$', waybill_view_reception ),
    #===================================================================================================================
    ( r'^waybill/viewwb_reception/(.*)/$', "waybill_view_reception" ),
    url( r'^waybill/viewwb/(.*)/$', "waybill_view", name="waybill_view" ),
    ( r'^waybill/commit_to_compas_receipt/$', "receiptToCompas" ),
    ( r'^waybill/commit_to_compas_dispatch_one/(.*)/$', "singleWBDispatchToCompas" ),
    ( r'^waybill/commit_to_compas_receipt_one/(.*)/$', "singleWBReceiptToCompas" ),
    #===================================================================================================================
    # ( r'^waybill/reset_waybill/$', waybill_search),
    #===================================================================================================================
    url( r'^waybill/compass_waybill/$', "django.views.generic.simple.direct_to_template", {
        "template": 'compas/list_waybills_compas_all.html',
        "extra_context": {
            'waybill_list': Waybill.objects.filter( invalidated = False, waybillSentToCompas = True ).all, 
            'waybill_list_rec': Waybill.objects.filter( invalidated = False, waybillRecSentToCompas = True ).all,
    }}, name="compass_waybill" ),
    ( r'^waybill/invalidate_waybill/(.*)/$', "invalidate_waybill" ),
    url( r'^waybill/view_stock/$', "django.views.generic.simple.direct_to_template", {
        "template": 'stock/stocklist.html',
        "extra_context": {
            'stocklist': EpicStock.objects.all,
    }}, name="view_stock" ),
    ( r'^waybill/report/ltis/$', "ltis_report" ),
    url( r'^waybill/report/select/$', "django.views.generic.simple.direct_to_template", {
        "template": 'reporting/select_report.html',
    }, name="select_report" ),
    ( r'^waybill/report/dispatch/(.*)/$', "dispatch_report_wh" ),
    ( r'^waybill/report/receipt/(.*)/(.*)/$', "receipt_report_wh" ),
    ( r'^waybill/report/receipt/(.*)/$', "receipt_report_cons" ),
    ( r'^waybill/images/qrcode/(.*)/$', "barcode_qr" ),
    ( r'^waybill/synchro/upload/', "post_synchronize_waybill" ),
    
    # download services
    ( r'^waybill/data/select/$', "select_data" ),
    ( r'^stock/synchro/download/', "get_synchronize_stock" ),
    ( r'^lti/synchro/download/', "get_synchronize_lti" ),
    ( r'^waybill/synchro/download/', "get_synchronize_waybill" ),
    ( r'^waybill/synchro/download2/', "get_synchronize_waybill2" ),
    # Additional data
    ( r'^all/synchro/download/file/', "get_all_data_download" ),
    ( r'^all/synchro/download/', "get_all_data" ),
    ( r'^all/download/stock_ets/', "get_wb_stock" ),

    ( r'^databrowse/(.*)', login_required(databrowse.site.root) ),
)
