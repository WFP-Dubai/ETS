'''
Created on 11/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-
from base import AbstractTestCase

from offliner.templatetags.extra_tags import truncatesmart



class ExtraTagsTestCase(AbstractTestCase):

    def test_truncatesmart(self):
        self.assertEquals('this is a...',truncatesmart('this is a very long string', 14))
        self.assertEquals('this is a very...',truncatesmart('this is a very long string', 15))
        self.assertEquals('this is a very...',truncatesmart('this is a very long string', 16))
        self.assertEquals('this is a very long...',truncatesmart('this is a very long string', 20))
        self.assertEquals('this is a very long...',truncatesmart('this is a very long string', 25))
        self.assertEquals('this is a very long string',truncatesmart('this is a very long string', 26))
        self.assertEquals('this is a very long string',truncatesmart('this is a very long string', 2000))
        self.assertEquals('this is a very long string',truncatesmart('this is a very long string', 'NOT_AN_INTEGER_VALUE'))
        self.assertEquals('...',truncatesmart('this is a very long string', 2.5))
        
