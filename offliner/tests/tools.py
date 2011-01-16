'''
Created on 20/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

import zlib, base64
import json

from django.conf import settings

from offliner.tests.base import AbstractTestCase
from offliner.tools import serialize_wb, wb_compress, zipBase64, new_waybill_no, wb_compress_repr, serialized_wb_repr, \
                           wb_uncompress_repr
from offliner.models import Waybill


class ToolTestCase(AbstractTestCase):
    
    def test_serialize_wb(self):
        wb_code = 1
        
        # Prepare expected method return
        waybill = Waybill.objects.get(id=wb_code)   
        loadindetails = waybill.loadingdetail_set.select_related() 
        from django.core import serializers
        data = serializers.serialize('json', [waybill] + list(loadindetails))       
        
        # Call to tested method
        serialized_waybill = serialize_wb(wb_code)
        
        # Testing method return
        self.assertEquals(data, serialized_waybill) 
        
    def test_wb_compress(self):
        wb_code = 1
        
        # Prepare expected method return
        waybill = Waybill.objects.get(id=wb_code)   
        loadindetails = waybill.loadingdetail_set.select_related() 
        from django.core import serializers
        data = serializers.serialize('json', [waybill] + list(loadindetails))
        zipped_data = zlib.compress(data)
        base64_data = base64.b64encode(zipped_data)      
        
        # Call to tested method
        compressed_waybill = wb_compress(wb_code)
        
        # Testing method return
        self.assertEquals(base64_data, compressed_waybill)     
        
    def test_zipBase64(self):
        data = 'Some data...'
        
        # Prepare expected method return
        zipped_data = zlib.compress(data)
        base64_data = base64.b64encode(zipped_data)
        
        # Call to tested method
        returned_data = zipBase64(data)
 
        # Testing method return
        self.assertEquals(base64_data, returned_data)  
        
    def test_new_waybill_no(self):
        wb_id = 1
        
        # Prepare expected method return
        expected = settings.WAYBILL_LETTER + '%04d' % wb_id
        
        # Call to tested method
        returned_data = new_waybill_no(Waybill.objects.get(id=wb_id))
        
        # Testing method return
        self.assertEquals(expected, returned_data) 
        
    def test_wb_compress_repr(self):
        wb_id = 1
        
        # Prepare expected method return     
        data = list() 
        from kiowa.db.utils import instance_as_dict
        waybill = Waybill.objects.get(id=wb_id)   
        waybill_dict = instance_as_dict(waybill, exclude=['id']) 
        from offliner.structures import waybill_named2positional_dict
        waybill_positional_dict = waybill_named2positional_dict(waybill_dict)
        data.append(waybill_positional_dict) 
        loading_details = waybill.loadingdetail_set.select_related() 
        ld_list = []
        for l in loading_details:
            ld_dict = instance_as_dict(l, exclude=['id','wbNumber'])
            from offliner.structures import loadingdetail_named2positional_dict
            ld_positional_dict = loadingdetail_named2positional_dict(ld_dict)
            ld_list.append(ld_positional_dict)          
        data.append(list(ld_list))
        base64_data = zipBase64(json.dumps(data))
        
        # Call to tested method
        compressed_waybill = wb_compress_repr(wb_id)
        
        # Testing method return
        self.assertEquals(base64_data, compressed_waybill)      
        
    def test_serialized_wb_repr(self):
        wb_id = 1
        
        # Prepare expected method return
        expected_data = list()        
        from kiowa.db.utils import instance_as_dict
        waybill = Waybill.objects.get(id=wb_id)   
        waybill_dict = instance_as_dict(waybill, exclude=['id'])
        from offliner.structures import waybill_named2positional_dict
        waybill_positional_dict = waybill_named2positional_dict(waybill_dict)
        expected_data.append(waybill_positional_dict) 
        loading_details = waybill.loadingdetail_set.select_related() 
        ld_list = []
        for l in loading_details:
            ld_dict = instance_as_dict(l, exclude=['id','wbNumber'])
            from offliner.structures import loadingdetail_named2positional_dict
            ld_positional_dict = loadingdetail_named2positional_dict(ld_dict)
            ld_list.append(ld_positional_dict)
        expected_data.append(list(ld_list)) 
        
        # Call to tested method
        compressed_waybill = serialized_wb_repr(wb_id)
        
        # Testing method return
        self.assertEquals(expected_data, compressed_waybill)

    def test_wb_uncompress_repr(self):
        compressed_wb = 'eJxtU01vm0AQ/SsrLr0k1n4BNjfkxSkVNjZYraUohw1dJatiiBZcqYry38sOCc6Wctr33szsvGXm/tXDXoS8b0lxwpgQjHFMMcd77wZ5xConTPylRdQiigm+JfSWEkuxOcUtJVStfyvzxxK+JYpW/rQgAFV3L7KvnlGhztL86qwQfmpi6IEGDFt6aeksv0vLY7ouUb7ZpOuksMrKKkdzUdAoeCjitETbVIgsQUlcHlF2FAuQyRgsm+6lNT0qL49V2/RGVn1rIAC8CWOb/tKhnTyPZZlDZ7pSzaC2oIHR7+pZV7UanDzpbijY67b5CPDfL9W1Mv8NCBwLofuWiJCI8ojQBWXU5yuIgefYyLqDFAqu14MTqZvhDhKh3eX8qEwEKnFV6qp0llsqWY8am2VeNT7Le/+Lo+zPUh0ZLMMpnE5g6hBn8U6kMTDwb3/kRSbQJs8F2hf5XRFvtwnMHP7IZGQ6TXVZ6DwRg1IHsbJzBeOJHZ0TF1IXMhdyF/ouhB72Rjc9miY8N/pJN7L23m7Q/eu4UNcpv37D4gX86+GE/xFW2A+W4bR9nOPFwE6rNyHuIN9B43JMc+Y6Jp8cvz08/AW1c/si'

        # Prepare expected method return
        unbase64_data = base64.b64decode(compressed_wb)
        unzipped = zlib.decompress(unbase64_data)
        uncompreesed_wb_expected = json.loads(unzipped)

        # Call to tested method
        uncompreesed_wb = wb_uncompress_repr(compressed_wb)

        # Testing method return
        self.assertEquals(uncompreesed_wb_expected, uncompreesed_wb)
        
              
            