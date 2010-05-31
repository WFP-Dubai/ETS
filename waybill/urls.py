from django.conf.urls.defaults import *
from ets.waybill.views import ltis,import_ltis,hello,lti_detail,ltis_redirect_wh,dispatch,lti_detail_url,loginWaybillSystem,selectAction
from ets.waybill.models import ltioriginal


info_dict = {
    'queryset': ltioriginal.objects.all()#,
#    'template_name': "ltioriginal_list.html"
}

urlpatterns = patterns('',
    (r'^loginHere$',login),
    (r'^select-action$',selectAction),
    (r'^waybill/list/(.*)$',ltis),
    (r'^waybill/list/(.*)$',ltis),
    (r'^waybill/list$',ltis_redirect_wh),
    (r'^waybill/import$',import_ltis),
    (r'^waybill/info$',lti_detail),
    (r'^waybill/info/(.*)$',lti_detail_url),
    (r'^waybill/dispatch$',dispatch),
    (r'^waybill/test$','django.views.generic.list_detail.object_list', info_dict),
)