from django.conf.urls.defaults import *
from ets.waybill.views import *
from ets.waybill.models import ltioriginal
from django.views.generic.simple import *

from django.contrib.auth.views import login,logout,password_change


info_dict_lti = {
    'queryset': ltioriginal.objects.all()#,
#    'template_name': "ltioriginal_list.html"
}
info_dict_waybill = {
    'queryset': Waybill.objects.all()#,
#    'template_name': "ltioriginal_list.html"
}


info_dict_waybill_reception= {
	'queryset': Waybill.objects.all(),
	'template_name': 'waybill/reception_list.html'
}


urlpatterns = patterns('',
    (r'^$',homepage),
    (r'^accounts/login/$',login),
    (r'^accounts/logout/$',logout),
    (r'^accounts/change_password',password_change),
#    (r'^loginHere$',login),
    (r'^select-action$',selectAction),
    (r'^waybill/create/(.*)$',waybillCreate),
    (r'^waybill/deserialize/$',deserialize),
    (r'^waybill/dispatch$',dispatch),
    (r'^waybill/edit/(.*)$',waybill_edit),
    (r'^waybill/edit$',waybill_edit),
    (r'^waybill/findwb/$',waybill_search),
    (r'^waybill/import$',import_ltis),
    (r'^waybill/info/(.*)$',lti_detail_url),
#    (r'^waybill/info$',lti_detail),
    (r'^waybill/list/(.*)$',listOfLtis),
    (r'^waybill/list$',ltis),
#    (r'^waybill/lti/(.*)$',single_lti_extra),
#    (r'^waybill/ltis_codes$',ltis_codes),
    (r'^waybill/print_original_reciept/(.*)$',waybill_finalize_reciept),    
    (r'^waybill/print_original/(.*)$',waybill_finalize_dispatch),
    (r'^waybill/receive/(.*)$',waybill_reception),
    (r'^waybill/receive$',waybill_reception_list),
    (r'^waybill/serialize/(.*)$',serialize),     
    (r'^waybill/test$','django.views.generic.list_detail.object_list', info_dict_lti),
    (r'^waybill/validate/$',waybill_validateSelect),
    (r'^waybill/validate_dispatch$',waybill_validate_dispatch_form),
    (r'^waybill/validate_receipt_form$',waybill_validate_receipt_form),
    (r'^waybill/validate/(.*)$',waybill_validate_form_update),
    (r'^waybill/viewwb_reception_edit/(.*)$',waybill_view_reception),
    (r'^waybill/viewwb_reception/(.*)$',waybill_view_reception),
    (r'^waybill/viewwb/(.*)$',waybill_view),
    (r'^waybill/commit_to_compas_dispatch/$',dispatchToCompas),
    (r'^waybill/commit_to_compas_receipt/$',receiptToCompas),
    (r'^waybill/commit_to_compas_dispatch_one/(.*)$',singleWBDispatchToCompas),
    (r'^waybill/commit_to_compas_receipt_one/(.*)$',singleWBReceiptToCompas),
    (r'^waybill/reset_waybill/$',waybill_search),
    (r'^waybill/compass_waybill/$',listCompasWB),
    (r'^waybill/invalidate_waybill/(.*)$',invalidate_waybill),
)