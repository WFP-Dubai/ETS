'''
Created on 03/dic/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

import json
import zlib, base64

from django.conf import settings
from django.core import serializers

from offliner.models import LtiOriginal, Waybill, RemovedLtis, SIWithRestant, EpicStock, WaybillSynchroState, Places



def serialize_wb(wb_id):
    '''
    This method serializes the Waybill identified by the wb_id param and the relateds LoadingDetails.
    
    @param wb_id: the Waybill identifier   
    @return the serialized json data.
    
    Usage:
    >>> wb_id = 81
    
    >>> s = serialize_wb(wb_id)
    
    >>> s
    '[{"pk": 81, "model": "offliner.waybill", "fields": {"waybillNumber": "X0081", "transportVehicleRegistration": "", "transportContractor": "RAIS MIDDLE EAST LTD.", "dispatchRemarks": "", "dateOfDispatch": "2010-12-13", "recipientArrivalDate": null, "recipientConsingee": "WORLD FOOD PROGRAMME", "transportSubContractor": "", "transportDeliverySignedTimestamp": null, "recipientDistance": null, "recipientName": "", "auditComment": "", "dispatcherSigned": false, "waybillProcessedForPayment": false, "recipientSignedTimestamp": null, "dispatcherTitle": "LOGISTICS OFFICER", "containerTwoSealNumber": "", "transportDeliverySigned": false, "containerTwoRemarksReciept": "", "ltiNumber": "JERX0011000A2040P", "containerOneRemarksReciept": "", "transportDispachSignedTimestamp": null, "transactionType": "DEL", "invalidated": false, "containerTwoRemarksDispatch": "", "recipientSigned": false, "transportDispachSigned": false, "dateOfLoading": "2010-12-13", "recipientEndDischargeDate": null, "recipientRemarks": "", "waybillSentToCompas": false, "recipientStartDischargeDate": null, "containerOneRemarksDispatch": "", "containerOneSealNumber": "", "waybillValidated": false, "transportType": "02", "destinationWarehouse": "QD9X001", "recipientLocation": "QALANDIA", "waybillRecSentToCompas": false, "transportDriverName": "", "dispatcherName": "JERX0010002630", "transportDriverLicenceID": "", "containerOneNumber": "", "recipientTitle": "", "containerTwoNumber": "", "waybillReceiptValidated": false, "transportTrailerRegistration": ""}}]'    
    '''
    
    waybill_to_serialize = Waybill.objects.get(id=wb_id)   
    items_to_serialize = waybill_to_serialize.loadingdetail_set.select_related() 
    data = serializers.serialize('json', [waybill_to_serialize] + list(items_to_serialize))
    return data


def wb_compress(wb_id):
    '''
    This method compress the Waybill identified by the wb_id param using zipBase64 algorithm.
    
    @param wb_id: the Waybill identifier   
    @return: a string containing the compressed representation of the Waybill with related LoadingDetails    
    
    Usage:
    >>> wb_id = 81
    
    >>> c = wb_compress(wb_id)

    >>> c
    'eJyFVMFuozAQ/RXEeVtBulp194ZiUrEiIQXUVlrtwYFJYtXYyHZaRVX/fceUEEhI9gYzz+M3b974z4dbv7q/nHv/m+NWsgSOP65crzkToG7f6X7FOHcxuWbAS43ZD7eNLnbVCpTFv3jevW9BRlGha6nME2xZwSGFDdMYNEwKCxxgplLgd2FkUyMNosyZR4TEoRMGWe7EObm1+JLpmppim0JF1as+lCmpgWRN2qSNTjzfu/EnN/6dzSsoWM1AmEAp9kY5QTyixI7zfhZJaCY2YHPuc5LGxJklCXGWafKQBvN5OKCc7VZD1oMsAc7eQO0zthFQ5qwCbWhVj9yKtA0VxRihBa3gUJnuSoYMqwrjXd9tx6C+rsH4mnINmGrnslSyAK2hnEm1pPv28AHUXXSR5fGGnBnekImThyjLo2nmJLNZNA1Ty6RAJai1Sf4uM6A9P1xRpcekf74dborkoO565YYdi/4OU/SZ73ueF0y8795ywCERMF7jyMO2VWwvtt0AcbBo1XxfN22TMLYlmED/MGu4/9Dvu9E917p3eJxVD/Bl71jSEt15xd2hKLFEsaVqAxcsfrI4rUsyzOQSzVVTPWoPQxt2Y6VHVD9tvQ85N0fL4WlE1k6ZwxC8SWN7HBcTzUPyTBVs5U432Ufy07pioEksi+7FeQziYEGioHcrGuRC88epKGvZ/ioel+IQbf2Idpz8uPPc8+MxKwB3PCJjmgz16Kh3G3e6YKP6YSfAanNdRkUZB3X2En9+/v0HMgMAVg=='   
    '''
    
    data = serialize_wb(wb_id)    
    zippedData = zipBase64(data)   
    return zippedData


def serialized_wb_repr(wb_id):
    '''
    This method serializes the Waybill identified by the wb_id param and the relateds LoadingDetails.
    Return the serialized data.
    
    @param wb_id: the Waybill identifier 
    @return: a list containing the Waybill positional dictionary as first element and a list of related LoadingDetails positional dictionaries as second element
    
    Usage:
    >>> wb_code = 159
    
    >>> s = serialized_wb_repr(wb_id) 
    
    >>> s
    [[(0, 'X0159'), (1, 'Vehicle Registration No'), (2, 'RAIS MIDDLE EAST LTD.'), (3, 'Dispatch Remarks'), (4, '2010-12-22'), (5, 'False'), (6, 'WORLD FOOD PROGRAMME'), (7, 'Transport Subcontractor'), (8, ''), (9, 'Print Dispatch Original'), (10, 'True'), (11, 'False'), (12, 'LOGISTICS OFFICER'), (13, 'Container 2: Seal:'), (14, 'False'), (15, ''), (16, 'JERX0011000A2066P'), (17, ''), (18, '2010-12-22 16:03:56.145471'), (19, 'Delivery'), (20, 'Container 2: Remarks:'), (21, 'False'), (22, 'True'), (23, '2010-12-22'), (24, ''), (25, 'False'), (26, 'Container 1: Remarks:'), (27, 'Container 1: Seal:'), (28, 'False'), (29, 'Road'), (30, 'QD9X001'), (31, 'QALANDIA'), (32, 'False'), (33, "Driver's Name"), (34, 'JERX0010002630'), (35, "Driver's Licens No"), (36, 'Container 1: Number:'), (37, ''), (38, 'Container 2: Number:'), (39, 'False'), (40, 'Trailer Registration No')], [[(0, '0.000'), (1, 'True'), (2, 'JERX001000000000000011128HQX0001000000000000907177'), (3, '300.000'), (4, 'False'), (5, '0.000'), (6, 'False'), (7, '0.000')], [(0, '0.000'), (1, 'True'), (2, 'JERX001000000000000011128HQX0001000000000000992018'), (3, '600.000'), (4, 'False'), (5, '0.000'), (6, 'False'), (7, '0.000')]]]     
    '''
    
    data = list() 
        
    from kiowa.db.utils import instance_as_dict
    waybill = Waybill.objects.get(id=wb_id)   
    waybill_dict = instance_as_dict(waybill, exclude=['id'])

    #waybill_positional_dict = zip(range(len(waybill_dict.values())), waybill_dict.values())

    from structures import waybill_named2positional_dict
    waybill_positional_dict = waybill_named2positional_dict(waybill_dict)

    data.append(waybill_positional_dict) 
    
    loading_details = waybill.loadingdetail_set.select_related() 
    ld_list = []
    from structures import loadingdetail_named2positional_dict
    for l in loading_details:
        ld_dict = instance_as_dict(l, exclude=['id','wbNumber'])

        #ld_positional_dict = zip(range(len(ld_dict.values())), ld_dict.values())

        ld_positional_dict = loadingdetail_named2positional_dict(ld_dict)

        ld_list.append(ld_positional_dict)
        
    data.append(list(ld_list))
    
    return data


def wb_compress_repr(wb_id):
    '''
    This method compress the Waybill identified by the wb_id param and the related LoadingDetails using zipBase64 algorithm.
    
    @param wb_id: the Waybill identifier 
    @return: a string containing the compressed representation of the Waybill with related LoadingDetails 
    
    Usage:
    >>> wb_id = 159
    
    >>> c = wb_compress(wb_id)

    >>> c
    'eJzlVcFuozAQ/RWLy17aCqiaNrmhkHSzoiEFtq202oMDTmLVYGQ7raKq/75jAsEkpHtdaXtq5g3jN2/e2L8+rPLVGiHnZniBrJxnhMEvi69WjBZEXL3j3ZIyZgG4ooRlEtAPq47Ot/mSCJ3/YkMBnaQELmTJhXoiG5oyEpE1lRBUlBc6sQ4jM47mvPPpmBfwf6p4VTryZjF6mPl+MEETL05QkPhXOj+jssQq3UQkx+JVE7P8OoSamE7DioSrBtFZru3Yl4576boaFySlJSWF8oSgb5j5kA9ZxZYxEwVSkhZrojHrOYwCH03D0EeLKLyPvIeHSaeFeLvsdpE0CAIobSHzI58w+kbELqbrgmQJzYlUOC97yEA3ChdpH885ziuKujLeZhSI5znEdWwhaKHQQaRQ0DUtMDPFJGJ/OqQrsSWA1LNeCJ4SKUk25WKBd3XJFWaSmMef5d4ekFDFKopBeD+Lk9k4RuF0OhtPIk1Ea4O19ZJ3HhNseGzcIMgdIQ2NvlDP4GZWrH0RAV1SqkYnpmh7zI9J9GLbjmPbtufag8GiwyosSH+NloduNN2cCmH4DjmDkX09uhkcvgQ3wCYku7JSxp8EGqEF+JFqA/+lH9PdHZlqfGSdzsio2M+9tcB+hQKOM9iALzZoUmRQId1gsSZn1shYVqs1VwxIwsGpJZa9rlK4ItdXumc0/XI4XTnM784ZzTGMVlN96pnIQb9mfnalSwajh/3Sg33Ggmz4Vlbooz/UDutIF/D0cEc+eoE392eecSqY7YxG7eyEtn+z/vtf3ySqAp39a1Jqo4PP3cG1bZ3WCmhK4JKZ+Z2CVVTWd7Yp4hkB9+GuAw9XwPHGn9l2o0YrCKGl+noaAlNGxPETVIdPnqDPzwvUvIYDp/c1ZPsVyAhQO34Ti4rjz4Iqec95VtngCsTVaVsd9XGO13Al7D1Su7dCAi5hMbCs+NWAUU7DnXLvy4NO+3ebw2g0N5JVH7SbKyk01pl1++c4jnv3/fHFPgKG9q1ze2sdc9DVdalru7etY/6Hxrr91gr6lYJnLK27CUFySG3aaSCDUX1uK0xnfu5/PL8hXM93Z+c3+Hfn9/sPw3932A=='

    '''
    
    data = serialized_wb_repr(wb_id)
    zippedData = zipBase64(json.dumps(data))
    return zippedData


def wb_uncompress_repr(compressed_wb):
    '''
    This method extracts from the compressed representation of the Waybill and related LoadingDetails contained in comppressed_wb param 
    the Waybill and the related LoadingDetail instances.
    
    @param compressed_wb: the compressed representation of the Waybill and related LoadingDetails
    @return: a list containing the Waybill positional dictionary in first element and a list of related LoadingDetails positional dictionaries in second element
     
    ''' 

    unbase64_data = base64.b64decode(compressed_wb)

    unzipped = zlib.decompress(unbase64_data)

    deserialized_content = json.loads(unzipped)

    return deserialized_content
  

def zipBase64(data):
    '''
    This method compress the data param and after encodes it using b64encode algorithm.
    
    @param data: the string data to compress 
    @return: a string containing the compressed and encoded data     
    
    Usage:
    
    >>> data = 'Some data...'
       
    >>> z = zipBase64(data)
    
    >>> z
    'eJwLzs9NVUhJLEnU09MDABtiA9k='
    '''    
    
    zippedData = zlib.compress(data)
    base64Data = base64.b64encode(zippedData)
    return base64Data

    
def restant_si(lti_code):
    '''
    @todo: write 
    '''
    detailed_lti = LtiOriginal.objects.filter(code=lti_code)
    listOfWaybills = Waybill.objects.filter(invalidated=False).filter(ltiNumber=lti_code).filter(waybillSentToCompas=False)
    listOfSI = []
#    listExl =removedLtis.objects.list()
    
    for lti in detailed_lti:
        if not RemovedLtis.objects.filter(lti=lti.lti_pk):
            if lti.isBulk():
                listOfSI += [SIWithRestant(lti.si_code, lti.quantity_net, lti.cmmname)]
                #print 'bulk'
            else:
                listOfSI += [SIWithRestant(lti.si_code, lti.number_of_units, lti.cmmname)]
                #print 'not bulk'

    for wb in listOfWaybills:
        for loading in wb.loadingdetail_set.select_related():
            for si in listOfSI:
                if si.SINumber == loading.siNo.si_code:
                    si.reduceCurrent(loading.numberUnitsLoaded)
    return listOfSI
     
     
def new_waybill_no(waybill):
    return settings.WAYBILL_LETTER + '%04d' % waybill.id


def synchronize_waybill(waybill_id):
    '''
    This method try to contact the online waybill application, and post's to an exposed url the serilized waybill. 
    If all goes right the waybill data are uploaded from the offline application to the online application.
    
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
    '''    
    serilized_waybill = serialize_wb(waybill_id) 
    
    import httplib, urllib
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
    
    print 'closing connection'
    conn.close()
    
    return response_message
    

def synchronize_stocks(warehouse_code):
    '''
    This method try to contact the online waybill application, and requests to an exposed url the serilized stocks. 
    If all goes right the stocks data are downloaded from the online application to the offline application.

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
    '''
       
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
            for k,v in el.items():
                setattr(x, k, v)
            x.save()
       
        message = 'Synchronization done on Stock'
    
    except Exception, e:
        message = 'Synchronization not done on Stock, verify your connection'
        print 'exception occurred'
        print e      
    
    print 'closing connection'
    conn.close()
    
    return message
    
    
class DefaultMappingDict(dict):
    '''
    This class is a mapping dictionary.
    '''
    
    def __init__(self, *args, **kwargs):
        self._default = kwargs.pop('default')        
        dict.__init__(self, *args, **kwargs)

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except:
            return self._default
    
            
def synchronize_ltis(warehouse_code):
    '''
    This method try to contact the online waybill application, and requests to an exposed url the serilized ltis. 
    If all goes right the ltis data are downloaded from the online application to the offline application.
    
    Usage:
    
    >>> warehouse_code = 'ASHX004'
    
    If the server can't be contacted:
    
    >>> response = synchronize_ltis(warehouse_code)
    exception occurred
    [Errno 111] Connection refused
    closing connection
    
    If the server can be contacted:
    
    >>> response = synchronize_ltis(warehouse_code)
    closing connection
    '''
       
    headers = {"Content-Type": "text/plain", "Accept": "application/json"}
    
    import httplib
    conn = httplib.HTTPConnection(settings.ONLINE_HOST_NAME, settings.ONLINE_HOST_PORT)
    
    # Create a DefaultMappingDict used for Waybill field names between Waybill online and offline structures
    mapping = DefaultMappingDict( default=lambda x: x.lower())
    
    try:
        conn.request("GET", "/ets/lti/synchro/download/?warehouse_code="+warehouse_code, {}, headers)
    
        response = conn.getresponse()
        data = response.read()
        
        # Try to update the stock data on local offline db
        r = json.loads(data)
        for el in r:
            x = LtiOriginal()
            for k,v in el.items():
                setattr(x, mapping[k](k), v)
            x.save()
       
        message = 'Synchronization done on Lti'
    
    except Exception, e:
        message = 'Synchronization not done on Lti, verify your connection'
        print 'exception occurred'
        print e      
    
    print 'closing connection'
    conn.close()
    
    return message


def synchronize_receipt_waybills(warehouse_code):
    '''
    This method try to contact the online waybill application, and requests to an exposed url the serilized receipt waybills. 
    If all goes right the receipt waybills data are downloaded from the online application to the offline application.
    
    Usage:
    
    >>> warehouse_code = 'ASHX004'
    
    If the server can't be contacted:
    
    >>> response = synchronize_receipt_waybills(warehouse_code)
    exception occurred
    [Errno 111] Connection refused
    closing connection
    
    If the server can be contacted:
    
    >>> response = synchronize_receipt_waybills(warehouse_code)
    closing connection
    '''
       
    headers = {"Content-Type": "text/plain", "Accept": "application/json"}
    
    import httplib
    conn = httplib.HTTPConnection(settings.ONLINE_HOST_NAME, settings.ONLINE_HOST_PORT)
    
    try:
        conn.request("GET", "/ets/waybill/synchro/download/?warehouse_code="+warehouse_code, {}, headers)
    
        response = conn.getresponse()
        data = response.read()
        
        # Try to update the receipt waybill data on local offline db
        r = json.loads(data)
        
        for el in r:
            x = Waybill()
            for k,v in el.items():
                if not k=='id' and not k=='destinationWarehouse':
                    setattr(x, k, v)
              
            x.destinationWarehouse = Places.objects.get(org_code=settings.OFFLINE_ORIGIN_WH_CODE)
            # perform an insert
            if Waybill.objects.filter(waybillNumber=x.waybillNumber).count()==0: 
                x.id = None 
            # perform an update
            else:
                x.id = Waybill.objects.filter(waybillNumber=x.waybillNumber)[0].id
            x.save()    
        
        message = 'Synchronization done on receipt Waybill'

    except Exception, e:
        message = 'Synchronization not done on receipt Waybill, verify your connection'
        print 'exception occurred'
        print e      
    
    print 'closing connection'
    conn.close()
    
    return message
