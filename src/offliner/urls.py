
from ets.urls import *

from offliner.views import ExportWaybillData

urlpatterns += patterns("offliner.views",
    ( r'^export/waybills/$', ExportWaybillData.as_view(), {}, "export_waybills" ),
)
