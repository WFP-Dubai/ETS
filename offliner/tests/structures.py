'''
Created on 14/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

from base import AbstractTestCase
from offliner.structures import waybill_name2position, waybill_position2name, \
                                waybill_named2positional_dict, waybill_positional2named_dict, \
                                loadingdetail_name2position, loadingdetail_position2name, \
                                loadingdetail_named2positional_dict, loadingdetail_positional2named_dict


class StructuresTestCase(AbstractTestCase):

    def test_waybill_name2position(self):
        self.assertEquals(0, waybill_name2position('ltiNumber'))
        self.assertEquals(1, waybill_name2position('waybillNumber'))
        self.assertEquals(2, waybill_name2position('dateOfLoading'))

        self.assertEquals(44, waybill_name2position('waybillProcessedForPayment'))
        self.assertEquals(45, waybill_name2position('invalidated'))
        self.assertEquals(46, waybill_name2position('auditComment'))

    def test_waybill_position2name(self):
        self.assertEquals('ltiNumber', waybill_position2name('0'))
        self.assertEquals('waybillNumber', waybill_position2name('1'))
        self.assertEquals('dateOfLoading', waybill_position2name('2'))

        self.assertEquals('waybillProcessedForPayment', waybill_position2name('44'))
        self.assertEquals('invalidated', waybill_position2name('45'))
        self.assertEquals('auditComment', waybill_position2name('46'))

    def test_waybill_named2positional_dict(self):
        from kiowa.db.utils import instance_as_dict
        from offliner.models import Waybill
        waybill = Waybill.objects.get(id=1)
        waybill_named_dict = instance_as_dict(waybill, exclude=['id'])
        waybill_positional_dict = waybill_named2positional_dict(waybill_named_dict)

        for i in range(0,46):
            if waybill_named_dict.has_key(waybill_position2name(str(i))):
                self.assertEquals(waybill_named_dict[waybill_position2name(str(i))], waybill_positional_dict[i])
        
    def test_waybill_positional2named_dict(self):
        from offliner.models import Waybill
        waybill = Waybill.objects.get(id=1)
        waybill_positional_dict = {}
        from kiowa.db.utils import instance_as_dict
        for k, v in instance_as_dict(waybill, exclude=['id']).items():
            waybill_positional_dict[str(waybill_name2position(k))] = v
        waybill_named_dict = waybill_positional2named_dict(waybill_positional_dict)

        for i in range(0,46):
            if waybill_positional_dict.has_key(str(i)):
                self.assertEquals(waybill_named_dict[waybill_position2name(str(i))], waybill_positional_dict[str(i)])

    def test_loadingdetail_name2position(self):
        self.assertEquals(0, loadingdetail_name2position('wbNumber'))
        self.assertEquals(1, loadingdetail_name2position('siNo'))
        self.assertEquals(2, loadingdetail_name2position('numberUnitsLoaded'))
        self.assertEquals(3, loadingdetail_name2position('numberUnitsGood'))
        self.assertEquals(4, loadingdetail_name2position('numberUnitsLost'))
        self.assertEquals(5, loadingdetail_name2position('numberUnitsDamaged'))
        self.assertEquals(6, loadingdetail_name2position('unitsLostReason'))
        self.assertEquals(7, loadingdetail_name2position('unitsDamagedReason'))
        self.assertEquals(8, loadingdetail_name2position('unitsDamagedType'))
        self.assertEquals(9, loadingdetail_name2position('unitsLostType'))
        self.assertEquals(10, loadingdetail_name2position('overloadedUnits'))
        self.assertEquals(11, loadingdetail_name2position('loadingDetailSentToCompas'))
        self.assertEquals(12, loadingdetail_name2position('overOffloadUnits'))

    def test_loadingdetail_position2name(self):
        self.assertEquals('wbNumber', loadingdetail_position2name('0'))
        self.assertEquals('siNo', loadingdetail_position2name('1'))
        self.assertEquals('numberUnitsLoaded', loadingdetail_position2name('2'))
        self.assertEquals('numberUnitsGood', loadingdetail_position2name('3'))
        self.assertEquals('numberUnitsLost', loadingdetail_position2name('4'))
        self.assertEquals('numberUnitsDamaged', loadingdetail_position2name('5'))
        self.assertEquals('unitsLostReason', loadingdetail_position2name('6'))
        self.assertEquals('unitsDamagedReason', loadingdetail_position2name('7'))
        self.assertEquals('unitsDamagedType', loadingdetail_position2name('8'))
        self.assertEquals('unitsLostType', loadingdetail_position2name('9'))
        self.assertEquals('overloadedUnits', loadingdetail_position2name('10'))
        self.assertEquals('loadingDetailSentToCompas', loadingdetail_position2name('11'))
        self.assertEquals('overOffloadUnits', loadingdetail_position2name('12'))

    def test_loadingdetail_named2positional_dict(self):
        from kiowa.db.utils import instance_as_dict
        from offliner.models import LoadingDetail
        loadingdetail = LoadingDetail.objects.get(id=154)
        loadingdetail_named_dict = instance_as_dict(loadingdetail, exclude=['id'])
        loadingdetail_positional_dict = loadingdetail_named2positional_dict(loadingdetail_named_dict)

        for i in range(0,12):
            if loadingdetail_named_dict.has_key(loadingdetail_position2name(str(i))):
                self.assertEquals(loadingdetail_named_dict[loadingdetail_position2name(str(i))], loadingdetail_positional_dict[i])

    def test_loadingdetail_positional2named_dict(self):
        from offliner.models import LoadingDetail
        loadingdetail = LoadingDetail.objects.get(id=154)
        loadingdetail_positional_dict = {}
        from kiowa.db.utils import instance_as_dict
        for k, v in instance_as_dict(loadingdetail, exclude=['id']).items():
            loadingdetail_positional_dict[str(loadingdetail_name2position(k))] = v
        loadingdetail_named_dict = loadingdetail_positional2named_dict(loadingdetail_positional_dict)

        for i in range(0,12):
            if loadingdetail_positional_dict.has_key(str(i)):
                self.assertEquals(loadingdetail_named_dict[loadingdetail_position2name(str(i))], loadingdetail_positional_dict[str(i)])
