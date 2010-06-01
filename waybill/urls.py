from django.conf.urls.defaults import *
from ets.waybill.views import *
from ets.waybill.models import ltioriginal

from django.contrib.auth.views import login,logout


info_dict = {
    'queryset': ltioriginal.objects.all()#,
#    'template_name': "ltioriginal_list.html"
}

urlpatterns = patterns('',
    (r'^loginHere$',login),
    (r'^select-action$',selectAction),
    (r'^waybill/list/(.*)$',ltis),
    (r'^waybill/list$',ltis_redirect_wh),
    (r'^waybill/import$',import_ltis),
    (r'^waybill/create/(.*)$',waybill_create),
    (r'^waybill/edit$',waybill_edit),
    (r'^waybill/receive$',waybill_reception),
    (r'^waybill/findwb$',waybill_search),
    (r'^waybill/validate$',waybill_validate_list),
    (r'^waybill/info$',lti_detail),
    (r'^waybill/info/(.*)$',lti_detail_url),
    (r'^waybill/dispatch$',dispatch),
    (r'^waybill/ltis_codes$',ltis_codes),
    (r'^waybill/testform$',testform),
    (r'^waybill/test$','django.views.generic.list_detail.object_list', info_dict),
)