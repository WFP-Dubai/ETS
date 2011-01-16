'''
Created on 20/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from kiowa.utils.testcase import ViewTestCase


class AbstractTestCase(ViewTestCase):
    fixtures = ['offliner/tests/fixtures/offliner/places.json', 'offliner/tests/fixtures/offliner/waybill.json']
    multi_db = True
    settings = {'SIGNALS_ENABLED': False}
    
    def assertEqualList(self, first, second):        
        self.assertEquals(len(first), len(second))
        
        i = 0
        for e in first:
            self.assertEquals(e, second[i])
            i = i+1