from django.conf.urls.defaults import *
from ets.waybill.views import *
from ets.waybill.models import ltioriginal
from django.views.generic.simple import *

from django.contrib.auth.views import login,logout


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
    (r'^loginHere$',login),
    (r'^select-action$',selectAction),
    (r'^waybill/lti/(.*)$',single_lti_extra),
    (r'^waybill/list/(.*)$',listOfLtis),
    (r'^waybill/list$',ltis_redirect_wh),
    (r'^waybill/import$',import_ltis),
    (r'^waybill/create/(.*)$',waybillCreate),
    (r'^waybill/edit$',waybill_edit),
    (r'^waybill/edit/(.*)$',waybill_edit),
    (r'^waybill/print_original/(.*)$',waybill_finalize_dispatch),
    (r'^waybill/print_original_reciept/(.*)$',waybill_finalize_reciept),    
    (r'^waybill/receive$',waybill_reception_list),
    (r'^waybill/receive/(.*)$',waybill_reception),
    (r'^waybill/findwb/$',waybill_search),
    (r'^waybill/validate$','django.views.generic.list_detail.object_list', info_dict_waybill),
    (r'^waybill/validate/(?P<object_id>.*)$','django.views.generic.list_detail.object_detail', info_dict_waybill),
    (r'^waybill/viewwb/(.*)$',waybill_view),
    (r'^waybill/viewwb_reception/(.*)$',waybill_view_reception),
    (r'^waybill/info$',lti_detail),
    (r'^waybill/info/(.*)$',lti_detail_url),
    (r'^waybill/dispatch$',dispatch),
    (r'^waybill/ltis_codes$',ltis_codes),
    (r'^waybill/testform/(.*)$',waybillCreate),
    (r'^waybill/test$','django.views.generic.list_detail.object_list', info_dict_lti),
    (r'^waybill/serialize/(.*)$',serialize),     
    (r'^waybill/deserialize/$',deserialize),
)