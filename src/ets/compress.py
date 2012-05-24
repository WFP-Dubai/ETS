### -*- coding: utf-8 -*- ####################################################

import base64, zlib

COMPRESS_MAPPING = (
    ('"_order":', '"_o":'),
    ('"receipt_signed_date":', '"r":'),
    ('"dispatch_date":', '"dd":'),
    ('"transport_dispach_signed_date":', '"td":'),
    ('"end_discharge_date":', '"e":'),
    ('"transport_driver_licence":', '"tdl":'),
    ('"container_two_remarks_reciept":', '"ctrr":'),
    ('"arrival_date":', '"ar":'),
    ('"container_two_number":', '"ctn":'),
    ('"destination":', '"d":'),
    ('"container_two_seal_number":', '"ctsn":'),
    ('"transport_trailer_registration":', '"ttr":'),
    ('"dispatcher_person":', '"dp":'),
    ('"receipt_person":', '"rp":'),
    ('"distance":', '"di":'),
    ('"date_removed":', '"dr":'),
    ('"receipt_validated":', '"rv":'),
    ('"loading_date":', '"ld":'),
    ('"receipt_sent_compas":', '"rsc":'),
    ('"sent_compas":', '"sc":'),
    ('"dispatch_remarks":', '"dr1":'),
    ('"container_one_seal_number":', '"cosn":'),
    ('"container_one_remarks_reciept":', '"corr":'),
    ('"receipt_remarks":', '"rr":'),
    ('"transport_sub_contractor":', '"tsc":'),
    ('"container_two_remarks_dispatch":', '"ctrd":'),
    ('"date_modified":', '"dm":'),
    ('"transport_vehicle_registration":', '"tvr":'),
    ('"start_discharge_date":', '"sdd":'),
    ('"transaction_type":', '"tt":'),
    ('"container_one_remarks_dispatch":', '"cord":'),
    ('"transport_type":', '"tt2":'),
    ('"container_one_number":', '"con":'),
    ('"date_created":', '"dc":'),
    ('"order":', '"o":'),
    ('"stock_item":', '"si":'),
    ('"waybill":', '"w":'),
    ('"number_units_damaged":', '"nud":'),
    ('"number_units_lost":', '"nul":'),
    ('"over_offload_units":', '"oou":'),
    ('"units_damaged_reason":', '"udr1":'),
    ('"overloaded_units":', '"ou1":'),
    ('"units_lost_reason":', '"ulr":'),
    ('"number_of_units":', '"nou2":'),
    ('"number_units_good":', '"noug":'),
    ('"transport_driver_name":', '"tdn1":'),
    ('"validated":', '"v":'),
    ('"title":', '"t":'),
    ('"compas":', '"c":'),
    ('"code":', '"co":'),
    ('"location":', '"lo":'),
    ('"groups":', '"gr":'),
    ('"user_permissions":', '"up":'),
    ('"organization":', '"or":'),
    ('"start_date":', '"sd":'),
    ('"end_date":', '"ed":'),
    ('"transport_name":', '"tn":'),
    ('"consignee":', '"con1":'),
    ('"transport_ouc":', '"to":'),
    ('"project_number":', '"pn":'),
    ('"origin_type":', '"ot":'),
    ('"transport_code":', '"tc":'),
    ('"warehouse":', '"wh":'),
    ('"country":', '"cr":'),
    ('"read_only":', '"ro":'),
    ('"db_engine":', '"de":'),
    ('"db_user":', '"du":'),
    ('"db_password":', '"dpa":'),
    ('"officers":', '"of":'),
    ('"db_port":', '"dbp":'),
    ('"db_name":', '"dn":'),
    ('"db_host":', '"dh":'),
    ('"updated":', '"u":'),
    ('"created":', '"cd":'),
    ('"expiry":', '"ex":'),
    ('"name":', '"n":'),
    ('"category":', '"ca":'),
    ('"unit_weight_gross":', '"uwg":'),
    ('"origin_id":', '"oi":'),
    ('"is_bulk":', '"ib":'),
    ('"allocation_code":', '"ac":'),
    ('"quality_description":', '"qd":'),
    ('"package":', '"p":'),
    ('"commodity":', '"cy":'),
    ('"unit_weight_net":', '"uwn":'),
    ('"si_code":', '"sic":'),
    ('"quality":', '"qc":'),
    ('"si_record_id":', '"sri":'),
    ('"fields":', '"f":'),
    ('"model":', '"m":'),
)

def compress_json(data):
    """Replaces all long field names with short ones, than compresses it with zlib and base64"""
    for full_field, cut_field in COMPRESS_MAPPING:
        data = data.replace(full_field, cut_field)

    return base64.b64encode( zlib.compress( data ) )


def decompress_json(data):
    """Replaces all short abbreviations with real field names"""
    
    try:
        data = zlib.decompress( base64.b64decode( data ) )
    except (zlib.error, TypeError):
        return
    else:
        #Extend field names
        for full_field, cut_field in COMPRESS_MAPPING:
            data = data.replace(cut_field, full_field)

    return data 
