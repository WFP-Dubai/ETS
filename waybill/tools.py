from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login,logout
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db import connections
from django.db import models
from django.forms.formsets import BaseFormSet
from django.forms.models import inlineformset_factory,modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Template, RequestContext,Library, Node
from ets.waybill.compas import *
from ets.waybill.forms import *
from ets.waybill.models import *
from ets.waybill.tools import *
from ets.waybill.views import *
import cx_Oracle
import datetime
import os,StringIO, zlib,base64,string
## Databrowse
from django.contrib import databrowse
import json
databrowse.site.register(Waybill)
databrowse.site.register(EpicStock)
databrowse.site.register(LtiOriginal)


def removeNonAsciiChars(s):
    return s if s=='' else ''.join([i for i in s if s in string.printable])

def logger(action,user,datain,dataout):
    pass

def loggit(items):
    print items

def track_compas_update():
    file = 'tagfile.tag'
    FILE = open(file,"w")
    FILE.write(str(datetime.datetime.now()))
    FILE.close()

def readTag():
    try:
        logfile = 'tagfile.tag'
        FILE = open(logfile)
        log = FILE.read()
        FILE.close()
        return log + 'x'
    except:
        return 'None'
    
def viewLog():
    try:
        logfile = 'logg.txt'
        FILE = open(logfile,"r")
        log = FILE.read()
        FILE.close()
        return log
    except:
        pass    

def uniq(inlist):
    # order preserving
    uniques = []
    for item in inlist:
        if item not in uniques:
            uniques.append(item)
    return uniques
    
#prints a list item....
def printlistitem(list,index):
    print list(index)

def printlist(list):
    for item in list:
        print item

# takes compressed base64 Data and uncompresses it
def un64unZip(data):
    data= string.replace(data,' ','+')
    zippedData = base64.b64decode(data)
    uncompressed = zlib.decompress(zippedData)    
    return uncompressed

# takes a wb id and returns a zipped base64 string of the serialized object // ?use table to reduce column names save 1000 bytes?

def serialize_wb(wb_id):
    """
    This method serializes the Waybill identified by the wb_id param with related LoadingDetails, LtiOriginals and EpicStocks.

    @param wb_id: the Waybill identifier
    @return the serialized json data.

    Usage:

    >>> wb_id = 3

    >>> s = serialize_wb(wb_id)

    >>> s
    [{"pk": 3, "model": "offliner.waybill", "fields": {"waybillNumber": "X0167", "transportVehicleRegistration": "vrn", "transportContractor": "RAIS MIDDLE EAST LTD.", "dispatchRemarks": "dr", "dateOfDispatch": "2011-01-18", "recipientArrivalDate": null, "recipientConsingee": "WORLD FOOD PROGRAMME", "transportSubContractor": "ts", "transportDeliverySignedTimestamp": null, "recipientDistance": null, "recipientName": "", "auditComment": "", "dispatcherSigned": false, "waybillProcessedForPayment": false, "recipientSignedTimestamp": null, "dispatcherTitle": "LOGISTICS OFFICER", "containerTwoSealNumber": "2s", "transportDeliverySigned": false, "containerTwoRemarksReciept": "", "ltiNumber": "JERX0011000Z7901P", "containerOneRemarksReciept": "", "transportDispachSignedTimestamp": null, "transactionType": "DEL", "invalidated": false, "containerTwoRemarksDispatch": "2r", "recipientSigned": false, "transportDispachSigned": false, "dateOfLoading": "2011-01-18", "recipientEndDischargeDate": null, "recipientRemarks": "", "waybillSentToCompas": false, "recipientStartDischargeDate": null, "containerOneRemarksDispatch": "1r", "containerOneSealNumber": "1s", "waybillValidated": false, "transportType": "02", "destinationWarehouse": "QD9X001", "recipientLocation": "QALANDIA", "waybillRecSentToCompas": false, "transportDriverName": "dn", "dispatcherName": "JERX0010002630", "transportDriverLicenceID": "dln", "containerOneNumber": "1n", "recipientTitle": "", "containerTwoNumber": "2n", "waybillReceiptValidated": false, "transportTrailerRegistration": "trn"}}, {"pk": "JERX001000000000000011031HQX0001000000000000990922", "model": "offliner.LtiOriginal", "fields": {"origin_location_code": "ASHX", "si_record_id": "HQX0001000000000000990922", "origin_loc_name": "ASHDOD", "code": "JERX0011000Z7901P", "destination_location_code": "QD9X", "quantity_net": "150.000", "consegnee_code": "WFP", "quantity_gross": "150.300", "commodity_code": "CERWHF", "destination_loc_name": "QALANDIA", "requested_dispatch_date": "2010-06-29", "transport_name": "RAIS MIDDLE EAST LTD.", "unit_weight_net": "50.000", "transport_ouc": "JERX001", "origin_wh_code": "ASHX004", "lti_id": "JERX001000000000000011031", "number_of_units": "3000", "unit_weight_gross": "50.100", "comm_category_code": "CER", "origin_wh_name": "ASHDOD_OVERSEAS_BONDED", "expiry_date": "2010-07-04", "project_wbs_element": "103871.1", "cmmname": "WHEAT FLOUR", "lti_date": "2010-06-29", "consegnee_name": "WORLD FOOD PROGRAMME", "origintype_desc": "Warehouse", "transport_code": "R001", "origin_type": "2", "si_code": "00004178"}}, {"pk": "JERX001000000000000011031HQX0001000000000000991507", "model": "offliner.LtiOriginal", "fields": {"origin_location_code": "ASHX", "si_record_id": "HQX0001000000000000991507", "origin_loc_name": "ASHDOD", "code": "JERX0011000Z7901P", "destination_location_code": "QD9X", "quantity_net": "200.000", "consegnee_code": "WFP", "quantity_gross": "200.400", "commodity_code": "PULCKP", "destination_loc_name": "QALANDIA", "requested_dispatch_date": "2010-06-29", "transport_name": "RAIS MIDDLE EAST LTD.", "unit_weight_net": "50.000", "transport_ouc": "JERX001", "origin_wh_code": "ASHX004", "lti_id": "JERX001000000000000011031", "number_of_units": "4000", "unit_weight_gross": "50.100", "comm_category_code": "PUL", "origin_wh_name": "ASHDOD_OVERSEAS_BONDED", "expiry_date": "2010-07-04", "project_wbs_element": "103871.1", "cmmname": "CHICKPEAS", "lti_date": "2010-06-29", "consegnee_name": "WORLD FOOD PROGRAMME", "origintype_desc": "Warehouse", "transport_code": "R001", "origin_type": "2", "si_code": "00005581"}}, {"pk": "JERX001000000000000011031HQX0001000000000000890038", "model": "offliner.LtiOriginal", "fields": {"origin_location_code": "ASHX", "si_record_id": "HQX0001000000000000890038", "origin_loc_name": "ASHDOD", "code": "JERX0011000Z7901P", "destination_location_code": "QD9X", "quantity_net": "357.000", "consegnee_code": "WFP", "quantity_gross": "384.000", "commodity_code": "OILVEG", "destination_loc_name": "QALANDIA", "requested_dispatch_date": "2010-06-29", "transport_name": "RAIS MIDDLE EAST LTD.", "unit_weight_net": "11.900", "transport_ouc": "JERX001", "origin_wh_code": "ASHX004", "lti_id": "JERX001000000000000011031", "number_of_units": "30000", "unit_weight_gross": "12.800", "comm_category_code": "OIL", "origin_wh_name": "ASHDOD_OVERSEAS_BONDED", "expiry_date": "2010-07-04", "project_wbs_element": "10387.1.01.01", "cmmname": "VEGETABLE OIL", "lti_date": "2010-06-29", "consegnee_name": "WORLD FOOD PROGRAMME", "origintype_desc": "Warehouse", "transport_code": "R001", "origin_type": "2", "si_code": "82492906"}}, {"pk": "ASHX004JERX0010000417801CERCERWHFBY17275", "model": "offliner.epicstock", "fields": {"si_record_id": "HQX0001000000000000990922", "quantity_gross": "10020.390", "qualitydescr": "Good", "si_code": "00004178", "quantity_net": "10000.000", "origin_id": "JERX0010000417801", "wh_code": "ASHX004", "packagename": "BAG, POLYPROPYLENE, 50 KG", "comm_category_code": "CER", "wh_country": "ISRAEL", "wh_location": "ASHDOD", "reference_number": "0080003270", "wh_regional": "OMC", "qualitycode": "G", "wh_name": "ASHDOD_OVERSEAS_BONDED", "commodity_code": "CERWHF", "package_code": "BY17", "allocation_code": "275", "number_of_units": 200, "project_wbs_element": "103871.1", "cmmname": "WHEAT FLOUR"}}, {"pk": "ASHX004JERX0010000558101PULPULCKPBY17275", "model": "offliner.epicstock", "fields": {"si_record_id": "HQX0001000000000000991507", "quantity_gross": "510.054", "qualitydescr": "Good", "si_code": "00005581", "quantity_net": "500.000", "origin_id": "JERX0010000558101", "wh_code": "ASHX004", "packagename": "BAG, POLYPROPYLENE, 50 KG", "comm_category_code": "PUL", "wh_country": "ISRAEL", "wh_location": "ASHDOD", "reference_number": "0080003713", "wh_regional": "OMC", "qualitycode": "G", "wh_name": "ASHDOD_OVERSEAS_BONDED", "commodity_code": "PULCKP", "package_code": "BY17", "allocation_code": "275", "number_of_units": 100000, "project_wbs_element": "103871.1", "cmmname": "CHICKPEAS"}}]
    """

    waybill_to_serialize = Waybill.objects.get(id=wb_id)

    # Add related LoadingDetais to serialized representation

    loadingdetails_to_serialize = waybill_to_serialize.loadingdetail_set.select_related()

    # Add related LtiOriginals to serialized representation

    ltis_to_serialize = LtiOriginal.objects.filter(code=waybill_to_serialize.ltiNumber)

    # Add related EpicStocks to serialized representation

    stocks_to_serialize = []
    for lti in ltis_to_serialize:
        for s in lti.get_stocks():
            stocks_to_serialize.append(s)

    data = serializers.serialize('json', [waybill_to_serialize] + list(loadingdetails_to_serialize) + list(ltis_to_serialize) + list(stocks_to_serialize))
    return data
def serialized_wb_repr(wb_id):
    """
    This method gives the serialized representation of the Waybill identified by the wb_id param with related LoadingDetails, LtiOriginals and EpicStocks.

    Return the serialized data.

    @param wb_id: the Waybill identifier
    @return: a list containing the Waybill positional dictionary as first element and lists of related LoadingDetails, LtiOriginals, EpicStocks positional dictionaries as subsequent elements

    Usage:

    >>> wb_code = 3

    >>> s = serialized_wb_repr(wb_id)

    >>> s
    [{0: 'JERX0011000Z7901P', 1: 'X0167', 2: '2011-01-18', 3: '2011-01-18', 4: 'Delivery', 5: 'Road', 6: 'dr', 7: 'JERX0010002630', 8: 'LOGISTICS OFFICER', 9: 'False', 10: 'RAIS MIDDLE EAST LTD.', 11: 'ts', 12: 'dn', 13: 'dln', 14: 'vrn', 15: 'trn', 16: 'False', 18: 'False', 20: '1n', 21: '2n', 22: '1s', 23: '2s', 24: '1r', 25: '2r', 26: '', 27: '', 28: 'QALANDIA', 29: 'WORLD FOOD PROGRAMME', 30: '', 31: '', 36: '', 37: 'False', 39: 'QD9X001', 40: 'False', 41: 'False', 42: 'False', 43: 'False', 44: 'False', 45: 'False', 46: ''}, [], [{0: 'JERX001000000000000011031HQX0001000000000000990922', 1: 'JERX001000000000000011031', 2: 'JERX0011000Z7901P', 3: '2010-06-29', 4: '2010-07-04', 5: 'R001', 6: 'JERX001', 7: 'RAIS MIDDLE EAST LTD.', 8: '2', 9: 'Warehouse', 10: 'ASHX', 11: 'ASHDOD', 12: 'ASHX004', 13: 'ASHDOD_OVERSEAS_BONDED', 14: 'QD9X', 15: 'QALANDIA', 16: 'WFP', 17: 'WORLD FOOD PROGRAMME', 18: '2010-06-29', 19: '103871.1', 20: 'HQX0001000000000000990922', 21: '00004178', 22: 'CER', 23: 'CERWHF', 24: 'WHEAT FLOUR', 25: '150.000', 26: '150.300', 27: '3000', 28: '50.000', 29: '50.100'}, {0: 'JERX001000000000000011031HQX0001000000000000991507', 1: 'JERX001000000000000011031', 2: 'JERX0011000Z7901P', 3: '2010-06-29', 4: '2010-07-04', 5: 'R001', 6: 'JERX001', 7: 'RAIS MIDDLE EAST LTD.', 8: '2', 9: 'Warehouse', 10: 'ASHX', 11: 'ASHDOD', 12: 'ASHX004', 13: 'ASHDOD_OVERSEAS_BONDED', 14: 'QD9X', 15: 'QALANDIA', 16: 'WFP', 17: 'WORLD FOOD PROGRAMME', 18: '2010-06-29', 19: '103871.1', 20: 'HQX0001000000000000991507', 21: '00005581', 22: 'PUL', 23: 'PULCKP', 24: 'CHICKPEAS', 25: '200.000', 26: '200.400', 27: '4000', 28: '50.000', 29: '50.100'}, {0: 'JERX001000000000000011031HQX0001000000000000890038', 1: 'JERX001000000000000011031', 2: 'JERX0011000Z7901P', 3: '2010-06-29', 4: '2010-07-04', 5: 'R001', 6: 'JERX001', 7: 'RAIS MIDDLE EAST LTD.', 8: '2', 9: 'Warehouse', 10: 'ASHX', 11: 'ASHDOD', 12: 'ASHX004', 13: 'ASHDOD_OVERSEAS_BONDED', 14: 'QD9X', 15: 'QALANDIA', 16: 'WFP', 17: 'WORLD FOOD PROGRAMME', 18: '2010-06-29', 19: '10387.1.01.01', 20: 'HQX0001000000000000890038', 21: '82492906', 22: 'OIL', 23: 'OILVEG', 24: 'VEGETABLE OIL', 25: '357.000', 26: '384.000', 27: '30000', 28: '11.900', 29: '12.800'}], [{0: 'ASHX004JERX0010000417801CERCERWHFBY17275', 1: 'OMC', 2: 'ISRAEL', 3: 'ASHDOD', 4: 'ASHX004', 5: 'ASHDOD_OVERSEAS_BONDED', 6: '103871.1', 7: 'HQX0001000000000000990922', 8: '00004178', 9: 'JERX0010000417801', 10: 'CER', 11: 'CERWHF', 12: 'WHEAT FLOUR', 13: 'BY17', 14: 'BAG, POLYPROPYLENE, 50 KG', 15: 'G', 16: 'Good', 17: '10000.000', 18: '10020.390', 19: '200', 20: '275', 21: '0080003270'}, {0: 'ASHX004JERX0010000558101PULPULCKPBY17275', 1: 'OMC', 2: 'ISRAEL', 3: 'ASHDOD', 4: 'ASHX004', 5: 'ASHDOD_OVERSEAS_BONDED', 6: '103871.1', 7: 'HQX0001000000000000991507', 8: '00005581', 9: 'JERX0010000558101', 10: 'PUL', 11: 'PULCKP', 12: 'CHICKPEAS', 13: 'BY17', 14: 'BAG, POLYPROPYLENE, 50 KG', 15: 'G', 16: 'Good', 17: '500.000', 18: '510.054', 19: '100000', 20: '275', 21: '0080003713'}]]
    """

    data = list()

    from kiowa.db.utils import instance_as_dict
    waybill = Waybill.objects.get(id=wb_id)
    waybill_dict = instance_as_dict(waybill, exclude=['id'])

    from structures import waybill_named2positional_dict
    waybill_positional_dict = waybill_named2positional_dict(waybill_dict)

    data.append(waybill_positional_dict)

    # Add related LoadingDetais to serialized representation

    loading_details = waybill.loadingdetail_set.select_related()
    ld_list = []
    from structures import loadingdetail_named2positional_dict
    for l in loading_details:
        ld_dict = instance_as_dict(l, exclude=['id', 'wbNumber'])
        ld_positional_dict = loadingdetail_named2positional_dict(ld_dict)
        ld_list.append(ld_positional_dict)

    data.append(list(ld_list))

    # Add related LtiOriginals to serialized representation

    ltis = LtiOriginal.objects.filter(code=waybill.ltiNumber)
    ltis_list = []
    from structures import lti_named2positional_dict
    for lti in ltis:
        lti_dict = instance_as_dict(lti, exclude=['id'])
        lti_positional_dict = lti_named2positional_dict(lti_dict)
        ltis_list.append(lti_positional_dict)

    data.append(list(ltis_list))

    # Add related EpicStocks to serialized representation

    stocks_list = []
    from structures import stock_named2positional_dict
    for lti in ltis:
        for stock in lti.get_stocks():
            stock_dict = instance_as_dict(stock, exclude=['id'])
            stock_positional_dict = stock_named2positional_dict(stock_dict)
            stocks_list.append(stock_positional_dict)

    data.append(list(stocks_list))

    return data


def wb_compress_repr(wb_id):
    """
    This method compress the Waybill identified by the wb_id param and the related LoadingDetails, LtiOriginals, EpicStocks using zipBase64 algorithm.

    @param wb_id: the Waybill identifier
    @return: a string containing the compressed representation of the Waybill with related LoadingDetails, LtiOriginals and EpicStocks

    Usage:

    >>> wb_id = 3

    >>> c = wb_compress(wb_id)

    >>> c
    'eJztlW1r2zAQx7+KyevEnOQH2XvnxA/x6tSJnTbpSimFBDYoC6RdYYx+951OtiW7awZjY33RkIDu5Pju9P/d6frHCEYfrNHHpNoCMAYAn0QIbDkaWyMmd7bAfCEtLi2Oz0yATVggXc5Llytd8f7+y9P++F06POmoDnc7afjS2B3lUhhhMSr3HZDuQLqLMsvrdT6rrTJN81lSyZ1Q7qR39w97yo3SrqK8thZ5HBeJlUT12irWsU3blPvjA60p891XWlPKu3tlULJPR2VQoo+N4feDBT2TU2xGT3IKxNWaAjEKytXZqDXFYVQ2pzBcrSkKrUS3olCrqIjO4zwiDxW+KasittKyjK1lVWZVtFgkJAG0/3RYt+re64he4g69ahWH8tBJLejtu6xv8r7p9E23b3p9U+XwPLaub/DXxwzMD0LnsPlqC4ONMIQQT7Tl8NW/dmz+kuEWUZiAP8GjbBFVLjEBV0PaHIpvvKwj9VXSSC/eAbq5O+4/H76ZkEb1fKuZRCsuY82l3AWVhYJTPXBbXiZVjZFup+V5nMSaVymfBtYkRVG7SVXzilPYKKL758KoADzSQDCbadBPaqP4lz6XiUB3QdO0qg3Q2MxT3QqbeRKtrbQoLyrdE8wDG1+jG0M6nMZBxTjtNiVvPB42NuYoifsj2DCaeIftbcLWaqNh87yAadiWF4WGDY3Z2VLDNpvnaGNxxviFAWrS4Zqouf8OtSAErPodtf+Bms1skN+TvGmBFG8Bd0Megq95K3ODNzQuk0zzhkayjqZ4nu1jVJDjiT5zTuB2jm68GdAxZocmdIzbgYTOuE6bMzYQkkMYGM5bNXKnV0xw4XWwlYtZh1VeV1FSdCxp/dyBfN5p9fxhI4vfXhrB8M4IB52gytCoNbeJIk3fJoq0wW2iaJOVa7amUTa2lmVxhbAsr4rkPBlbHlhnmQYu06Rlh8NOo0YJtUopvtDF8W4KQePFG6ko3ebI23GFsoHDhTkwXionJxr29kWh5tcbU66dwJ1y7QAeKqfK0Mo1o1kpp0ezUq43mv+2bt5QNY+hw3PNkdB13KuyCUzr+ebmJ9TUrdY='
    """

    data = serialized_wb_repr(wb_id)
    from kiowa.utils.encode import DecimalJSONEncoder
    zippedData = zipBase64(json.dumps(data, cls=DecimalJSONEncoder))
    return zippedData


def wb_uncompress_repr(compressed_wb):
    """
    This method extracts from the compressed representation of the Waybill and related LoadingDetails, LtiOriginals, EpicStocks contained in comppressed_wb param
    the Waybill and the related LoadingDetail, LtiOriginals, EpicStocks instances.

    @param compressed_wb: the compressed representation of the Waybill and related LoadingDetails, LtiOriginals, EpicStocks
    @return: a list containing:
        - the Waybill positional dictionary in 1st element,
        - a list of related LoadingDetails positional dictionaries in 2nd element,
        - a list of related LtiOriginals positional dictionaries in 3th element,
        - a list of related EpicStocks positional dictionaries in 4th element.

    Usage:

    >>> c = 'eJztlW1r2zAQx7+KyevEnOQH2XvnxA/x6tSJnTbpSimFBDYoC6RdYYx+951OtiW7awZjY33RkIDu5Pju9P/d6frHCEYfrNHHpNoCMAYAn0QIbDkaWyMmd7bAfCEtLi2Oz0yATVggXc5Llytd8f7+y9P++F06POmoDnc7afjS2B3lUhhhMSr3HZDuQLqLMsvrdT6rrTJN81lSyZ1Q7qR39w97yo3SrqK8thZ5HBeJlUT12irWsU3blPvjA60p891XWlPKu3tlULJPR2VQoo+N4feDBT2TU2xGT3IKxNWaAjEKytXZqDXFYVQ2pzBcrSkKrUS3olCrqIjO4zwiDxW+KasittKyjK1lVWZVtFgkJAG0/3RYt+re64he4g69ahWH8tBJLejtu6xv8r7p9E23b3p9U+XwPLaub/DXxwzMD0LnsPlqC4ONMIQQT7Tl8NW/dmz+kuEWUZiAP8GjbBFVLjEBV0PaHIpvvKwj9VXSSC/eAbq5O+4/H76ZkEb1fKuZRCsuY82l3AWVhYJTPXBbXiZVjZFup+V5nMSaVymfBtYkRVG7SVXzilPYKKL758KoADzSQDCbadBPaqP4lz6XiUB3QdO0qg3Q2MxT3QqbeRKtrbQoLyrdE8wDG1+jG0M6nMZBxTjtNiVvPB42NuYoifsj2DCaeIftbcLWaqNh87yAadiWF4WGDY3Z2VLDNpvnaGNxxviFAWrS4Zqouf8OtSAErPodtf+Bms1skN+TvGmBFG8Bd0Megq95K3ODNzQuk0zzhkayjqZ4nu1jVJDjiT5zTuB2jm68GdAxZocmdIzbgYTOuE6bMzYQkkMYGM5bNXKnV0xw4XWwlYtZh1VeV1FSdCxp/dyBfN5p9fxhI4vfXhrB8M4IB52gytCoNbeJIk3fJoq0wW2iaJOVa7amUTa2lmVxhbAsr4rkPBlbHlhnmQYu06Rlh8NOo0YJtUopvtDF8W4KQePFG6ko3ebI23GFsoHDhTkwXionJxr29kWh5tcbU66dwJ1y7QAeKqfK0Mo1o1kpp0ezUq43mv+2bt5QNY+hw3PNkdB13KuyCUzr+ebmJ9TUrdY='

    >>> u = wb_uncompress_repr(c)

    >>> u
    [{u'42': u'False', u'43': u'False', u'24': u'1r', u'25': u'2r', u'26': u'', u'27': u'', u'20': u'1n', u'21': u'2n', u'22': u'1s', u'23': u'2s', u'46': u'', u'44': u'False', u'45': u'False', u'28': u'QALANDIA', u'29': u'WORLD FOOD PROGRAMME', u'40': u'False', u'41': u'False', u'1': u'X0167', u'0': u'JERX0011000Z7901P', u'3': u'2011-01-18', u'2': u'2011-01-18', u'5': u'Road', u'4': u'Delivery', u'7': u'JERX0010002630', u'6': u'dr', u'9': u'False', u'8': u'LOGISTICS OFFICER', u'39': u'QD9X001', u'11': u'ts', u'10': u'RAIS MIDDLE EAST LTD.', u'13': u'dln', u'12': u'dn', u'15': u'trn', u'14': u'vrn', u'16': u'False', u'18': u'False', u'31': u'', u'30': u'', u'37': u'False', u'36': u''}, [], [{u'24': u'WHEAT FLOUR', u'25': u'150.000', u'26': u'150.300', u'27': u'3000', u'20': u'HQX0001000000000000990922', u'21': u'00004178', u'22': u'CER', u'23': u'CERWHF', u'28': u'50.000', u'29': u'50.100', u'1': u'JERX001000000000000011031', u'0': u'JERX001000000000000011031HQX0001000000000000990922', u'3': u'2010-06-29', u'2': u'JERX0011000Z7901P', u'5': u'R001', u'4': u'2010-07-04', u'7': u'RAIS MIDDLE EAST LTD.', u'6': u'JERX001', u'9': u'Warehouse', u'8': u'2', u'11': u'ASHDOD', u'10': u'ASHX', u'13': u'ASHDOD_OVERSEAS_BONDED', u'12': u'ASHX004', u'15': u'QALANDIA', u'14': u'QD9X', u'17': u'WORLD FOOD PROGRAMME', u'16': u'WFP', u'19': u'103871.1', u'18': u'2010-06-29'}, {u'24': u'CHICKPEAS', u'25': u'200.000', u'26': u'200.400', u'27': u'4000', u'20': u'HQX0001000000000000991507', u'21': u'00005581', u'22': u'PUL', u'23': u'PULCKP', u'28': u'50.000', u'29': u'50.100', u'1': u'JERX001000000000000011031', u'0': u'JERX001000000000000011031HQX0001000000000000991507', u'3': u'2010-06-29', u'2': u'JERX0011000Z7901P', u'5': u'R001', u'4': u'2010-07-04', u'7': u'RAIS MIDDLE EAST LTD.', u'6': u'JERX001', u'9': u'Warehouse', u'8': u'2', u'11': u'ASHDOD', u'10': u'ASHX', u'13': u'ASHDOD_OVERSEAS_BONDED', u'12': u'ASHX004', u'15': u'QALANDIA', u'14': u'QD9X', u'17': u'WORLD FOOD PROGRAMME', u'16': u'WFP', u'19': u'103871.1', u'18': u'2010-06-29'}, {u'24': u'VEGETABLE OIL', u'25': u'357.000', u'26': u'384.000', u'27': u'30000', u'20': u'HQX0001000000000000890038', u'21': u'82492906', u'22': u'OIL', u'23': u'OILVEG', u'28': u'11.900', u'29': u'12.800', u'1': u'JERX001000000000000011031', u'0': u'JERX001000000000000011031HQX0001000000000000890038', u'3': u'2010-06-29', u'2': u'JERX0011000Z7901P', u'5': u'R001', u'4': u'2010-07-04', u'7': u'RAIS MIDDLE EAST LTD.', u'6': u'JERX001', u'9': u'Warehouse', u'8': u'2', u'11': u'ASHDOD', u'10': u'ASHX', u'13': u'ASHDOD_OVERSEAS_BONDED', u'12': u'ASHX004', u'15': u'QALANDIA', u'14': u'QD9X', u'17': u'WORLD FOOD PROGRAMME', u'16': u'WFP', u'19': u'10387.1.01.01', u'18': u'2010-06-29'}], [{u'20': u'275', u'21': u'0080003270', u'1': u'OMC', u'0': u'ASHX004JERX0010000417801CERCERWHFBY17275', u'3': u'ASHDOD', u'2': u'ISRAEL', u'5': u'ASHDOD_OVERSEAS_BONDED', u'4': u'ASHX004', u'7': u'HQX0001000000000000990922', u'6': u'103871.1', u'9': u'JERX0010000417801', u'8': u'00004178', u'11': u'CERWHF', u'10': u'CER', u'13': u'BY17', u'12': u'WHEAT FLOUR', u'15': u'G', u'14': u'BAG, POLYPROPYLENE, 50 KG', u'17': u'10000.000', u'16': u'Good', u'19': u'200', u'18': u'10020.390'}, {u'20': u'275', u'21': u'0080003713', u'1': u'OMC', u'0': u'ASHX004JERX0010000558101PULPULCKPBY17275', u'3': u'ASHDOD', u'2': u'ISRAEL', u'5': u'ASHDOD_OVERSEAS_BONDED', u'4': u'ASHX004', u'7': u'HQX0001000000000000991507', u'6': u'103871.1', u'9': u'JERX0010000558101', u'8': u'00005581', u'11': u'PULCKP', u'10': u'PUL', u'13': u'BY17', u'12': u'CHICKPEAS', u'15': u'G', u'14': u'BAG, POLYPROPYLENE, 50 KG', u'17': u'500.000', u'16': u'Good', u'19': u'100000', u'18': u'510.054'}]]
    """
    unbase64_data = base64.b64decode(compressed_wb.replace(' ','+'))
    unzipped = zlib.decompress(unbase64_data)

    deserialized_content = json.loads(unzipped)

    return deserialized_content
    
def restant_si(lti_code):
    """
    @todo: write method definition
    """
    detailed_lti = LtiOriginal.objects.filter(code=lti_code)
    listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code).filter(waybillSentToCompas=False)
    listOfSI = []
#    listExl =removedLtis.objects.list()

    for lti in detailed_lti:
        if not removedLtis.objects.filter(lti=lti.lti_pk):
            if lti.isBulk():
                listOfSI += [SIWithRestant(lti.si_code, lti.quantity_net, lti.cmmname)]
            else:
                listOfSI += [SIWithRestant(lti.si_code, lti.number_of_units, lti.cmmname)]

    for wb in listOfWaybills:
        for loading in wb.loadingdetail_set.select_related():
            for si in listOfSI:
                if si.SINumber == loading.siNo.si_code:
                    si.reduceCurrent(loading.numberUnitsLoaded)
    return listOfSI

##### Make Waybill number !!!! (make better)
def newWaybillNo(waybill):
    return 'E' + '%04d' % waybill.id
    
def new_waybill_no(waybill):
    """
    This method gives a waybill identifier for the waybill instance param, chaining the warehouse identifier char with the sequence of the table.
    Note: Different offliner app installation must have different warehouse identifier char.

    @param waybill: the Waybill instance
    @return: a string containing the waybill identifier.
    """
    return settings.WAYBILL_LETTER + '%04d' % waybill.id

def synchronize_waybill(waybill_id):
    """
    This method try to contact the online waybill application, and post's to an exposed url the serilized waybill.

    If all goes right the waybill data are uploaded from the offline application to the online application.

    @param waybill_id: the Waybill identifier
    @return: a string containing the message on the sync operation.

    Usage:

    >>> waybill_id = 81

    If the server can't be contacted:

    >>> synchronize_waybill(waybill_id)
    exception occurred
    [Errno 111] Connection refused
    closing connection

    If the server can be contacted:

    >>> synchronize_waybill(waybill_id)
    closing connection
    """
    serilized_waybill = serialize_wb(waybill_id)

    import httplib
    import urllib
    params = urllib.urlencode({'serilized_waybill': serilized_waybill})

    headers = {"Content-Type": "application/json", "Accept": "text/plain"}

    conn = httplib.HTTPConnection(settings.ONLINE_HOST_NAME, settings.ONLINE_HOST_PORT)

    response_message = None

    try:
        conn.request("POST", "/ets/waybill/synchro/upload/", params, headers)

        response = conn.getresponse()

        response_message = response.read()

    except Exception, e:
        print 'exception occurred'
        print e
    conn.close()

    return response_message


def synchronize_stocks(warehouse_code):
    """
    This method try to contact the online waybill application, and requests to an exposed url the serilized stocks.

    If all goes right the stocks data are downloaded from the online application to the offline application.

    @param warehouse_code: the warehouse identifier
    @return: a string containing the message on the sync operation.

    Usage:

    >>> warehouse_code = 'ASHX004'

    If the server can't be contacted:

    >>> response = synchronize_stocks(warehouse_code)
    exception occurred
    [Errno 111] Connection refused
    closing connection

    If the server can be contacted:

    >>> response = synchronize_stocks(warehouse_code)
    closing connection
    """

    headers = {"Content-Type": "text/plain", "Accept": "application/json"}

    import httplib
    conn = httplib.HTTPConnection(settings.ONLINE_HOST_NAME, settings.ONLINE_HOST_PORT)

    try:
        conn.request("GET", "/ets/stock/synchro/download/?warehouse_code="+warehouse_code, {}, headers)

        response = conn.getresponse()
        data = response.read()

        # Try to update the stock data on local offline db
        r = json.loads(data)
        for el in r:
            x = EpicStock()
            for k, v in el.items():
                setattr(x, k, v)
            x.save()

        message = 'Synchronization done on Stock'

    except Exception, e:
        message = 'Synchronization not done on Stock, verify your connection'
        print 'exception occurred'
        print e

    conn.close()

    return message


def wb_compress(wb_id):
    """
    This method compress the Waybill identified by the wb_id param using zipBase64 algorithm.

    @param wb_id: the Waybill identifier
    @return: a string containing the compressed representation of the Waybill with related LoadingDetails, LtiOriginals and EpicStocks

    Usage:

    >>> wb_id = 3

    >>> c = wb_compress(wb_id)

    >>> c
    'eJzlWG1P4zgQ/itRPkPlpC1t71sgaeltICUtb3c6RSFxWx+pnXVSuGrFf79x3tOmRQu7sKdDfEAeezzzzPNMxvz5TQ4f5d+k9pEkr5iPA/hbZvN5QCjmrWd380CCQAbjnODAj8D6Tc5WL9erB8zF/juknPTEppi7NAoZj2/wkngBtvGCRLAYE0bFxidOa9vOGIW/vZglbmxtPJUuxrpuGpKhTWeSOdNbYr9PotCNvaWNVy5/FEHIPk8MboytuZ6ZxbqKFOUYKcdKX9g59khIMI01zsmTG+iwH3bRdRBUrRBGROgCC5t8a9mmLg0tS5cmtjWytYsLoxb0dP1QjzuOanYdB+QJ882ULCj2Z2SFo9hdhQ33QuCxS72mkC7dVRKN8OyufQIxrlawnq/lkGCeXgPrczeIMJiy8kw483AUYX/I+MTdZIfzTcVFe6Msb5iROEiCMa3ReDobn00lazgcnxm2iMQDLFzBltkzm2K3Qgv1EC6VWKoeshLbEB4Oi2yDmJRufzfsOwRlRgj90RsgZVKLwqK42UcZh0jMW+5NPNkIxQXOzjZhkrhumMIFocAhIkj3Svg1RnJ5F+/K8ea4KhtSkpvM9YGjBzhuUB9ceEuXL/AeolcEJJdMmYJlxoBgoRs1UiR2k+iaXDfgXk1e4dvFqVNEiSpx3DSAW6CTlwKpCf2haIQmfeXW5XjJ1lFivdIHghs1XEzmFQ3oSjO1S32sVW4FmuwBoKwMF8TNJenTugDz9YyXQEv1pI3kXQcm8TCofawnXgK6DU0FFlrLoBDgtt4qWqP1lDAJ48N4cpcEmG936Bg69MvLkZR9FipJlT8gvbZyfnWHtgyDARqoSXl2vySgYMbJAmq2/TVJl50gq5LjwVlxVJue34mtEXEACMZ9h4hE5IMXl84cmpUF/OiWniLnVwtVbyAVRu3GImglNn1duzQm8cahOOkrShe1wEtWlgiDcnFx6HY4qZ1ZcBZF+al2fmoFWAlrfgq66u35sCGiIqEqhzn+uoZt2HdyPjp+qk/RJdAxOjlWBzUqFm72fm3XlMTOMyaLZZznWaZZ+mFrrwJmBfznZa2GCHWyFp4VcC+lxDaaMNphc0eEkcDVzq6uxlVgCZEpJZQO1A0vGK/BWQ+tTgvHujHsKaTvnFqXupHQBP8TEvBQx7F3nKYRcvY39iCOh8jBAc4/yRB+v6e0khS81Sq/5Pbc0GbS0LSu7RyD5vKU7CmO7hlD0kxi6IYOECQpQdkBawXKIbDr5YmzRqpm4sq3iTJ0lF7/HfIHYvc+Rf75xR8sfxW9Rf7iVGef/CfX5tmXpoj+t/LvvEf+AOcnyv/sfAzFBPf/CfF3u33lzeLvDxBg8AniLy/+YPG3u703iL/d75SntsVvjc0bY/SLiV9RWoNP/fbvV7+itvqH1A94fpj6W0oLid+tFgD1NGbaKeCcBfNLt4G+2hmoA3RSawNZISulE2MCUmC0SofV03ulp/a6zeLHIfGimHmPW9L/rrG+YYaGVxZM0QOUmQOwCiySx9CIMX/fdNM0xQtjrsoMoR26pjknj6xGjsPT/dFd4Lx0p9roSJpY5j0UbnJvGpfGkdRF0pfRq6Nq4n5NY74Ri+OpraX/fID1oPKSLVsbx3PMxcPSocVzEPoixNxWeyg7yuGdx0QDFrK4OKugll8/yna+rpFDj5YMhsIiuCHW3WCnsWaU2VU9DEjvmrQPk1d85qDvX5vpqPXzyJsPpbvk7SpAt27nO6ibfJsbqNt9nbhpvj+TuNmQ9SOJ21PaH0Lcctz+EcRNCfCOMfHl5a9/AexyIYk='
    """

    data = serialize_wb(wb_id)
    from kiowa.utils.encode import DecimalJSONEncoder
    zippedData = zipBase64(json.dumps(data, cls=DecimalJSONEncoder))

    return zippedData


class DefaultMappingDict(dict):
    """
    This class is a mapping dictionary.
    """

    def __init__(self, *args, **kwargs):
        self._default = kwargs.pop('default')
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except:
            return self._default

def zipBase64(data):
    """
    This method compress the data param and after encodes it using b64encode algorithm.

    @param data: the string data to compress
    @return: a string containing the compressed and encoded data

    Usage:

    >>> data = 'Some data...'

    >>> z = zipBase64(data)

    >>> z
    'eJwLzs9NVUhJLEnU09MDABtiA9k='
    """

    zippedData = zlib.compress(data)
    base64Data = base64.b64encode(zippedData)
    return base64Data

    
     


####
    
def update_persons():
    """
    Executes Imports of LTIs Persons
    Fix to include Compas Station
    """
    
    originalPerson = EpicPerson.objects.using('compas').filter(org_unit_code=settings.COMPAS_STATION)
    for my_person in originalPerson:
        my_person.save(using='default')    



## Importing Needs to add imports for DispatchPoint & ReceptionPoint

def import_setup():
    ## read all ltis from compas & extract Dispatch points & reception points
    #select distinct origin_loc_name,origin_location_code,origin_wh_name,origin_wh_code from epic_lti
    #select distinct destination_location_code,consegnee_name,destination_loc_name,consingee_code from epic_lti
    disp = LtiOriginal.objects.using('compas').values('origin_loc_name','origin_location_code','origin_wh_name','origin_wh_code').filter(lti_id__startswith=settings.COMPAS_STATION).distinct()
    rec = LtiOriginal.objects.using('compas').values('destination_location_code','consegnee_name','destination_loc_name','consegnee_code').filter(lti_id__startswith=settings.COMPAS_STATION).distinct()
    ## maybe add a time limit?
    for d in rec:
        this_dp,created = ReceptionPoint.objects.get_or_create(LOC_NAME=d['destination_loc_name'],LOCATION_CODE=d['destination_location_code'],consegnee_name=d['consegnee_name'],consegnee_code=d['consegnee_code'])
        if created:
            this_dp.ACTIVE_START_DATE = datetime.date(9999,12,31)
            this_dp.save()

    for d in disp:
        this_dp,created = DispatchPoint.objects.get_or_create(origin_loc_name=d['origin_loc_name'],origin_location_code=d['origin_location_code'],origin_wh_name=d['origin_wh_name'],origin_wh_code=d['origin_wh_code'])
        if created:
            this_dp.ACTIVE_START_DATE = datetime.date(9999,12,31)
            this_dp.save()

    
    
def import_geo():
    """
    Executes Imports of places
    """
    ## Fix countries, get by config
    
    #UPDATE GEO
    #loop thrugh CC
    for country in settings.COUNTRIES:
        try:
            my_geo = places.objects.using('compas').filter(COUNTRY_CODE=country)
            for the_geo in my_geo:
                    the_geo.save(using='default')
        except:
            pass    
    return True

def import_stock():
    """
    Executes Imports of Stock
    """
    originalStock = EpicStock.objects.using('compas')
    for myrecord in originalStock:
        myrecord.save(using='default')
    
    current_stock = EpicStock.objects.all()
    for item in current_stock:
        if item not in originalStock:
            item.number_of_units = 0;
            item.save()
            
def import_lti():
    listRecepients = ReceptionPoint.objects.values('consegnee_code','LOCATION_CODE','ACTIVE_START_DATE').filter(ACTIVE_START_DATE__lt=datetime.date.today()).distinct()
    listDispatchers = DispatchPoint.objects.values('origin_wh_code','ACTIVE_START_DATE').filter(ACTIVE_START_DATE__lt=datetime.date.today()).distinct()
    # check what type is the comodity... if bulk swap
    
    ## TODO: Fix so ltis imported are not expired
    original = LtiOriginal.objects.using('compas').filter(requested_dispatch_date__gt='2011-01-01')
    # log each item
    for myrecord in original:
        not_in = True
        for rec in listRecepients:
            if myrecord.consegnee_code in rec['consegnee_code'] and myrecord.destination_location_code in rec['LOCATION_CODE'] and myrecord.lti_date >=  rec['ACTIVE_START_DATE']:
                for disp in listDispatchers:
                    if myrecord.origin_wh_code in disp['origin_wh_code'] and myrecord.lti_date >=  disp['ACTIVE_START_DATE']:
                        myrecord.save(using='default') ## here we import the record...
                        try:
                            myr = removedLtis.objects.get(lti=myrecord)
                            myr.delete()
                        except:
                            pass
                        try:
                            mysist =myrecord.sitracker #try to get it, if it exist check LTI NOU and update if not equal#Use get or create!!

                            if mysist.number_units_start != myrecord.number_of_units:
                                try:
                                    change = myrecord.number_of_units - mysist.number_units_start 
                                    mysist.number_units_left =    mysist.number_units_left + change    
                                    mysist.save(using='default')    
                                except:
                                    pass
                        except:
                            mysist = SiTracker()
                            mysist.LTI=myrecord
                            mysist.number_units_left = myrecord.number_of_units
                            mysist.number_units_start = myrecord.number_of_units
                            mysist.save(using='default')
                        not_in = False
                        break
                    
                not_in = False
                break
            else:
                #pass# not here (remove if it should no be here)
                try:
                    LtiOriginal.objects.get(id = myrecord.id)
                except:
                    pass
                

    #cleanup ltis loop and see if changes to lti ie deleted rows
    current = LtiOriginal.objects.all()
    for c in current:
        if c not in original:
            c.remove_lti()
    #    if c.expiry_date < datetime.date.today():
    #        c.remove_lti()

            
def getMyProfile(request):
    myprofile =''
    try:
        myprofile = request.user.profile
    except:
        pass
    return myprofile

def printIt(line):
#    print line
    pass

    