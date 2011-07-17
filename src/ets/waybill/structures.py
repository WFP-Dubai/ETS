'''
Created on 13/gen/2010

@author: serafino
'''

# -*- coding: utf-8 -*-

class WaybillFieldsMap:

    NAME_2_POSITION = {
        'ltiNumber': 0,
        'waybillNumber': 1,
        'dateOfLoading': 2,
        'dateOfDispatch': 3,
        'transactionType': 4,
        'transportType': 5,
        'dispatchRemarks': 6,
        'dispatcherName': 7,
        'dispatcherTitle': 8,
        'dispatcherSigned': 9,
        'transportContractor': 10,
        'transportSubContractor': 11,
        'transportDriverName': 12,
        'transportDriverLicenceID': 13,
        'transportVehicleRegistration': 14,
        'transportTrailerRegistration': 15,
        'transportDispachSigned': 16,
        'transportDispachSignedTimestamp': 17,
        'transportDeliverySigned': 18,
        'transportDeliverySignedTimestamp': 19,
        'containerOneNumber': 20,
        'containerTwoNumber': 21,
        'containerOneSealNumber': 22,
        'containerTwoSealNumber': 23,
        'containerOneRemarksDispatch': 24,
        'containerTwoRemarksDispatch': 25,
        'containerOneRemarksReciept': 26,
        'containerTwoRemarksReciept': 27,
        'recipientLocation': 28,
        'recipientConsingee': 29,
        'recipientName': 30,
        'recipientTitle': 31,
        'recipientArrivalDate': 32,
        'recipientStartDischargeDate': 33,
        'recipientEndDischargeDate': 34,
        'recipientDistance': 35,
        'recipientRemarks': 36,
        'recipientSigned': 37,
        'recipientSignedTimestamp': 38,
        'destinationWarehouse': 39,
        'waybillValidated': 40,
        'waybillReceiptValidated': 41,
        'waybillSentToCompas': 42,
        'waybillRecSentToCompas': 43,
        'waybillProcessedForPayment': 44,
        'invalidated': 45,
        'auditComment': 46,
    }

    POSITION_2_NAME = {
        '0': 'ltiNumber',
        '1': 'waybillNumber',
        '2': 'dateOfLoading',
        '3': 'dateOfDispatch',
        '4': 'transactionType',
        '5': 'transportType',
        '6': 'dispatchRemarks',
        '7': 'dispatcherName',
        '8': 'dispatcherTitle',
        '9': 'dispatcherSigned',
        '10': 'transportContractor',
        '11': 'transportSubContractor',
        '12': 'transportDriverName',
        '13': 'transportDriverLicenceID',
        '14': 'transportVehicleRegistration',
        '15': 'transportTrailerRegistration',
        '16': 'transportDispachSigned',
        '17': 'transportDispachSignedTimestamp',
        '18': 'transportDeliverySigned',
        '19': 'transportDeliverySignedTimestamp',
        '20': 'containerOneNumber',
        '21': 'containerTwoNumber',
        '22': 'containerOneSealNumber',
        '23': 'containerTwoSealNumber',
        '24': 'containerOneRemarksDispatch',
        '25': 'containerTwoRemarksDispatch',
        '26': 'containerOneRemarksReciept',
        '27': 'containerTwoRemarksReciept',
        '28': 'recipientLocation',
        '29': 'recipientConsingee',
        '30': 'recipientName',
        '31': 'recipientTitle',
        '32': 'recipientArrivalDate',
        '33': 'recipientStartDischargeDate',
        '34': 'recipientEndDischargeDate',
        '35': 'recipientDistance',
        '36': 'recipientRemarks',
        '37': 'recipientSigned',
        '38': 'recipientSignedTimestamp',
        '39': 'destinationWarehouse',
        '40': 'waybillValidated',
        '41': 'waybillReceiptValidated',
        '42': 'waybillSentToCompas',
        '43': 'waybillRecSentToCompas',
        '44': 'waybillProcessedForPayment',
        '45': 'invalidated',
        '46': 'auditComment',
    }


def waybill_name2position( name ):
    return WaybillFieldsMap.NAME_2_POSITION[name]


def waybill_position2name( position ):
    return WaybillFieldsMap.POSITION_2_NAME[position]


def waybill_named2positional_dict( name_dict ):
    positional_dict = {}
    for key, value in name_dict.items():
        #positional_dict["W%s" % str(waybill_name2position(key))] = value
        positional_dict[waybill_name2position( key )] = value
    return positional_dict


def waybill_positional2named_dict( positional_dict ):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[waybill_position2name( key )] = value
    return named_dict


class LoadingDetailFieldsMap():

    NAME_2_POSITION = {
        'wbNumber': 0,
        'siNo': 1,
        'numberUnitsLoaded': 2,
        'numberUnitsGood': 3,
        'numberUnitsLost': 4,
        'numberUnitsDamaged': 5,
        'unitsLostReason': 6,
        'unitsDamagedReason': 7,
        'unitsDamagedType': 8,
        'unitsLostType': 9,
        'overloadedUnits': 10,
        'loadingDetailSentToCompas': 11,
        'overOffloadUnits': 12,
    }

    POSITION_2_NAME = {
        '0': 'wbNumber',
        '1': 'siNo',
        '2': 'numberUnitsLoaded',
        '3': 'numberUnitsGood',
        '4': 'numberUnitsLost',
        '5': 'numberUnitsDamaged',
        '6': 'unitsLostReason',
        '7': 'unitsDamagedReason',
        '8': 'unitsDamagedType',
        '9': 'unitsLostType',
        '10': 'overloadedUnits',
        '11': 'loadingDetailSentToCompas',
        '12': 'overOffloadUnits',
    }


def loadingdetail_name2position( name ):
    return LoadingDetailFieldsMap.NAME_2_POSITION[name]


def loadingdetail_position2name( position ):
    return LoadingDetailFieldsMap.POSITION_2_NAME[position]


def loadingdetail_named2positional_dict( name_dict ):
    positional_dict = {}
    for key, value in name_dict.items():
        #positional_dict["L%s" % str(loadingdetail_name2position(key))] = value
        positional_dict[loadingdetail_name2position( key )] = value
    return positional_dict


def loadingdetail_positional2named_dict( positional_dict ):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[loadingdetail_position2name( key )] = value
    return named_dict


class LtiOriginalFieldsMap():

    NAME_2_POSITION = {
        'lti_pk': 0,
        'lti_id': 1,
        'code': 2,
        'lti_date': 3,
        'expiry_date': 4,
        'transport_code': 5,
        'transport_ouc': 6,
        'transport_name': 7,
        'origin_type': 8,
        'origintype_desc': 9,
        'origin_location_code': 10,
        'origin_loc_name': 11,
        'origin_wh_code': 12,
        'origin_wh_name': 13,
        'destination_location_code': 14,
        'destination_loc_name': 15,
        'consegnee_code': 16,
        'consegnee_name': 17,
        'requested_dispatch_date': 18,
        'project_wbs_element': 19,
        'si_record_id': 20,
        'si_code': 21,
        'comm_category_code': 22,
        'commodity_code': 23,
        'cmmname': 24,
        'quantity_net': 25,
        'quantity_gross': 26,
        'number_of_units': 27,
        'unit_weight_net': 28,
        'unit_weight_gross': 29,
    }

    POSITION_2_NAME = {
        '0': 'lti_pk',
        '1': 'lti_id',
        '2': 'code',
        '3': 'lti_date',
        '4': 'expiry_date',
        '5': 'transport_code',
        '6': 'transport_ouc',
        '7': 'transport_name',
        '8': 'origin_type',
        '9': 'origintype_desc',
        '10': 'origin_location_code',
        '11': 'origin_loc_name',
        '12': 'origin_wh_code',
        '13': 'origin_wh_name',
        '14': 'destination_location_code',
        '15': 'destination_loc_name',
        '16': 'consegnee_code',
        '17': 'consegnee_name',
        '18': 'requested_dispatch_date',
        '19': 'project_wbs_element',
        '20': 'si_record_id',
        '21': 'si_code',
        '22': 'comm_category_code',
        '23': 'commodity_code',
        '24': 'cmmname',
        '25': 'quantity_net',
        '26': 'quantity_gross',
        '27': 'number_of_units',
        '28': 'unit_weight_net',
        '29': 'unit_weight_gross',
    }


def lti_name2position( name ):
    return LtiOriginalFieldsMap.NAME_2_POSITION[name]


def lti_position2name( position ):
    return LtiOriginalFieldsMap.POSITION_2_NAME[position]


def lti_named2positional_dict( name_dict ):
    positional_dict = {}
    for key, value in name_dict.items():
        positional_dict[lti_name2position( key )] = value
    return positional_dict


def lti_positional2named_dict( positional_dict ):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[lti_position2name( key )] = value
    return named_dict


class EpicStocklFieldsMap():

    NAME_2_POSITION = {
        'wh_pk': 0,
        'wh_regional': 1,
        'wh_country': 2,
        'wh_location': 3,
        'wh_code': 4,
        'wh_name': 5,
        'project_wbs_element': 6,
        'si_record_id': 7,
        'si_code': 8,
        'origin_id': 9,
        'comm_category_code': 10,
        'commodity_code': 11,
        'cmmname': 12,
        'package_code': 13,
        'packagename': 14,
        'qualitycode': 15,
        'qualitydescr': 16,
        'quantity_net': 17,
        'quantity_gross': 18,
        'number_of_units': 19,
        'allocation_code': 20,
        'reference_number': 21,
    }

    POSITION_2_NAME = {
        '0': 'wh_pk',
        '1': 'wh_regional',
        '2': 'wh_country',
        '3': 'wh_location',
        '4': 'wh_code',
        '5': 'wh_name',
        '6': 'project_wbs_element',
        '7': 'si_record_id',
        '8': 'si_code',
        '9': 'origin_id',
        '10': 'comm_category_code',
        '11': 'commodity_code',
        '12': 'cmmname',
        '13': 'package_code',
        '14': 'packagename',
        '15': 'qualitycode',
        '16': 'qualitydescr',
        '17': 'quantity_net',
        '18': 'quantity_gross',
        '19': 'number_of_units',
        '20': 'allocation_code',
        '21': 'reference_number',
    }


def stock_name2position( name ):
    return EpicStocklFieldsMap.NAME_2_POSITION[name]


def stock_position2name( position ):
    return EpicStocklFieldsMap.POSITION_2_NAME[position]


def stock_named2positional_dict( name_dict ):
    positional_dict = {}
    for key, value in name_dict.items():
        positional_dict[stock_name2position( key )] = value
    return positional_dict


def stock_positional2named_dict( positional_dict ):
    named_dict = {}
    for key, value in positional_dict.items():
        named_dict[stock_position2name( key )] = value
    return named_dict
