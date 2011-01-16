'''
Created on 13/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-


class WaybillFieldsMap:

    NAME_2_POSITION = {
        'ltiNumber' : 0,
        'waybillNumber' : 1,
        'dateOfLoading' : 2,
        'dateOfDispatch' : 3,
        'transactionType' : 4,
        'transportType' : 5,
        'dispatchRemarks' : 6,
        'dispatcherName' : 7,
        'dispatcherTitle' : 8,
        'dispatcherSigned' : 9,
        'transportContractor' : 10,
        'transportSubContractor' : 11,
        'transportDriverName' : 12,
        'transportDriverLicenceID' : 13,
        'transportVehicleRegistration' : 14,
        'transportTrailerRegistration' : 15,
        'transportDispachSigned' : 16,
        'transportDispachSignedTimestamp' : 17,
        'transportDeliverySigned' : 18,
        'transportDeliverySignedTimestamp' : 19,
        'containerOneNumber' : 20,
        'containerTwoNumber' : 21,
        'containerOneSealNumber' : 22,
        'containerTwoSealNumber' : 23,
        'containerOneRemarksDispatch' : 24,
        'containerTwoRemarksDispatch' : 25,
        'containerOneRemarksReciept' : 26,
        'containerTwoRemarksReciept' : 27,
        'recipientLocation' : 28,
        'recipientConsingee' : 29,
        'recipientName' : 30,
        'recipientTitle' : 31,
        'recipientArrivalDate' : 32,
        'recipientStartDischargeDate' : 33,
        'recipientEndDischargeDate' : 34,
        'recipientDistance' : 35,
        'recipientRemarks' : 36,
        'recipientSigned' : 37,
        'recipientSignedTimestamp' : 38,
        'destinationWarehouse' : 39,
        'waybillValidated' : 40,
        'waybillReceiptValidated' : 41,
        'waybillSentToCompas' : 42,
        'waybillRecSentToCompas' : 43,
        'waybillProcessedForPayment' : 44,
        'invalidated' : 45,
        'auditComment' : 46,
    }

    POSITION_2_NAME = {
        '0' : 'ltiNumber',
        '1' : 'waybillNumber',
        '2' : 'dateOfLoading',
        '3' : 'dateOfDispatch',
        '4' : 'transactionType',
        '5' : 'transportType',
        '6' : 'dispatchRemarks',
        '7' : 'dispatcherName',
        '8' : 'dispatcherTitle',
        '9' : 'dispatcherSigned',
        '10' : 'transportContractor',
        '11' : 'transportSubContractor',
        '12' : 'transportDriverName',
        '13' : 'transportDriverLicenceID',
        '14' : 'transportVehicleRegistration',
        '15' : 'transportTrailerRegistration',
        '16' : 'transportDispachSigned',
        '17' : 'transportDispachSignedTimestamp',
        '18' : 'transportDeliverySigned',
        '19' : 'transportDeliverySignedTimestamp',
        '20' : 'containerOneNumber',
        '21' : 'containerTwoNumber',
        '22' : 'containerOneSealNumber',
        '23' : 'containerTwoSealNumber',
        '24' : 'containerOneRemarksDispatch',
        '25' : 'containerTwoRemarksDispatch',
        '26' : 'containerOneRemarksReciept',
        '27' : 'containerTwoRemarksReciept',
        '28' : 'recipientLocation',
        '29' : 'recipientConsingee',
        '30' : 'recipientName',
        '31' : 'recipientTitle',
        '32' : 'recipientArrivalDate',
        '33' : 'recipientStartDischargeDate',
        '34' : 'recipientEndDischargeDate',
        '35' : 'recipientDistance',
        '36' : 'recipientRemarks',
        '37' : 'recipientSigned',
        '38' : 'recipientSignedTimestamp',
        '39' : 'destinationWarehouse',
        '40' : 'waybillValidated',
        '41' : 'waybillReceiptValidated',
        '42' : 'waybillSentToCompas',
        '43' : 'waybillRecSentToCompas',
        '44' : 'waybillProcessedForPayment',
        '45' : 'invalidated',
        '46' : 'auditComment'
    }

def waybill_name2position(name):
    return WaybillFieldsMap.NAME_2_POSITION[name]

def waybill_position2name(position):
    return WaybillFieldsMap.POSITION_2_NAME[position]

def waybill_named2positional_dict(name_dict):
    positional_dict = {}
    for key, value in name_dict.items():
        #positional_dict["W%s" % str(waybill_name2position(key))] = value
        positional_dict[waybill_name2position(key)] = value
    return positional_dict

def waybill_positional2named_dict(positional_dict):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[waybill_position2name(key)] = value
    return named_dict
    

class LoadingDetailFieldsMap():

    NAME_2_POSITION = {
        'wbNumber' : 0,
        'siNo' : 1,
        'numberUnitsLoaded' : 2,
        'numberUnitsGood' : 3,
        'numberUnitsLost' : 4,
        'numberUnitsDamaged' : 5,
        'unitsLostReason' : 6,
        'unitsDamagedReason' : 7,
        'unitsDamagedType' : 8,
        'unitsLostType' : 9,
        'overloadedUnits' : 10,
        'loadingDetailSentToCompas' : 11,
        'overOffloadUnits' : 12
    }

    POSITION_2_NAME = {
        '0' : 'wbNumber',
        '1' : 'siNo',
        '2' : 'numberUnitsLoaded',
        '3' : 'numberUnitsGood',
        '4' : 'numberUnitsLost',
        '5' : 'numberUnitsDamaged',
        '6' : 'unitsLostReason',
        '7' : 'unitsDamagedReason',
        '8' : 'unitsDamagedType',
        '9' : 'unitsLostType',
        '10' :'overloadedUnits',
        '11' : 'loadingDetailSentToCompas',
        '12' : 'overOffloadUnits'
    }

def loadingdetail_name2position(name):
    return LoadingDetailFieldsMap.NAME_2_POSITION[name]

def loadingdetail_position2name(position):
    return LoadingDetailFieldsMap.POSITION_2_NAME[position]

def loadingdetail_named2positional_dict(name_dict):
    positional_dict = {}
    for key, value in name_dict.items():
        #positional_dict["L%s" % str(loadingdetail_name2position(key))] = value
        positional_dict[loadingdetail_name2position(key)] = value
    return positional_dict

def loadingdetail_positional2named_dict(positional_dict):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[loadingdetail_position2name(key)] = value
    return named_dict