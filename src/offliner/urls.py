
from ets.urls import *

from ets.offliner.views import ExportWaybillData

urlpatterns += patterns("ets.offliner.views",
    ( r'^export/waybills/$', ExportWaybillData.as_view(), {}, "export_waybills" ),
)
