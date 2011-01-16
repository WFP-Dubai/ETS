'''
Created on 02/dic/2010

@author: serafino
'''

from django.conf.urls.defaults import url, patterns


urlpatterns = patterns(
                       '',
                       
                       # Common Offline Dispatch & Offline Receipt urls:
                       
                       # Home
                       url(r'^$', 'offliner.views.select_action'),
                       
                       # Waybill export to file
                       url(r'^waybill/export/$', 'offliner.views.waybill_export', name = 'waybill_export'),
                       
                       # Waybill import from file
                       url(r'^waybill/import/$', 'offliner.views.waybill_import', name = 'waybill_import'),
                                              
                       # Waybill import from text
                       url(r'^waybill/scan/$', 'offliner.views.waybill_scan', name = 'waybill_scan'),


                       # Offline Dispatch urls:
                       
                       # List of LTI
                       url(r'^list/$', 'offliner.views.ltis_list', name = 'ltis_list'),
                       
                       # LTI detail
                       url(r'^info/(.*)$', 'offliner.views.lti_detail', name = 'lti_detail'),
                       
                       # Waybill new
                       url(r'^create/(.*)$', 'offliner.views.waybill_create', name = 'waybill_create'),
                       
                       # Waybill view
                       url(r'^viewwb/(.*)$', 'offliner.views.waybill_view', name = 'waybill_view'),
                       
                       # Waybill print (finalizes dispatch waybill)
                       url(r'^waybill/print_original/(.*)$','offliner.views.waybill_finalize_dispatch_offline',name='waybill_finalize_dispatch'),
                       
                       # List of Waybills
                       url(r'^waybill/list/$', 'offliner.views.waybills_list', name = 'waybills_list'),
                       
                       # Synchronize Waybill
                       url(r'^synchronize_waybill/(.*)$', 'offliner.views.waybill_upload', name = 'waybill_upload'),
                       
                       # Synchronize Stocks
                       url(r'^synchronize_stocks/$', 'offliner.views.stock_download', name='stock_download'),
                       
                       # Synchronize LTIs
                       url(r'^synchronize_ltis/$', 'offliner.views.lti_download', name='lti_download'),
                       
                       
                       # Offline Receipt urls:
                       
                       # Synchronize Waybills reception
                       url(r'^synchronize_receipt_waybills/$', 'offliner.views.receipt_waybill_download', name='receipt_waybill_download'),
                                           
                       # List of Waybill reception                      
                       url(r'^waybill/reception/list/$', 'offliner.views.waybill_reception_list', name = 'waybill_reception_list'),  
                       
                       # Waybill reception receive
                       url(r'^waybill/receive/(.*)$', 'offliner.views.waybill_reception', name = 'waybill_reception'), 
                       
                       # Waybill reception view
                       url(r'^waybill/viewwb_reception/(.*)$', 'offliner.views.waybill_view_reception', name = 'waybill_view_reception'), 
                       
                       # Waybill reception print (finalizes receipt waybill)
                       url(r'^waybill/print_original_receipt/(.*)$','offliner.views.waybill_finalize_receipt_offline',name='waybill_finalize_receipt'),                   
                       
)
