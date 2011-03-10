from django.conf.urls.defaults import *
from ets.waybill.views import *
from ets.waybill.tools import *
from ets.waybill.models import LtiOriginal
from django.views.generic.simple import *
from django.contrib import databrowse

from django.contrib.auth.views import login,logout,password_change,password_change_done


info_dict_lti = {
    'queryset': LtiOriginal.objects.all()
}
info_dict_waybill = {
    'queryset': Waybill.objects.all()
}


info_dict_waybill_reception= {
    'queryset': Waybill.objects.all(),
    'template_name': 'waybill/reception_list.html'
}

urlpatterns = patterns('',
    (r'^$','django.views.generic.simple.redirect_to',{'url':'select-action'}),
    (r'^accounts/login/$',login),
    (r'^accounts/logout/$',logout),
    (r'^accounts/change_password',password_change),
    (r'^accounts/profile',profile),
    (r'^accounts/change_password_done',password_change_done),
    #(r'^select-action$','django.views.generic.simple.direct_to_template', {'template': 'selectAction.html'}),
    (r'^select-action$',selectAction),
    (r'^waybill/viewlog',viewLogView),
    (r'^waybill/create/(.*)$',waybillCreate),
    (r'^waybill/deserialize/$',deserialize),
    (r'^waybill/dispatch$',dispatch),
    (r'^waybill/edit/(.*)$',waybill_edit),
    (r'^waybill/edit$',waybill_edit),
    (r'^waybill/findwb/$',waybill_search),
    (r'^waybill/import$',import_ltis),
    (r'^waybill/info/(.*)$',lti_detail_url),
    (r'^waybill/list/(.*)$',listOfLtis),
    (r'^waybill/list$',ltis),
    (r'^waybill/print_original_receipt/(.*)$',waybill_finalize_receipt),    
    (r'^waybill/print_original/(.*)$',waybill_finalize_dispatch),
    (r'^waybill/receive/(.*)$',waybill_reception),
    (r'^waybill/receive$',waybill_reception_list),
    (r'^waybill/serialize/(.*)$',serialize),     
    (r'^waybill/test$','django.views.generic.list_detail.object_list', info_dict_lti),
    #(r'^waybill/validate/$',waybill_validateSelect),
    (r'^waybill/validate/$','django.views.generic.simple.direct_to_template', {'template': 'selectValidateAction.html'}),
    (r'^waybill/validate_dispatch$',waybill_validate_dispatch_form),
    (r'^waybill/validate_receipt_form$',waybill_validate_receipt_form),
    (r'^waybill/validate/(.*)$',waybill_validate_form_update),
    (r'^waybill/viewwb_reception_edit/(.*)$',waybill_view_reception),
    (r'^waybill/viewwb_reception/(.*)$',waybill_view_reception),
    (r'^waybill/viewwb/(.*)$',waybill_view),
    #(r'^waybill/commit_to_compas_dispatch/$',dispatchToCompas),
    (r'^waybill/commit_to_compas_receipt/$',receiptToCompas),
    (r'^waybill/commit_to_compas_dispatch_one/(.*)$',singleWBDispatchToCompas),
    (r'^waybill/commit_to_compas_receipt_one/(.*)$',singleWBReceiptToCompas),
    (r'^waybill/reset_waybill/$',waybill_search),
    (r'^waybill/compass_waybill/$',listCompasWB),
    (r'^waybill/invalidate_waybill/(.*)$',invalidate_waybill),
    (r'^waybill/view_stock/$',view_stock),
    (r'^waybill/report/ltis/$',ltis_report),
    (r'^waybill/report/select$',select_report),
    (r'^waybill/report/dispatch/(.*)$',dispatch_report_wh),
    (r'^waybill/report/receipt/(.*)/(.*)$',receipt_report_wh),
    (r'^waybill/report/receipt/(.*)$',receipt_report_cons),
    (r'^waybill/images/qrcode/(.*)$',barcode_qr),
    (r'^databrowse/(.*)', databrowse.site.root),
    (r'^waybill/synchro/upload/',post_synchronize_waybill), 

     # download services
     (r'^stock/synchro/download/',get_synchronize_stock),
     (r'^lti/synchro/download/',get_synchronize_lti),
     (r'^waybill/synchro/download/',get_synchronize_waybill),
     
)