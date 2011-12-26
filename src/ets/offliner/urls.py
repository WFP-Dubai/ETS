
from django.conf import settings
from django.conf.urls.defaults import patterns, include, handler404, handler500
from django.contrib import databrowse
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from django.views.generic.list_detail import object_detail, object_list
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.utils.translation import ugettext as _

from django.contrib import admin #@Reimport
admin.autodiscover()

from ets.forms import WaybillSearchForm, WaybillScanForm
from ets.models import Waybill
from ets.views import waybill_list, waybill_reception
from ets.decorators import receipt_view, dispatch_view, person_required, warehouse_related, receipt_compas, officer_required, waybill_user_related
import ets.models


urlpatterns = patterns("ets.offliner.views",
    #( r'^synchronization/$', "synchronization", {}, "synchronization"),
    ( r'^synchronize/$', "request_update", {}, "synchronize" ),
)
