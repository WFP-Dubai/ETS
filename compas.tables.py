# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class ActualBeneficiaries(models.Model):
    beneficiary_code = models.CharField(unique=True, max_length=2)
    beneficiary_descr = models.CharField(max_length=50)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'actual_beneficiaries'

class AllocAreas(models.Model):
    code = models.CharField(max_length=10, blank=True)
    type = models.CharField(max_length=1, blank=True)
    name = models.CharField(max_length=50, blank=True)
    sub_sector_nme = models.CharField(max_length=30, blank=True)
    sector_nme = models.CharField(max_length=30, blank=True)
    country_nme = models.CharField(max_length=50, blank=True)
    class Meta:
        db_table = u'alloc_areas'

class BaseLabels(models.Model):
    lbl_record_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    lbl_type = models.CharField(unique=True, max_length=3)
    lbl_text = models.CharField(unique=True, max_length=200)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'base_labels'

class CnfdspDetails(models.Model):
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_destination_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    quality_received = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'cnfdsp_details'

class CnfdspDetailsBck(models.Model):
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    org_unit_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_destination_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quality_received = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'cnfdsp_details_bck'

class CnfdspMasters(models.Model):
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    extra_code = models.CharField(max_length=25, blank=True)
    receipt_location_code = models.CharField(max_length=10)
    receipt_code = models.CharField(max_length=13)
    tran_type_code_rec = models.CharField(max_length=4)
    tran_type_descr_rec = models.CharField(max_length=50, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateField()
    end_discharge_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'cnfdsp_masters'

class CnfdspMastersBck(models.Model):
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    org_unit_code = models.CharField(max_length=13)
    extra_code = models.CharField(max_length=25, blank=True)
    receipt_location_code = models.CharField(max_length=10)
    receipt_code = models.CharField(max_length=13)
    tran_type_code_rec = models.CharField(max_length=4)
    tran_type_descr_rec = models.CharField(max_length=50, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateField()
    end_discharge_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'cnfdsp_masters_bck'

class CodeTables(models.Model):
    delete_ind = models.CharField(max_length=1, blank=True)
    table_type_cde = models.CharField(unique=True, max_length=3, blank=True)
    table_cde = models.CharField(unique=True, max_length=8, blank=True)
    table_cde_rdfn1 = models.CharField(max_length=8, blank=True)
    table_cde_len1 = models.CharField(max_length=1, blank=True)
    table_cde_fill7 = models.CharField(max_length=7, blank=True)
    table_cde_rdfn2 = models.CharField(max_length=8, blank=True)
    table_cde_len2 = models.CharField(max_length=2, blank=True)
    table_cde_fill6 = models.CharField(max_length=6, blank=True)
    table_cde_rdfn3 = models.CharField(max_length=8, blank=True)
    table_cde_len3 = models.CharField(max_length=3, blank=True)
    table_cde_fill5 = models.CharField(max_length=5, blank=True)
    table_cde_rdfn4 = models.CharField(max_length=8, blank=True)
    table_cde_len4 = models.CharField(max_length=4, blank=True)
    table_cde_fill4 = models.CharField(max_length=4, blank=True)
    table_cde_rdfn5 = models.CharField(max_length=8, blank=True)
    table_cde_len5 = models.CharField(max_length=5, blank=True)
    table_cde_fill3 = models.CharField(max_length=3, blank=True)
    table_cde_rdfn6 = models.CharField(max_length=8, blank=True)
    table_cde_len6 = models.CharField(max_length=6, blank=True)
    table_cde_fill2 = models.CharField(max_length=2, blank=True)
    table_cde_rdfn7 = models.CharField(max_length=8, blank=True)
    table_cde_len7 = models.CharField(max_length=7, blank=True)
    table_cde_fill1 = models.CharField(max_length=1, blank=True)
    field1_dsc = models.CharField(max_length=30, blank=True)
    field2_dsc = models.CharField(max_length=30, blank=True)
    field3_dsc = models.CharField(max_length=30, blank=True)
    field4_dsc = models.CharField(max_length=30, blank=True)
    field5_dsc = models.CharField(max_length=30, blank=True)
    field6_dsc = models.CharField(max_length=70, blank=True)
    field7_dsc = models.CharField(max_length=70, blank=True)
    field8_dsc = models.CharField(max_length=70, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'code_tables'

class CoiToSis(models.Model):
    si_record_id = models.CharField(unique=True, max_length=25)
    origin_id = models.CharField(max_length=23)
    percentage_n = models.DecimalField(max_digits=5, decimal_places=2)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'coi_to_sis'

class CommcifBasecost(models.Model):
    record_id = models.CharField(unique=True, max_length=25)
    origin_id = models.CharField(max_length=25, blank=True)
    declaration_number = models.IntegerField(null=True, blank=True)
    declared_mt = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    c_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    c_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    c_currency = models.CharField(max_length=3, blank=True)
    c_exchange_rate_date = models.DateField(null=True, blank=True)
    o_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    o_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    o_currency = models.CharField(max_length=3, blank=True)
    o_exchange_rate_date = models.DateField(null=True, blank=True)
    eo_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    eo_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    eo_currency = models.CharField(max_length=3, blank=True)
    eo_exchange_rate_date = models.DateField(null=True, blank=True)
    a_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    a_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    a_currency = models.CharField(max_length=3, blank=True)
    a_exchange_rate_date = models.DateField(null=True, blank=True)
    l_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    l_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    l_currency = models.CharField(max_length=3, blank=True)
    l_exchange_rate_date = models.DateField(null=True, blank=True)
    ot_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    ot_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    ot_currency = models.CharField(max_length=3, blank=True)
    ot_exchange_rate_date = models.DateField(null=True, blank=True)
    ad_rate = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    ad_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    ad_currency = models.CharField(max_length=3, blank=True)
    ad_exchange_rate_date = models.DateField(null=True, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'commcif_basecost'

class Commodities(models.Model):
    comm_category_code = models.CharField(unique=True, max_length=9)
    code = models.CharField(unique=True, max_length=18)
    description = models.CharField(max_length=100, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'commodities'

class CommodityOrigins(models.Model):
    origin_id = models.CharField(unique=True, max_length=23)
    origin_type = models.CharField(max_length=1)
    creation_date = models.DateField(unique=True)
    vessel_or_supplier = models.CharField(unique=True, max_length=50)
    reference_number = models.CharField(unique=True, max_length=8)
    geo_point_code = models.CharField(unique=True, max_length=10, blank=True)
    manual_indicator = models.CharField(max_length=1, blank=True)
    org_unit_code = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'commodity_origins'

class CommCategories(models.Model):
    code = models.CharField(unique=True, max_length=9)
    description = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'comm_categories'

class CommPacked(models.Model):
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    description = models.CharField(max_length=100, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'comm_packed'

class CompasJob(models.Model):
    job = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    last_date = models.DateField(null=True, blank=True)
    last_sec = models.CharField(max_length=8, blank=True)
    next_date = models.DateField(null=True, blank=True)
    next_sec = models.CharField(max_length=8, blank=True)
    total_time = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    broken = models.CharField(max_length=1, blank=True)
    failures = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'compas_job'

class CompasMessages(models.Model):
    message_type = models.CharField(unique=True, max_length=3)
    message_number = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    message_title = models.CharField(max_length=30, blank=True)
    message_text = models.CharField(max_length=80)
    message_hint = models.CharField(max_length=80, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'compas_messages'

class CompasUsers(models.Model):
    compas_user_id = models.CharField(unique=True, max_length=25)
    org_unit_code = models.CharField(unique=True, max_length=13)
    compas_username = models.CharField(unique=True, max_length=30)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'compas_users'

class Countries(models.Model):
    code = models.CharField(unique=True, max_length=3)
    un_classification = models.CharField(max_length=1)
    country_iso_3_code = models.CharField(max_length=3)
    country_iso_2_code = models.CharField(max_length=2, blank=True)
    validity_indicator = models.CharField(max_length=1, blank=True)
    official_name = models.CharField(max_length=100)
    short_name = models.CharField(unique=True, max_length=50)
    country_undp_code = models.CharField(max_length=3, blank=True)
    country_fao_code = models.CharField(max_length=3, blank=True)
    starting_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    country_wis_code = models.CharField(max_length=3, blank=True)
    donor_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'countries'

class Currencies(models.Model):
    code = models.CharField(unique=True, max_length=3)
    currency_validity_indicator = models.CharField(max_length=1)
    currency_official_name = models.CharField(max_length=50)
    currency_short_name = models.CharField(max_length=20)
    currency_plural = models.CharField(max_length=20, blank=True)
    currency_abbreviation = models.CharField(max_length=10, blank=True)
    currency_symbol = models.CharField(max_length=10, blank=True)
    curr_auth_cnt_code = models.CharField(max_length=3, blank=True)
    curr_auth_ter_code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'currencies'

class CustomizedFormItems(models.Model):
    record_id = models.CharField(unique=True, max_length=25)
    org_unit_code = models.CharField(unique=True, max_length=13)
    table_name = models.CharField(unique=True, max_length=30)
    item_label = models.CharField(unique=True, max_length=30)
    item_type = models.CharField(max_length=1)
    item_length = models.DecimalField(max_digits=127, decimal_places=127)
    item_default_value = models.CharField(max_length=2000, blank=True)
    item_ouc = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'customized_form_items'

class CustomizedPrivileges(models.Model):
    compas_user_id = models.CharField(unique=True, max_length=25)
    org_unit_code = models.CharField(unique=True, max_length=13)
    standard_role_code = models.CharField(unique=True, max_length=3)
    menu_record_id = models.CharField(unique=True, max_length=25)
    flag_create = models.CharField(max_length=1)
    flag_edit = models.CharField(max_length=1)
    flag_view = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'customized_privileges'

class CustomizedPrvData(models.Model):
    compas_user_id = models.CharField(unique=True, max_length=25)
    org_unit_code = models.CharField(unique=True, max_length=13)
    menu_record_id = models.CharField(unique=True, max_length=25)
    standard_role_code = models.CharField(unique=True, max_length=3)
    data_org_unit_code = models.CharField(unique=True, max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'customized_prv_data'

class CPrjTypes(models.Model):
    code = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    type = models.CharField(max_length=30, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'c_prj_types'

class DispatchDetails(models.Model):
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    si_record_id = models.CharField(max_length=25, blank=True)
    origin_id = models.CharField(unique=True, max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_destination_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'dispatch_details'

class DispatchFormItems(models.Model):
    item_record_id = models.CharField(unique=True, max_length=25)
    dispatch_code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    item_value = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'dispatch_form_items'

class DispatchMasters(models.Model):
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    dispatch_date = models.DateField()
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=13)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    destination_code = models.CharField(max_length=13, blank=True)
    pro_activity_code = models.CharField(max_length=6, blank=True)
    activity_ouc = models.CharField(max_length=13, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    loan_id = models.CharField(max_length=25, blank=True)
    loading_date = models.DateField()
    organization_id = models.CharField(max_length=12)
    tran_type_code = models.CharField(max_length=4)
    tran_type_descr = models.CharField(max_length=50, blank=True)
    modetrans_code = models.CharField(max_length=2)
    comments = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    certifing_title = models.CharField(max_length=50, blank=True)
    trans_contractor_code = models.CharField(max_length=4)
    supplier1_ouc = models.CharField(max_length=13)
    trans_subcontractor_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    nmbplt_id = models.CharField(max_length=25, blank=True)
    nmbtrl_id = models.CharField(max_length=25, blank=True)
    driver_name = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=20, blank=True)
    vehicle_registration = models.CharField(max_length=20, blank=True)
    trailer_plate = models.CharField(max_length=20, blank=True)
    container_number = models.CharField(max_length=15, blank=True)
    atl_li_code = models.CharField(max_length=8, blank=True)
    notify_indicator = models.CharField(max_length=1, blank=True)
    customised = models.CharField(max_length=50, blank=True)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    notify_org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'dispatch_masters'

class DistanceRates(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_warehouse_code = models.CharField(unique=True, max_length=13)
    destination_warehouse_code = models.CharField(unique=True, max_length=13)
    start_date = models.DateField(unique=True)
    end_date = models.DateField(unique=True, null=True, blank=True)
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=11, decimal_places=2)
    distance_travelling = models.DecimalField(max_digits=10, decimal_places=3)
    transport_rate_type = models.CharField(max_length=10)
    transport_type = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'distance_rates'

class DistanceRatesBck(models.Model):
    org_unit_code = models.CharField(max_length=13)
    origin_warehouse_code = models.CharField(max_length=13)
    destination_warehouse_code = models.CharField(max_length=13)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=11, decimal_places=2)
    distance_travelling = models.DecimalField(max_digits=10, decimal_places=3)
    transport_rate_type = models.CharField(max_length=10)
    transport_type = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'distance_rates_bck'

class DistributionDetails(models.Model):
    dst_record_id = models.CharField(unique=True, max_length=25)
    dst_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    si_record_id = models.CharField(max_length=25, blank=True)
    wbs_element = models.CharField(max_length=25, blank=True)
    activity_code = models.CharField(max_length=6, blank=True)
    activity_org_unit_code = models.CharField(max_length=13, blank=True)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    opening_net = models.DecimalField(max_digits=11, decimal_places=3)
    received_net = models.DecimalField(max_digits=11, decimal_places=3)
    distribution_net = models.DecimalField(max_digits=11, decimal_places=3)
    food_returns_net = models.DecimalField(max_digits=11, decimal_places=3)
    lost_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'distribution_details'

class DistributionMasters(models.Model):
    dst_record_id = models.CharField(unique=True, max_length=25)
    organization_id = models.CharField(unique=True, max_length=12)
    level_id = models.CharField(max_length=10)
    country_code = models.CharField(unique=True, max_length=3, blank=True)
    sector_country_code = models.CharField(max_length=3, blank=True)
    sector_code = models.CharField(unique=True, max_length=3, blank=True)
    sub_sector_country_code = models.CharField(max_length=3, blank=True)
    sub_sector_sector_code = models.CharField(max_length=3, blank=True)
    sub_sector_code = models.CharField(unique=True, max_length=3, blank=True)
    location_country_code = models.CharField(max_length=3, blank=True)
    location_sector_code = models.CharField(max_length=3, blank=True)
    location_sub_sector_code = models.CharField(max_length=3, blank=True)
    location_code = models.CharField(unique=True, max_length=10, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    period_from = models.DateField(unique=True, null=True, blank=True)
    period_to = models.DateField(unique=True, null=True, blank=True)
    lou_code = models.CharField(max_length=15, blank=True)
    comments = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'distribution_masters'

class DocumentTypes(models.Model):
    code = models.CharField(unique=True, max_length=2)
    descr = models.CharField(max_length=20)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'document_types'

class Donors(models.Model):
    code = models.CharField(max_length=12, blank=True)
    name = models.CharField(max_length=80, blank=True)
    class Meta:
        db_table = u'donors'

class DspcstTrntypes(models.Model):
    record_id = models.CharField(unique=True, max_length=25)
    consignee_wfp = models.CharField(max_length=1, blank=True)
    origin_type = models.CharField(max_length=1, blank=True)
    stock_maintained = models.CharField(max_length=1, blank=True)
    tran_type_code = models.CharField(max_length=4, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'dspcst_trntypes'

class DstActualBeneficiaries(models.Model):
    dst_record_id = models.CharField(unique=True, max_length=25)
    beneficiary_code = models.CharField(unique=True, max_length=2)
    beneficiary_number = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'dst_actual_beneficiaries'

class Ekko(models.Model):
    mandt = models.CharField(max_length=3)
    ebeln = models.CharField(max_length=10)
    bukrs = models.CharField(max_length=4)
    bstyp = models.CharField(max_length=1)
    bsart = models.CharField(max_length=4)
    bsakz = models.CharField(max_length=1)
    loekz = models.CharField(max_length=1)
    statu = models.CharField(max_length=1)
    aedat = models.CharField(max_length=8)
    ernam = models.CharField(max_length=12)
    pincr = models.CharField(max_length=5)
    lponr = models.CharField(max_length=5)
    lifnr = models.CharField(max_length=10)
    spras = models.CharField(max_length=1)
    zterm = models.CharField(max_length=4)
    zbd1t = models.IntegerField()
    zbd2t = models.IntegerField()
    zbd3t = models.IntegerField()
    zbd1p = models.DecimalField(max_digits=5, decimal_places=3)
    zbd2p = models.DecimalField(max_digits=5, decimal_places=3)
    ekorg = models.CharField(max_length=4)
    ekgrp = models.CharField(max_length=3)
    waers = models.CharField(max_length=5)
    wkurs = models.DecimalField(max_digits=9, decimal_places=5)
    kufix = models.CharField(max_length=1)
    bedat = models.CharField(max_length=8)
    kdatb = models.CharField(max_length=8)
    kdate = models.CharField(max_length=8)
    bwbdt = models.CharField(max_length=8)
    angdt = models.CharField(max_length=8)
    bnddt = models.CharField(max_length=8)
    gwldt = models.CharField(max_length=8)
    ausnr = models.CharField(max_length=10)
    angnr = models.CharField(max_length=10)
    ihran = models.CharField(max_length=8)
    ihrez = models.CharField(max_length=12)
    verkf = models.CharField(max_length=30)
    telf1 = models.CharField(max_length=16)
    llief = models.CharField(max_length=10)
    kunnr = models.CharField(max_length=10)
    konnr = models.CharField(max_length=10)
    abgru = models.CharField(max_length=2)
    autlf = models.CharField(max_length=1)
    weakt = models.CharField(max_length=1)
    reswk = models.CharField(max_length=4)
    lblif = models.CharField(max_length=10)
    inco1 = models.CharField(max_length=3)
    inco2 = models.CharField(max_length=28)
    ktwrt = models.DecimalField(max_digits=15, decimal_places=2)
    submi = models.CharField(max_length=10)
    knumv = models.CharField(max_length=10)
    kalsm = models.CharField(max_length=6)
    stafo = models.CharField(max_length=6)
    lifre = models.CharField(max_length=10)
    exnum = models.CharField(max_length=10)
    unsez = models.CharField(max_length=12)
    logsy = models.CharField(max_length=10)
    upinc = models.CharField(max_length=5)
    stako = models.CharField(max_length=1)
    frggr = models.CharField(max_length=2)
    frgsx = models.CharField(max_length=2)
    frgke = models.CharField(max_length=1)
    frgzu = models.CharField(max_length=8)
    frgrl = models.CharField(max_length=1)
    lands = models.CharField(max_length=3)
    lphis = models.CharField(max_length=1)
    adrnr = models.CharField(max_length=10)
    stceg_l = models.CharField(max_length=3)
    stceg = models.CharField(max_length=20)
    absgr = models.CharField(max_length=2)
    addnr = models.CharField(max_length=10)
    kornr = models.CharField(max_length=1)
    class Meta:
        db_table = u'ekko'

class Eul4AccessPrivs(models.Model):
    ap_id = models.IntegerField(unique=True)
    ap_type = models.CharField(max_length=10)
    ap_eu_id = models.IntegerField(unique=True)
    ap_priv_level = models.IntegerField()
    gp_app_id = models.IntegerField(null=True, blank=True)
    gba_ba_id = models.IntegerField(null=True, blank=True)
    gd_doc_id = models.IntegerField(null=True, blank=True)
    ap_element_state = models.IntegerField()
    ap_created_by = models.CharField(max_length=64)
    ap_created_date = models.DateField()
    ap_updated_by = models.CharField(max_length=64, blank=True)
    ap_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_access_privs'

class Eul4AppParams(models.Model):
    app_id = models.IntegerField(unique=True)
    app_type = models.CharField(max_length=10)
    app_name_mn = models.IntegerField(unique=True)
    app_description_mn = models.IntegerField()
    sp_default_value = models.CharField(max_length=240, blank=True)
    sp_value = models.CharField(max_length=240, blank=True)
    app_element_state = models.IntegerField()
    app_created_by = models.CharField(max_length=64)
    app_created_date = models.DateField()
    app_updated_by = models.CharField(max_length=64, blank=True)
    app_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_app_params'

class Eul4AsmpCons(models.Model):
    apc_id = models.IntegerField(unique=True)
    apc_type = models.CharField(max_length=10)
    apc_cons_type = models.IntegerField()
    apc_asmp_id = models.IntegerField(unique=True)
    aoc_obj_id = models.IntegerField(unique=True, null=True, blank=True)
    asoc_sumo_id = models.IntegerField(null=True, blank=True)
    auc_eu_id = models.IntegerField(null=True, blank=True)
    apc_element_state = models.IntegerField()
    apc_created_by = models.CharField(max_length=64)
    apc_created_date = models.DateField()
    apc_updated_by = models.CharField(max_length=64, blank=True)
    apc_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_asmp_cons'

class Eul4AsmpLogs(models.Model):
    apl_id = models.IntegerField(unique=True)
    apl_timestamp = models.DateField()
    apl_event_type = models.IntegerField()
    apl_asmp_id = models.IntegerField()
    apl_sumo_id = models.IntegerField(null=True, blank=True)
    apl_element_state = models.IntegerField()
    apl_created_by = models.CharField(max_length=64)
    apl_created_date = models.DateField()
    apl_updated_by = models.CharField(max_length=64, blank=True)
    apl_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_asmp_logs'

class Eul4AsmPolicies(models.Model):
    asmp_id = models.IntegerField(unique=True)
    asmp_name = models.CharField(unique=True, max_length=100)
    asmp_developer_key = models.CharField(unique=True, max_length=100)
    asmp_description = models.CharField(max_length=240, blank=True)
    asmp_user_prop1 = models.CharField(max_length=100, blank=True)
    asmp_user_prop2 = models.CharField(max_length=100, blank=True)
    asmp_element_state = models.IntegerField()
    asmp_created_by = models.CharField(max_length=64)
    asmp_created_date = models.DateField()
    asmp_updated_by = models.CharField(max_length=64, blank=True)
    asmp_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_asm_policies'

class Eul4Bas(models.Model):
    ba_id = models.IntegerField(unique=True)
    ba_name = models.CharField(unique=True, max_length=100)
    ba_developer_key = models.CharField(unique=True, max_length=100)
    ba_description = models.CharField(max_length=240, blank=True)
    ba_ext_name = models.CharField(max_length=64, blank=True)
    ba_user_prop1 = models.CharField(max_length=100, blank=True)
    ba_user_prop2 = models.CharField(max_length=100, blank=True)
    ba_element_state = models.IntegerField()
    ba_created_by = models.CharField(max_length=64)
    ba_created_date = models.DateField()
    ba_updated_by = models.CharField(max_length=64, blank=True)
    ba_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_bas'

class Eul4BatchParams(models.Model):
    bp_id = models.IntegerField(unique=True)
    bp_name = models.CharField(unique=True, max_length=100)
    bp_value1 = models.CharField(max_length=250)
    bp_value2 = models.CharField(max_length=250, blank=True)
    bp_value3 = models.CharField(max_length=250, blank=True)
    bp_value4 = models.CharField(max_length=250, blank=True)
    bp_value5 = models.CharField(max_length=250, blank=True)
    bp_value6 = models.CharField(max_length=250, blank=True)
    bp_bs_id = models.IntegerField(unique=True)
    bp_element_state = models.IntegerField()
    bp_created_by = models.CharField(max_length=64)
    bp_created_date = models.DateField()
    bp_updated_by = models.CharField(max_length=64, blank=True)
    bp_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_batch_params'

class Eul4BatchQueries(models.Model):
    bq_id = models.IntegerField(unique=True)
    bq_bs_id = models.IntegerField(unique=True)
    bq_query_id = models.CharField(unique=True, max_length=240)
    bq_result_sql_1 = models.CharField(max_length=250, blank=True)
    bq_result_sql_2 = models.CharField(max_length=250, blank=True)
    bq_result_sql_3 = models.CharField(max_length=250, blank=True)
    bq_result_sql_4 = models.CharField(max_length=250, blank=True)
    bq_element_state = models.IntegerField()
    bq_created_by = models.CharField(max_length=64)
    bq_created_date = models.DateField()
    bq_updated_by = models.CharField(max_length=64, blank=True)
    bq_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_batch_queries'

class Eul4BatchReports(models.Model):
    br_id = models.IntegerField(unique=True)
    br_name = models.CharField(unique=True, max_length=100)
    br_workbook_name = models.CharField(max_length=240)
    br_description = models.CharField(max_length=240, blank=True)
    br_next_run_date = models.DateField(null=True, blank=True)
    br_job_id = models.BigIntegerField(unique=True, null=True, blank=True)
    br_expiry = models.BigIntegerField(null=True, blank=True)
    br_completion_date = models.DateField(null=True, blank=True)
    br_num_freq_units = models.BigIntegerField(null=True, blank=True)
    br_eu_id = models.IntegerField()
    br_rfu_id = models.IntegerField()
    br_auto_refresh = models.IntegerField()
    br_report_schema = models.CharField(max_length=64)
    br_element_state = models.IntegerField()
    br_created_by = models.CharField(max_length=64)
    br_created_date = models.DateField()
    br_updated_by = models.CharField(max_length=64, blank=True)
    br_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_batch_reports'

class Eul4BatchSheets(models.Model):
    bs_id = models.IntegerField(unique=True)
    bs_br_id = models.IntegerField(unique=True)
    bs_sheet_name = models.CharField(max_length=240)
    bs_sheet_id = models.CharField(unique=True, max_length=240)
    bs_element_state = models.IntegerField()
    bs_created_by = models.CharField(max_length=64)
    bs_created_date = models.DateField()
    bs_updated_by = models.CharField(max_length=64, blank=True)
    bs_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_batch_sheets'

class Eul4BaObjLinks(models.Model):
    bol_id = models.IntegerField(unique=True)
    bol_ba_id = models.IntegerField(unique=True)
    bol_obj_id = models.IntegerField(unique=True)
    bol_sequence = models.BigIntegerField(null=True, blank=True)
    bol_element_state = models.IntegerField()
    bol_created_by = models.CharField(max_length=64)
    bol_created_date = models.DateField()
    bol_updated_by = models.CharField(max_length=64, blank=True)
    bol_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_ba_obj_links'

class Eul4BqDeps(models.Model):
    bqd_id = models.IntegerField(unique=True)
    bqd_type = models.CharField(unique=True, max_length=10)
    bqd_bq_id = models.IntegerField(unique=True)
    bfild_fil_id = models.IntegerField(unique=True, null=True, blank=True)
    bid_it_id = models.IntegerField(null=True, blank=True)
    bfund_fun_id = models.IntegerField(null=True, blank=True)
    bqd_element_state = models.IntegerField()
    bqd_created_by = models.CharField(max_length=64)
    bqd_created_date = models.DateField()
    bqd_updated_by = models.CharField(max_length=64, blank=True)
    bqd_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_bq_deps'

class Eul4BqTables(models.Model):
    bqt_id = models.IntegerField(unique=True)
    bqt_bq_id = models.IntegerField(unique=True)
    bqt_brr_id = models.IntegerField(unique=True)
    bqt_table_name = models.CharField(unique=True, max_length=64)
    bqt_element_state = models.IntegerField()
    bqt_created_by = models.CharField(max_length=64)
    bqt_created_date = models.DateField()
    bqt_updated_by = models.CharField(max_length=64, blank=True)
    bqt_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_bq_tables'

class Eul4BrRuns(models.Model):
    brr_id = models.IntegerField(unique=True)
    brr_br_id = models.IntegerField(unique=True)
    brr_run_number = models.BigIntegerField(unique=True)
    brr_state = models.IntegerField()
    brr_run_date = models.DateField(null=True, blank=True)
    brr_svr_err_code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    brr_svr_err_text = models.CharField(max_length=240, blank=True)
    brr_act_elap_time = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    brr_element_state = models.IntegerField()
    brr_created_by = models.CharField(max_length=64)
    brr_created_date = models.DateField()
    brr_updated_by = models.CharField(max_length=64, blank=True)
    brr_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_br_runs'

class Eul4DbhNodes(models.Model):
    dhn_id = models.IntegerField(unique=True)
    dhn_name = models.CharField(unique=True, max_length=100)
    dhn_developer_key = models.CharField(unique=True, max_length=100)
    dhn_description = models.CharField(max_length=240, blank=True)
    dhn_data_fmt_msk = models.CharField(max_length=100)
    dhn_disp_fmt_msk = models.CharField(max_length=100)
    dhn_hi_id = models.IntegerField(unique=True)
    dhn_user_prop2 = models.CharField(max_length=100, blank=True)
    dhn_user_prop1 = models.CharField(max_length=100, blank=True)
    dhn_element_state = models.IntegerField()
    dhn_created_by = models.CharField(max_length=64)
    dhn_created_date = models.DateField()
    dhn_updated_by = models.CharField(max_length=64, blank=True)
    dhn_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_dbh_nodes'

class Eul4Documents(models.Model):
    doc_id = models.IntegerField(unique=True)
    doc_name = models.CharField(unique=True, max_length=100)
    doc_developer_key = models.CharField(unique=True, max_length=100)
    doc_description = models.CharField(max_length=240, blank=True)
    doc_eu_id = models.IntegerField(unique=True)
    doc_length = models.BigIntegerField()
    doc_batch = models.IntegerField(unique=True)
    doc_content_type = models.CharField(max_length=100)
    doc_document = models.TextField(blank=True) # This field type is a guess.
    doc_user_prop2 = models.CharField(max_length=100, blank=True)
    doc_user_prop1 = models.CharField(max_length=100, blank=True)
    doc_element_state = models.IntegerField()
    doc_created_by = models.CharField(max_length=64)
    doc_created_date = models.DateField()
    doc_updated_by = models.CharField(max_length=64, blank=True)
    doc_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_documents'

class Eul4Domains(models.Model):
    dom_id = models.IntegerField(unique=True)
    dom_name = models.CharField(unique=True, max_length=100)
    dom_developer_key = models.CharField(unique=True, max_length=100)
    dom_description = models.CharField(max_length=240, blank=True)
    dom_data_type = models.IntegerField()
    dom_logical_item = models.IntegerField()
    dom_sys_generated = models.IntegerField()
    dom_cardinality = models.BigIntegerField(null=True, blank=True)
    dom_last_exec_time = models.BigIntegerField(null=True, blank=True)
    dom_cached = models.IntegerField()
    dom_it_id_lov = models.IntegerField(null=True, blank=True)
    dom_it_id_rank = models.IntegerField(null=True, blank=True)
    dom_user_prop2 = models.CharField(max_length=100, blank=True)
    dom_user_prop1 = models.CharField(max_length=100, blank=True)
    dom_element_state = models.IntegerField()
    dom_created_by = models.CharField(max_length=64)
    dom_created_date = models.DateField()
    dom_updated_by = models.CharField(max_length=64, blank=True)
    dom_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_domains'

class Eul4ElemXrefs(models.Model):
    ex_id = models.IntegerField(unique=True)
    ex_type = models.IntegerField()
    ex_ref1 = models.CharField(max_length=100)
    ex_el_type = models.CharField(max_length=10)
    ex_el_id = models.IntegerField()
    ex_ref2 = models.CharField(max_length=100, blank=True)
    class Meta:
        db_table = u'eul4_elem_xrefs'

class Eul4EulUsers(models.Model):
    eu_id = models.IntegerField(unique=True)
    eu_username = models.CharField(unique=True, max_length=64)
    eu_security_model = models.IntegerField()
    eu_use_pub_privs = models.IntegerField()
    eu_query_time_lmt = models.BigIntegerField(null=True, blank=True)
    eu_query_est_lmt = models.BigIntegerField(null=True, blank=True)
    eu_row_fetch_lmt = models.BigIntegerField(null=True, blank=True)
    eu_role_flag = models.IntegerField()
    eu_batch_jobs_lmt = models.BigIntegerField(null=True, blank=True)
    eu_batch_wnd_start = models.DateField(null=True, blank=True)
    eu_batch_wnd_end = models.DateField(null=True, blank=True)
    eu_batch_qtime_lmt = models.BigIntegerField(null=True, blank=True)
    eu_batch_expiry = models.BigIntegerField(null=True, blank=True)
    eu_batch_cmt_sz = models.BigIntegerField(null=True, blank=True)
    eu_batch_rep_user = models.CharField(max_length=64, blank=True)
    eu_element_state = models.IntegerField()
    eu_created_by = models.CharField(max_length=64)
    eu_created_date = models.DateField()
    eu_updated_by = models.CharField(max_length=64, blank=True)
    eu_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_eul_users'

class Eul4Expressions(models.Model):
    exp_id = models.IntegerField(unique=True)
    exp_type = models.CharField(max_length=10)
    exp_name = models.CharField(unique=True, max_length=100)
    exp_developer_key = models.CharField(unique=True, max_length=100)
    exp_description = models.CharField(max_length=240, blank=True)
    exp_formula1 = models.CharField(max_length=250, blank=True)
    exp_data_type = models.IntegerField()
    exp_sequence = models.BigIntegerField(null=True, blank=True)
    it_dom_id = models.IntegerField(null=True, blank=True)
    it_obj_id = models.IntegerField(null=True, blank=True)
    it_doc_id = models.IntegerField(unique=True, null=True, blank=True)
    it_format_mask = models.CharField(max_length=100, blank=True)
    it_max_data_width = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    it_max_disp_width = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    it_alignment = models.IntegerField(null=True, blank=True)
    it_word_wrap = models.IntegerField(null=True, blank=True)
    it_disp_null_val = models.CharField(max_length=100, blank=True)
    it_fun_id = models.IntegerField(null=True, blank=True)
    it_heading = models.CharField(max_length=240, blank=True)
    it_hidden = models.IntegerField(null=True, blank=True)
    it_placement = models.IntegerField(null=True, blank=True)
    it_user_def_fmt = models.CharField(max_length=100, blank=True)
    it_case_storage = models.IntegerField(null=True, blank=True)
    it_case_display = models.IntegerField(null=True, blank=True)
    it_ext_column = models.CharField(max_length=64, blank=True)
    ci_it_id = models.IntegerField(null=True, blank=True)
    ci_runtime_item = models.IntegerField(null=True, blank=True)
    par_multiple_vals = models.IntegerField(null=True, blank=True)
    co_nullable = models.IntegerField(null=True, blank=True)
    p_case_sensitive = models.IntegerField(null=True, blank=True)
    jp_key_id = models.IntegerField(null=True, blank=True)
    fil_obj_id = models.IntegerField(unique=True, null=True, blank=True)
    fil_doc_id = models.IntegerField(null=True, blank=True)
    fil_runtime_filter = models.IntegerField(null=True, blank=True)
    fil_app_type = models.IntegerField(null=True, blank=True)
    fil_ext_filter = models.CharField(max_length=64, blank=True)
    exp_user_prop2 = models.CharField(max_length=100, blank=True)
    exp_user_prop1 = models.CharField(max_length=100, blank=True)
    exp_element_state = models.IntegerField()
    exp_created_by = models.CharField(max_length=64)
    exp_created_date = models.DateField()
    exp_updated_by = models.CharField(max_length=64, blank=True)
    exp_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_expressions'

class Eul4ExpDeps(models.Model):
    ed_id = models.IntegerField(unique=True)
    ed_type = models.CharField(max_length=10)
    pd_p_id = models.IntegerField(null=True, blank=True)
    ped_exp_id = models.IntegerField(null=True, blank=True)
    pfd_fun_id = models.IntegerField(null=True, blank=True)
    psd_sq_id = models.IntegerField(null=True, blank=True)
    cd_exp_id = models.IntegerField(unique=True, null=True, blank=True)
    cfd_fun_id = models.IntegerField(null=True, blank=True)
    cid_exp_id = models.IntegerField(unique=True, null=True, blank=True)
    ed_element_state = models.IntegerField()
    ed_created_by = models.CharField(max_length=64)
    ed_created_date = models.DateField()
    ed_updated_by = models.CharField(max_length=64, blank=True)
    ed_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_exp_deps'

class Eul4FreqUnits(models.Model):
    rfu_id = models.IntegerField(unique=True)
    rfu_name_mn = models.IntegerField(unique=True)
    rfu_sql_expression = models.CharField(max_length=240)
    rfu_sequence = models.BigIntegerField(null=True, blank=True)
    rfu_element_state = models.IntegerField()
    rfu_created_by = models.CharField(max_length=64)
    rfu_created_date = models.DateField()
    rfu_updated_by = models.CharField(max_length=64, blank=True)
    rfu_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_freq_units'

class Eul4Functions(models.Model):
    fun_id = models.IntegerField(unique=True)
    fun_name = models.CharField(unique=True, max_length=100)
    fun_developer_key = models.CharField(unique=True, max_length=100)
    fun_description_s = models.CharField(max_length=240, blank=True)
    fun_description_mn = models.IntegerField(null=True, blank=True)
    fun_function_type = models.IntegerField()
    fun_hidden = models.IntegerField()
    fun_data_type = models.IntegerField()
    fun_available = models.IntegerField()
    fun_maximum_args = models.BigIntegerField(null=True, blank=True)
    fun_minimum_args = models.BigIntegerField()
    fun_built_in = models.IntegerField()
    fun_ext_name = models.CharField(max_length=64)
    fun_ext_package = models.CharField(max_length=64, blank=True)
    fun_ext_owner = models.CharField(max_length=64, blank=True)
    fun_ext_db_link = models.CharField(max_length=64, blank=True)
    fun_user_prop2 = models.CharField(max_length=100, blank=True)
    fun_user_prop1 = models.CharField(max_length=100, blank=True)
    fun_element_state = models.IntegerField()
    fun_created_by = models.CharField(max_length=64)
    fun_created_date = models.DateField()
    fun_updated_by = models.CharField(max_length=64, blank=True)
    fun_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_functions'

class Eul4FunArguments(models.Model):
    fa_id = models.IntegerField(unique=True)
    fa_name_s = models.CharField(unique=True, max_length=100, blank=True)
    fa_name_mn = models.IntegerField(unique=True, null=True, blank=True)
    fa_developer_key = models.CharField(unique=True, max_length=100)
    fa_description_s = models.CharField(max_length=240, blank=True)
    fa_description_mn = models.IntegerField(null=True, blank=True)
    fa_data_type = models.IntegerField()
    fa_optional = models.IntegerField()
    fa_position = models.BigIntegerField(unique=True)
    fa_fun_id = models.IntegerField(unique=True)
    fa_user_prop2 = models.CharField(max_length=100, blank=True)
    fa_user_prop1 = models.CharField(max_length=100, blank=True)
    fa_element_state = models.IntegerField()
    fa_created_by = models.CharField(max_length=64)
    fa_created_date = models.DateField()
    fa_updated_by = models.CharField(max_length=64, blank=True)
    fa_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_fun_arguments'

class Eul4FunCtgs(models.Model):
    fc_id = models.IntegerField(unique=True)
    fc_name_s = models.CharField(unique=True, max_length=100, blank=True)
    fc_name_mn = models.IntegerField(unique=True, null=True, blank=True)
    fc_developer_key = models.CharField(unique=True, max_length=100)
    fc_description_s = models.CharField(max_length=240, blank=True)
    fc_description_mn = models.IntegerField(null=True, blank=True)
    fc_user_prop2 = models.CharField(max_length=100, blank=True)
    fc_user_prop1 = models.CharField(max_length=100, blank=True)
    fc_element_state = models.IntegerField()
    fc_created_by = models.CharField(max_length=64)
    fc_created_date = models.DateField()
    fc_updated_by = models.CharField(max_length=64, blank=True)
    fc_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_fun_ctgs'

class Eul4FunFcLinks(models.Model):
    ffl_id = models.IntegerField(unique=True)
    ffl_fun_id = models.IntegerField(unique=True)
    ffl_fc_id = models.IntegerField(unique=True)
    ffl_element_state = models.IntegerField()
    ffl_created_by = models.CharField(max_length=64)
    ffl_created_date = models.DateField()
    ffl_updated_by = models.CharField(max_length=64, blank=True)
    ffl_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_fun_fc_links'

class Eul4Gateways(models.Model):
    gw_id = models.IntegerField(unique=True)
    gw_type = models.CharField(max_length=10)
    gw_gateway_name = models.CharField(max_length=100)
    gw_product_name = models.CharField(max_length=100)
    gw_description = models.CharField(max_length=240, blank=True)
    egw_version = models.CharField(max_length=30, blank=True)
    egw_database_link = models.CharField(max_length=64, blank=True)
    egw_schema = models.CharField(max_length=64, blank=True)
    egw_sql_paradigm = models.CharField(max_length=10, blank=True)
    gw_element_state = models.IntegerField()
    gw_created_by = models.CharField(max_length=64)
    gw_created_date = models.DateField()
    gw_updated_by = models.CharField(max_length=64, blank=True)
    gw_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_gateways'

class Eul4Hierarchies(models.Model):
    hi_id = models.IntegerField(unique=True)
    hi_type = models.CharField(max_length=10)
    hi_name = models.CharField(unique=True, max_length=100)
    hi_developer_key = models.CharField(unique=True, max_length=100)
    hi_description = models.CharField(max_length=240, blank=True)
    hi_sys_generated = models.IntegerField()
    hi_ext_hierarchy = models.CharField(max_length=64, blank=True)
    dbh_default = models.IntegerField(null=True, blank=True)
    ibh_dbh_id = models.IntegerField(null=True, blank=True)
    hi_user_prop2 = models.CharField(max_length=100, blank=True)
    hi_user_prop1 = models.CharField(max_length=100, blank=True)
    hi_element_state = models.IntegerField()
    hi_created_by = models.CharField(max_length=64)
    hi_created_date = models.DateField()
    hi_updated_by = models.CharField(max_length=64, blank=True)
    hi_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_hierarchies'

class Eul4HiNodes(models.Model):
    hn_id = models.IntegerField(unique=True)
    hn_name = models.CharField(unique=True, max_length=100)
    hn_developer_key = models.CharField(unique=True, max_length=100)
    hn_description = models.CharField(max_length=240, blank=True)
    hn_hi_id = models.IntegerField(unique=True)
    hn_ext_node = models.CharField(max_length=64, blank=True)
    hn_user_prop2 = models.CharField(max_length=100, blank=True)
    hn_user_prop1 = models.CharField(max_length=100, blank=True)
    hn_element_state = models.IntegerField()
    hn_created_by = models.CharField(max_length=64)
    hn_created_date = models.DateField()
    hn_updated_by = models.CharField(max_length=64, blank=True)
    hn_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_hi_nodes'

class Eul4HiSegments(models.Model):
    hs_id = models.IntegerField(unique=True)
    hs_type = models.CharField(max_length=10)
    dhs_hi_id = models.IntegerField(unique=True, null=True, blank=True)
    dhs_dhn_id_child = models.IntegerField(null=True, blank=True)
    dhs_dhn_id_parent = models.IntegerField(null=True, blank=True)
    ihs_hn_id_child = models.IntegerField(null=True, blank=True)
    ihs_hn_id_parent = models.IntegerField(null=True, blank=True)
    ihs_hi_id = models.IntegerField(null=True, blank=True)
    hs_element_state = models.IntegerField()
    hs_created_by = models.CharField(max_length=64)
    hs_created_date = models.DateField()
    hs_updated_by = models.CharField(max_length=64, blank=True)
    hs_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_hi_segments'

class Eul4IgExpLinks(models.Model):
    iel_id = models.IntegerField(unique=True)
    iel_type = models.CharField(max_length=10)
    hil_exp_id = models.IntegerField(null=True, blank=True)
    hil_hn_id = models.IntegerField(unique=True, null=True, blank=True)
    kil_exp_id = models.IntegerField(null=True, blank=True)
    kil_key_id = models.IntegerField(null=True, blank=True)
    kil_sequence = models.BigIntegerField(null=True, blank=True)
    iel_element_state = models.IntegerField()
    iel_created_by = models.CharField(max_length=64)
    iel_created_date = models.DateField()
    iel_updated_by = models.CharField(max_length=64, blank=True)
    iel_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_ig_exp_links'

class Eul4IhsFkLinks(models.Model):
    ifl_id = models.IntegerField(unique=True)
    ifl_ihs_id = models.IntegerField(unique=True)
    ifl_key_id = models.IntegerField(unique=True)
    ifl_element_state = models.IntegerField()
    ifl_created_by = models.CharField(max_length=64)
    ifl_created_date = models.DateField()
    ifl_updated_by = models.CharField(max_length=64, blank=True)
    ifl_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_ihs_fk_links'

class Eul4KeyCons(models.Model):
    key_id = models.IntegerField(unique=True)
    key_type = models.CharField(max_length=10)
    key_name = models.CharField(unique=True, max_length=100)
    key_developer_key = models.CharField(unique=True, max_length=100)
    key_description = models.CharField(max_length=240, blank=True)
    key_ext_key = models.CharField(max_length=64, blank=True)
    key_obj_id = models.IntegerField()
    uk_primary = models.IntegerField(null=True, blank=True)
    fk_key_id_remote = models.IntegerField(null=True, blank=True)
    fk_obj_id_remote = models.IntegerField(null=True, blank=True)
    fk_one_to_one = models.IntegerField(null=True, blank=True)
    fk_mstr_no_detail = models.IntegerField(null=True, blank=True)
    fk_dtl_no_master = models.IntegerField(null=True, blank=True)
    fk_mandatory = models.IntegerField(null=True, blank=True)
    key_user_prop2 = models.CharField(max_length=100, blank=True)
    key_user_prop1 = models.CharField(max_length=100, blank=True)
    key_element_state = models.IntegerField()
    key_created_by = models.CharField(max_length=64)
    key_created_date = models.DateField()
    key_updated_by = models.CharField(max_length=64, blank=True)
    key_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_key_cons'

class Eul4Objs(models.Model):
    obj_id = models.IntegerField(unique=True)
    obj_type = models.CharField(max_length=10)
    obj_name = models.CharField(unique=True, max_length=100)
    obj_developer_key = models.CharField(unique=True, max_length=100)
    obj_description = models.CharField(max_length=240, blank=True)
    obj_ba_id = models.IntegerField(null=True, blank=True)
    obj_hidden = models.IntegerField()
    obj_distinct_flag = models.IntegerField()
    obj_ndeterministic = models.IntegerField()
    obj_cbo_hint = models.CharField(max_length=100, blank=True)
    obj_ext_object = models.CharField(max_length=64, blank=True)
    obj_ext_owner = models.CharField(max_length=64, blank=True)
    obj_ext_db_link = models.CharField(max_length=64, blank=True)
    obj_object_sql1 = models.CharField(max_length=250, blank=True)
    obj_object_sql2 = models.CharField(max_length=250, blank=True)
    obj_object_sql3 = models.CharField(max_length=250, blank=True)
    sobj_ext_table = models.CharField(max_length=64, blank=True)
    obj_user_prop2 = models.CharField(max_length=100, blank=True)
    obj_user_prop1 = models.CharField(max_length=100, blank=True)
    obj_element_state = models.IntegerField()
    obj_created_by = models.CharField(max_length=64)
    obj_created_date = models.DateField()
    obj_updated_by = models.CharField(max_length=64, blank=True)
    obj_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_objs'

class Eul4ObjDeps(models.Model):
    od_id = models.IntegerField(unique=True)
    od_obj_id_from = models.IntegerField(unique=True)
    od_obj_id_to = models.IntegerField(unique=True)
    od_element_state = models.IntegerField()
    od_created_by = models.CharField(max_length=64)
    od_created_date = models.DateField()
    od_updated_by = models.CharField(max_length=64, blank=True)
    od_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_obj_deps'

class Eul4ObjJoinUsgs(models.Model):
    oju_id = models.IntegerField(unique=True)
    oju_obj_id = models.IntegerField(unique=True, null=True, blank=True)
    oju_join_modified = models.IntegerField()
    oju_key_id = models.IntegerField(unique=True)
    oju_sumo_id = models.IntegerField(unique=True, null=True, blank=True)
    oju_element_state = models.IntegerField()
    oju_created_by = models.CharField(max_length=64)
    oju_created_date = models.DateField()
    oju_updated_by = models.CharField(max_length=64, blank=True)
    oju_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_obj_join_usgs'


class Eul4QppStats(models.Model):
    qs_id = models.IntegerField(unique=True)
    qs_cost = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    qs_act_cpu_time = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    qs_act_elap_time = models.DecimalField(max_digits=127, decimal_places=127)
    qs_est_elap_time = models.DecimalField(max_digits=127, decimal_places=127)
    qs_object_use_key = models.CharField(max_length=240)
    qs_summary_fit = models.IntegerField(null=True, blank=True)
    qs_state = models.IntegerField(null=True, blank=True)
    qs_num_rows = models.IntegerField(null=True, blank=True)
    qs_doc_owner = models.CharField(max_length=64, blank=True)
    qs_doc_name = models.CharField(max_length=100, blank=True)
    qs_doc_details = models.CharField(max_length=240, blank=True)
    qs_sdo_id = models.IntegerField(null=True, blank=True)
    qs_dbmp0 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp1 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp2 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp3 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp4 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp5 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp6 = models.TextField(blank=True) # This field type is a guess.
    qs_dbmp7 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp0 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp1 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp2 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp3 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp4 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp5 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp6 = models.TextField(blank=True) # This field type is a guess.
    qs_mbmp7 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp0 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp1 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp2 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp3 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp4 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp5 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp6 = models.TextField(blank=True) # This field type is a guess.
    qs_jbmp7 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp0 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp1 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp2 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp3 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp4 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp5 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp6 = models.TextField(blank=True) # This field type is a guess.
    qs_fbmp7 = models.TextField(blank=True) # This field type is a guess.
    qs_created_by = models.CharField(max_length=64)
    qs_created_date = models.DateField()
    class Meta:
        db_table = u'eul4_qpp_stats'

class Eul4Segments(models.Model):
    seg_id = models.IntegerField(unique=True)
    seg_seg_type = models.IntegerField(unique=True)
    seg_sequence = models.BigIntegerField(unique=True)
    seg_obj_id = models.IntegerField(null=True, blank=True)
    seg_sumo_id = models.IntegerField(null=True, blank=True)
    seg_cuo_id = models.IntegerField(null=True, blank=True)
    seg_bq_id = models.IntegerField(unique=True, null=True, blank=True)
    seg_exp_id = models.IntegerField(unique=True, null=True, blank=True)
    seg_sms_id = models.IntegerField(unique=True, null=True, blank=True)
    seg_el_id = models.IntegerField(unique=True, null=True, blank=True)
    seg_chunk1 = models.CharField(max_length=250, blank=True)
    seg_chunk2 = models.CharField(max_length=250, blank=True)
    seg_chunk3 = models.CharField(max_length=250, blank=True)
    seg_chunk4 = models.CharField(max_length=250, blank=True)
    seg_element_state = models.IntegerField()
    seg_created_by = models.CharField(max_length=64)
    seg_created_date = models.DateField()
    seg_updated_by = models.CharField(max_length=64, blank=True)
    seg_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_segments'

class Eul4Sequences(models.Model):
    seq_id = models.IntegerField()
    seq_name = models.CharField(max_length=100)
    seq_nextval = models.BigIntegerField()
    class Meta:
        db_table = u'eul4_sequences'

class Eul4SqCrrltns(models.Model):
    sqc_id = models.IntegerField(unique=True)
    sqc_sq_id = models.IntegerField(unique=True)
    sqc_it_inner_id = models.IntegerField(unique=True)
    sqc_it_outer_id = models.IntegerField(unique=True)
    sqc_element_state = models.IntegerField()
    sqc_created_by = models.CharField(max_length=64)
    sqc_created_date = models.DateField()
    sqc_updated_by = models.CharField(max_length=64, blank=True)
    sqc_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_sq_crrltns'

class Eul4SubQueries(models.Model):
    sq_id = models.IntegerField(unique=True)
    sq_name = models.CharField(unique=True, max_length=100)
    sq_developer_key = models.CharField(unique=True, max_length=100)
    sq_description = models.CharField(max_length=240, blank=True)
    sq_obj_id = models.IntegerField()
    sq_it_id = models.IntegerField()
    sq_fil_id = models.IntegerField(unique=True)
    sq_user_prop2 = models.CharField(max_length=100, blank=True)
    sq_user_prop1 = models.CharField(max_length=100, blank=True)
    sq_element_state = models.IntegerField()
    sq_created_by = models.CharField(max_length=64)
    sq_created_date = models.DateField()
    sq_updated_by = models.CharField(max_length=64, blank=True)
    sq_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_sub_queries'

class Eul4SummaryObjs(models.Model):
    sumo_id = models.IntegerField(unique=True)
    sumo_type = models.CharField(max_length=10)
    sumo_internal = models.IntegerField()
    sumo_item_deleted = models.IntegerField()
    sumo_item_modified = models.IntegerField()
    sumo_join_state = models.IntegerField()
    sumo_validity = models.IntegerField()
    sumo_ext_object = models.CharField(max_length=64, blank=True)
    sumo_ext_owner = models.CharField(max_length=64, blank=True)
    sumo_ext_db_link = models.CharField(max_length=64, blank=True)
    sumo_asmp_id = models.IntegerField(null=True, blank=True)
    sumo_active = models.IntegerField()
    sbo_srs_id = models.IntegerField(unique=True, null=True, blank=True)
    sbo_max_item_comb = models.BigIntegerField(null=True, blank=True)
    sdo_sbo_id = models.IntegerField(null=True, blank=True)
    sdo_num_joins = models.BigIntegerField(null=True, blank=True)
    sdo_num_usgs = models.BigIntegerField(null=True, blank=True)
    sdo_num_axis_items = models.BigIntegerField(null=True, blank=True)
    sdo_num_rows = models.BigIntegerField(null=True, blank=True)
    sdo_bitmap_pos = models.BigIntegerField(unique=True, null=True, blank=True)
    sdo_object_sql1 = models.CharField(max_length=250, blank=True)
    sdo_object_sql2 = models.CharField(max_length=250, blank=True)
    sdo_object_sql3 = models.CharField(max_length=250, blank=True)
    sdo_last_refresh = models.DateField(null=True, blank=True)
    sdo_table_name = models.CharField(max_length=64, blank=True)
    sdo_table_owner = models.CharField(max_length=64, blank=True)
    sdo_database_link = models.CharField(max_length=64, blank=True)
    msdo_svr_err_code = models.BigIntegerField(null=True, blank=True)
    msdo_svr_err_text = models.CharField(max_length=240, blank=True)
    msdo_refresh_reqd = models.IntegerField(null=True, blank=True)
    ems_commit_size = models.BigIntegerField(null=True, blank=True)
    ems_state = models.IntegerField(null=True, blank=True)
    sumo_element_state = models.IntegerField()
    sumo_created_by = models.CharField(max_length=64)
    sumo_created_date = models.DateField()
    sumo_updated_by = models.CharField(max_length=64, blank=True)
    sumo_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_summary_objs'

class Eul4SumoExpUsgs(models.Model):
    seu_id = models.IntegerField(unique=True)
    seu_type = models.CharField(unique=True, max_length=10)
    seu_sumo_id = models.IntegerField(unique=True)
    seu_ext_column = models.CharField(max_length=64, blank=True)
    seu_visible = models.IntegerField()
    siu_exp_id = models.IntegerField(null=True, blank=True)
    siu_item_modified = models.IntegerField(null=True, blank=True)
    smiu_fun_id = models.IntegerField(null=True, blank=True)
    sfu_fun_id = models.IntegerField(null=True, blank=True)
    seu_element_state = models.IntegerField()
    seu_created_by = models.CharField(max_length=64)
    seu_created_date = models.DateField()
    seu_updated_by = models.CharField(max_length=64, blank=True)
    seu_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_sumo_exp_usgs'

class Eul4SumBitmaps(models.Model):
    sb_id = models.IntegerField(unique=True)
    sb_bitmap = models.TextField() # This field type is a guess.
    sb_sequence = models.BigIntegerField(unique=True)
    sb_exp_id = models.IntegerField(unique=True, null=True, blank=True)
    sb_key_id = models.IntegerField(unique=True, null=True, blank=True)
    sb_fun_id = models.IntegerField(null=True, blank=True)
    sb_element_state = models.IntegerField()
    sb_created_by = models.CharField(max_length=64)
    sb_created_date = models.DateField()
    sb_updated_date = models.DateField(null=True, blank=True)
    sb_updated_by = models.CharField(max_length=64, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_sum_bitmaps'

class Eul4SumRfshSets(models.Model):
    srs_id = models.IntegerField(unique=True)
    srs_name = models.CharField(unique=True, max_length=100)
    srs_developer_key = models.CharField(unique=True, max_length=100)
    srs_description = models.CharField(max_length=240, blank=True)
    srs_state = models.IntegerField()
    srs_online = models.IntegerField()
    srs_auto_refresh = models.IntegerField()
    srs_last_refresh = models.DateField(null=True, blank=True)
    srs_next_refresh = models.DateField(null=True, blank=True)
    srs_job_id = models.BigIntegerField(null=True, blank=True)
    srs_eu_id = models.IntegerField()
    srs_num_freq_units = models.BigIntegerField(null=True, blank=True)
    srs_rfu_id = models.IntegerField(null=True, blank=True)
    srs_refresh_count = models.BigIntegerField(null=True, blank=True)
    srs_user_prop2 = models.CharField(max_length=100, blank=True)
    srs_user_prop1 = models.CharField(max_length=100, blank=True)
    srs_element_state = models.IntegerField()
    srs_created_by = models.CharField(max_length=64)
    srs_created_date = models.DateField()
    srs_updated_by = models.CharField(max_length=64, blank=True)
    srs_updated_date = models.DateField(null=True, blank=True)
    notm = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_sum_rfsh_sets'

class Eul4Versions(models.Model):
    ver_name = models.CharField(max_length=100, blank=True)
    ver_description = models.CharField(max_length=240, blank=True)
    ver_release = models.CharField(max_length=30)
    ver_min_code_ver = models.CharField(max_length=30)
    ver_eul_timestamp = models.CharField(max_length=30)
    ver_sa = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'eul4_versions'

class ExchangeRates(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    currency_code = models.CharField(unique=True, max_length=3)
    currency_code_referred_to = models.CharField(unique=True, max_length=3)
    start_date = models.DateField(unique=True)
    end_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=18, decimal_places=6)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'exchange_rates'

class ExchangeRatesBck(models.Model):
    org_unit_code = models.CharField(max_length=13)
    currency_code = models.CharField(max_length=3)
    currency_code_referred_to = models.CharField(max_length=3)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    value = models.DecimalField(max_digits=18, decimal_places=6)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'exchange_rates_bck'

class Frm50Bindvar(models.Model):
    owner = models.CharField(max_length=32, blank=True)
    modid = models.IntegerField(null=True, blank=True)
    itemid = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    nextbpos = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    plsqlbv_ep = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    total_bindvar = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'frm50__bindvar'

class Frm50Buffer(models.Model):
    owner = models.CharField(max_length=32, blank=True)
    modid = models.IntegerField(null=True, blank=True)
    startaddr = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    startref = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    datatype = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    longid = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'frm50__buffer'

class Frm50Grp(models.Model):
    owner = models.CharField(max_length=30, blank=True)
    modid = models.IntegerField(unique=True, null=True, blank=True)
    itemid = models.IntegerField(unique=True, null=True, blank=True)
    grpname = models.CharField(max_length=30, blank=True)
    grpflag = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'frm50__grp'

class Frm50Object(models.Model):
    owner = models.CharField(max_length=32, blank=True)
    modid = models.IntegerField(null=True, blank=True)
    itemid = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    name = models.CharField(max_length=32, blank=True)
    objecttype = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    sequence = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rawlen = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    textlen = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    chunkno = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    scopeid = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    scope1 = models.CharField(max_length=32, blank=True)
    scope2 = models.CharField(max_length=32, blank=True)
    scope3 = models.CharField(max_length=32, blank=True)
    rawdata = models.TextField(blank=True) # This field type is a guess.
    textdata1 = models.CharField(max_length=2000, blank=True)
    textdata2 = models.CharField(max_length=2000, blank=True)
    textdata3 = models.CharField(max_length=2000, blank=True)
    textdata4 = models.CharField(max_length=2000, blank=True)
    programunitid = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'frm50__object'

class GeoPoints(models.Model):
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(unique=True, max_length=30)
    latitude_degrees = models.IntegerField(null=True, blank=True)
    latitude_minutes = models.IntegerField(null=True, blank=True)
    latitude_direction = models.CharField(max_length=1, blank=True)
    longitude_degrees = models.IntegerField(null=True, blank=True)
    longitude_minutes = models.IntegerField(null=True, blank=True)
    longitude_direction = models.CharField(max_length=1, blank=True)
    port_indicator = models.CharField(max_length=1)
    country_code = models.CharField(unique=True, max_length=3)
    sector_code = models.CharField(unique=True, max_length=3)
    sub_sector_code = models.CharField(unique=True, max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'geo_points'

class Help2Forms(models.Model):
    canvasname = models.CharField(unique=True, max_length=100, blank=True)
    tabpagename = models.CharField(unique=True, max_length=100, blank=True)
    formname = models.CharField(unique=True, max_length=100)
    helpfilename = models.CharField(unique=True, max_length=100, blank=True)
    topicname = models.CharField(unique=True, max_length=100, blank=True)
    nodename = models.CharField(unique=True, max_length=100, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'help2forms'

class HstCnfdspdtl(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_destination_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    quality_received = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.DecimalField(max_digits=11, decimal_places=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_cnfdspdtl'

class HstCnfdspdtlBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    org_unit_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_destination_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quality_received = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.DecimalField(max_digits=11, decimal_places=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_cnfdspdtl_bck'

class HstCnfdspmst(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    extra_code = models.CharField(max_length=25, blank=True)
    receipt_location_code = models.CharField(max_length=10)
    tran_type_code_rec = models.CharField(max_length=4)
    tran_type_descr_rec = models.CharField(max_length=50, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateField()
    end_discharge_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_cnfdspmst'

class HstCnfdspmstBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    org_unit_code = models.CharField(max_length=13)
    extra_code = models.CharField(max_length=25, blank=True)
    receipt_location_code = models.CharField(max_length=10)
    tran_type_code_rec = models.CharField(max_length=4)
    tran_type_descr_rec = models.CharField(max_length=50, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    arrival_date = models.DateField()
    end_discharge_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_cnfdspmst_bck'

class HstDspdtl(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    si_record_id = models.CharField(unique=True, max_length=25, blank=True)
    origin_id = models.CharField(unique=True, max_length=23, blank=True)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_destination_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'hst_dspdtl'

class HstDspdtlBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    si_record_id = models.CharField(max_length=25, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_destination_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'hst_dspdtl_bck'

class HstDspmst(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    dispatch_date = models.DateField()
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=13)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    destination_code = models.CharField(max_length=13, blank=True)
    pro_activity_code = models.CharField(max_length=6, blank=True)
    activity_ouc = models.CharField(max_length=13, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    loan_id = models.CharField(max_length=25, blank=True)
    loading_date = models.DateField()
    organization_id = models.CharField(max_length=12)
    tran_type_code = models.CharField(max_length=4)
    tran_type_descr = models.CharField(max_length=50, blank=True)
    modetrans_code = models.CharField(max_length=2)
    comments = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    certifing_title = models.CharField(max_length=50, blank=True)
    trans_contractor_code = models.CharField(max_length=4)
    supplier1_ouc = models.CharField(max_length=13)
    trans_subcontractor_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    nmbplt_id = models.CharField(max_length=25, blank=True)
    nmbtrl_id = models.CharField(max_length=25, blank=True)
    driver_name = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=20, blank=True)
    vehicle_registration = models.CharField(max_length=20, blank=True)
    trailer_plate = models.CharField(max_length=20, blank=True)
    container_number = models.CharField(max_length=15, blank=True)
    atl_li_code = models.CharField(max_length=8, blank=True)
    notify_indicator = models.CharField(max_length=1, blank=True)
    customised = models.CharField(max_length=50, blank=True)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    notify_org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_dspmst'

class HstDspmstBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    dispatch_date = models.DateField()
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=13)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    destination_code = models.CharField(max_length=13, blank=True)
    pro_activity_code = models.CharField(max_length=6, blank=True)
    activity_ouc = models.CharField(max_length=13, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    loan_id = models.CharField(max_length=25, blank=True)
    loading_date = models.DateField()
    organization_id = models.CharField(max_length=12)
    tran_type_code = models.CharField(max_length=4)
    tran_type_descr = models.CharField(max_length=50, blank=True)
    modetrans_code = models.CharField(max_length=2)
    comments = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    certifing_title = models.CharField(max_length=50, blank=True)
    trans_contractor_code = models.CharField(max_length=4)
    supplier1_ouc = models.CharField(max_length=13)
    trans_subcontractor_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    nmbplt_id = models.CharField(max_length=25, blank=True)
    nmbtrl_id = models.CharField(max_length=25, blank=True)
    driver_name = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=20, blank=True)
    vehicle_registration = models.CharField(max_length=20, blank=True)
    trailer_plate = models.CharField(max_length=20, blank=True)
    container_number = models.CharField(max_length=15, blank=True)
    atl_li_code = models.CharField(max_length=8, blank=True)
    notify_indicator = models.CharField(max_length=1, blank=True)
    customised = models.CharField(max_length=50, blank=True)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    notify_org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_dspmst_bck'

class HstLtidtl(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    lti_id = models.CharField(unique=True, max_length=25)
    si_record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_ltidtl'

class HstLtidtlBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    lti_id = models.CharField(max_length=25)
    si_record_id = models.CharField(max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_ltidtl_bck'

class HstLtimst(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    lti_id = models.CharField(unique=True, max_length=25)
    code = models.CharField(max_length=25)
    lti_date = models.DateField()
    contract_code = models.CharField(max_length=20, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=10)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    organization_id = models.CharField(max_length=12)
    requested_dispatch_date = models.DateField(null=True, blank=True)
    inspection_indicator = models.CharField(max_length=1, blank=True)
    officer_code = models.CharField(max_length=7)
    person2_ouc = models.CharField(max_length=13)
    title_of_officer = models.CharField(max_length=50, blank=True)
    issuing_code = models.CharField(max_length=7)
    person1_ouc = models.CharField(max_length=13)
    title_of_issuing = models.CharField(max_length=50, blank=True)
    transporter_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    transport_rate_type = models.CharField(max_length=10, blank=True)
    transport_currency = models.CharField(max_length=3, blank=True)
    transport_rate = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_entitlement = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_rate = models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)
    fuel_currency = models.CharField(max_length=5, blank=True)
    food_release = models.CharField(max_length=6, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    remarks_b = models.CharField(max_length=250, blank=True)
    observations = models.CharField(max_length=250, blank=True)
    status_indicator = models.CharField(max_length=1)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_ltimst'

class HstLtimstBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.DecimalField(max_digits=127, decimal_places=127)
    lti_id = models.CharField(max_length=25)
    code = models.CharField(max_length=25)
    lti_date = models.DateField()
    contract_code = models.CharField(max_length=20, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=10)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    organization_id = models.CharField(max_length=12)
    requested_dispatch_date = models.DateField(null=True, blank=True)
    inspection_indicator = models.CharField(max_length=1, blank=True)
    officer_code = models.CharField(max_length=7)
    person2_ouc = models.CharField(max_length=13)
    title_of_officer = models.CharField(max_length=50, blank=True)
    issuing_code = models.CharField(max_length=7)
    person1_ouc = models.CharField(max_length=13)
    title_of_issuing = models.CharField(max_length=50, blank=True)
    transporter_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    transport_rate_type = models.CharField(max_length=10, blank=True)
    transport_currency = models.CharField(max_length=3, blank=True)
    transport_rate = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_entitlement = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_rate = models.DecimalField(null=True, max_digits=15, decimal_places=5, blank=True)
    fuel_currency = models.CharField(max_length=5, blank=True)
    food_release = models.CharField(max_length=6, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    remarks_b = models.CharField(max_length=250, blank=True)
    observations = models.CharField(max_length=250, blank=True)
    status_indicator = models.CharField(max_length=1)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'hst_ltimst_bck'

class InstallationStatus(models.Model):
    org_unit_code = models.CharField(max_length=13, primary_key=True)
    version_d = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=2000, blank=True)
    max_extent = models.CharField(max_length=1, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'installation_status'

class InternalAdjustments(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    adjustment_date = models.DateField(unique=True)
    adjustment_id = models.IntegerField(unique=True)
    adjustment_type = models.IntegerField()
    storage_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    new_quality = models.CharField(max_length=1, blank=True)
    new_allocation_code = models.CharField(max_length=10, blank=True)
    new_quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    new_quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    new_number_of_units = models.IntegerField(null=True, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    person_title = models.CharField(max_length=50)
    reason = models.CharField(max_length=250)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'internal_adjustments'

class InterConsignments(models.Model):
    intvyg_code = models.CharField(unique=True, max_length=25)
    intdlv_code = models.IntegerField(unique=True)
    intcns_code = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    si_record_id = models.CharField(max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    net_metric_tons = models.DecimalField(max_digits=11, decimal_places=3)
    gross_metric_tons = models.DecimalField(max_digits=11, decimal_places=3)
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    delivery_number = models.CharField(unique=True, max_length=10, blank=True)
    container_type = models.CharField(max_length=3, blank=True)
    containers_count = models.IntegerField(null=True, blank=True)
    pallets_count = models.IntegerField(null=True, blank=True)
    package_count = models.IntegerField(null=True, blank=True)
    complete_indicator = models.CharField(max_length=1)
    origin_id = models.CharField(max_length=23, blank=True)
    wis_indicator = models.CharField(max_length=1)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_consignments'

class InterConsignmentsBck1(models.Model):
    intvyg_code = models.CharField(max_length=25)
    intdlv_code = models.IntegerField()
    intcns_code = models.DecimalField(max_digits=127, decimal_places=127)
    si_record_id = models.CharField(max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    net_metric_tons = models.DecimalField(max_digits=11, decimal_places=3)
    gross_metric_tons = models.DecimalField(max_digits=11, decimal_places=3)
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    container_type = models.CharField(max_length=3, blank=True)
    containers_count = models.IntegerField(null=True, blank=True)
    pallets_count = models.IntegerField(null=True, blank=True)
    package_count = models.IntegerField(null=True, blank=True)
    complete_indicator = models.CharField(max_length=1)
    origin_id = models.CharField(max_length=23, blank=True)
    wis_indicator = models.CharField(max_length=1)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_consignments_bck1'

class InterDeliveries(models.Model):
    intvyg_code = models.CharField(unique=True, max_length=25)
    intdlv_code = models.IntegerField(unique=True)
    bill_of_lading_date = models.DateField(unique=True)
    bill_of_lading_code = models.CharField(unique=True, max_length=30)
    remarks_text = models.CharField(max_length=2000, blank=True)
    wis_indicator = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_deliveries'

class InterDeliveriesBck1(models.Model):
    intvyg_code = models.CharField(max_length=25)
    intdlv_code = models.IntegerField()
    bill_of_lading_date = models.DateField()
    bill_of_lading_code = models.CharField(max_length=30)
    remarks_text = models.CharField(max_length=2000, blank=True)
    wis_indicator = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_deliveries_bck1'

class InterVoyages(models.Model):
    intvyg_code = models.CharField(unique=True, max_length=25)
    voyage_id = models.CharField(unique=True, max_length=10)
    load_point_code = models.CharField(unique=True, max_length=10)
    discharge_point_code = models.CharField(unique=True, max_length=10)
    vessel_name = models.CharField(unique=True, max_length=50)
    carriage_type = models.CharField(max_length=1)
    ata_date = models.DateField(null=True, blank=True)
    eta_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    shipping_agent_code = models.CharField(max_length=4, blank=True)
    supplier1_ouc = models.CharField(max_length=13, blank=True)
    clearing_agent_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    wis_indicator = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_voyages'

class InterVoyagesBck1(models.Model):
    intvyg_code = models.CharField(max_length=25)
    voyage_id = models.CharField(max_length=10)
    load_point_code = models.CharField(max_length=10)
    discharge_point_code = models.CharField(max_length=10)
    vessel_name = models.CharField(max_length=50)
    carriage_type = models.CharField(max_length=1)
    ata_date = models.DateField(null=True, blank=True)
    eta_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    shipping_agent_code = models.CharField(max_length=4, blank=True)
    supplier1_ouc = models.CharField(max_length=13, blank=True)
    clearing_agent_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    wis_indicator = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'inter_voyages_bck1'

class InvmstFormItems(models.Model):
    item_record_id = models.CharField(unique=True, max_length=25)
    invoice_id = models.CharField(unique=True, max_length=25)
    item_value = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invmst_form_items'

class InvmstFormItemsBck(models.Model):
    item_record_id = models.CharField(max_length=25)
    invoice_id = models.CharField(max_length=25)
    item_value = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invmst_form_items_bck'

class InvoiceDetails(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    invoice_line_id = models.BigIntegerField(unique=True)
    rate = models.DecimalField(max_digits=11, decimal_places=2)
    exchange_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    cif_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    calculation_type = models.CharField(max_length=1, blank=True)
    tpo_id = models.CharField(max_length=25, blank=True)
    tpo_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    delete_by = models.CharField(max_length=30, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invoice_details'

class InvoiceDetailsBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    invoice_line_id = models.BigIntegerField()
    rate = models.DecimalField(max_digits=11, decimal_places=2)
    exchange_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=10, decimal_places=3, blank=True)
    cif_value = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    calculation_type = models.CharField(max_length=1, blank=True)
    tpo_id = models.CharField(max_length=25, blank=True)
    tpo_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    delete_by = models.CharField(max_length=30, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invoice_details_bck'

class InvoiceMasters(models.Model):
    invoice_id = models.CharField(unique=True, max_length=25)
    org_unit_code = models.CharField(max_length=13)
    invoice_code = models.CharField(max_length=50)
    invoice_date = models.DateField()
    supplier_ouc = models.CharField(max_length=13)
    supplier_code = models.CharField(max_length=4)
    currency = models.CharField(max_length=3)
    remarks = models.CharField(max_length=50, blank=True)
    invoice_status = models.CharField(max_length=1, blank=True)
    paid = models.CharField(max_length=1, blank=True)
    tpo_id = models.CharField(max_length=25, blank=True)
    tpo_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invoice_masters'

class InvoiceMastersBck(models.Model):
    invoice_id = models.CharField(max_length=25)
    org_unit_code = models.CharField(max_length=13)
    invoice_code = models.CharField(max_length=50)
    invoice_date = models.DateField()
    supplier_ouc = models.CharField(max_length=13)
    supplier_code = models.CharField(max_length=4)
    currency = models.CharField(max_length=3)
    remarks = models.CharField(max_length=50, blank=True)
    invoice_status = models.CharField(max_length=1, blank=True)
    paid = models.CharField(max_length=1, blank=True)
    tpo_id = models.CharField(max_length=25, blank=True)
    tpo_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'invoice_masters_bck'

class KSS2Snapshots(models.Model):
    t_name = models.CharField(unique=True, max_length=50)
    updatable = models.CharField(max_length=1)
    down = models.CharField(max_length=1)
    w_clause = models.CharField(max_length=2000, blank=True)
    sorting = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$$2_snapshots'

class KSSPacklog(models.Model):
    s_off = models.CharField(max_length=13)
    d_off = models.CharField(max_length=13, blank=True)
    pack = models.BigIntegerField(null=True, blank=True)
    s_date = models.DateField()
    r_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$$_packlog'

class KSSRepLog(models.Model):
    job_n = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    d_off = models.CharField(max_length=13, blank=True)
    text = models.CharField(max_length=2000, blank=True)
    class Meta:
        db_table = u'k$$_rep_log'

class KSSRepRunning(models.Model):
    job_n = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    d_off = models.CharField(unique=True, max_length=13)
    s_date = models.DateField(null=True, blank=True)
    name_file = models.CharField(max_length=2000, blank=True)
    flag_status = models.CharField(max_length=1, blank=True)
    job_type = models.CharField(max_length=1, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$$_rep_running'

class KSActualBeneficiaries(models.Model):
    beneficiary_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_actual_beneficiaries'

class KSBaseLabels(models.Model):
    lbl_record_id = models.DecimalField(max_digits=127, decimal_places=127)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_base_labels'

class KSCnfdspDetails(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    quality_received = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_cnfdsp_details'

class KSCnfdspDetailsBck(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    quality_received = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_cnfdsp_details_bck'

class KSCnfdspMasters(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_cnfdsp_masters'

class KSCodeTables(models.Model):
    table_type_cde = models.CharField(max_length=3, blank=True)
    table_cde = models.CharField(max_length=8, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'k$_code_tables'

class KSCoiToSis(models.Model):
    si_record_id = models.CharField(max_length=25)
    origin_id = models.CharField(max_length=23)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_coi_to_sis'

class KSCommcifBasecost(models.Model):
    record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_commcif_basecost'

class KSCommodities(models.Model):
    comm_category_code = models.CharField(max_length=9, blank=True)
    code = models.CharField(max_length=18, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_commodities'

class KSCommodityOrigins(models.Model):
    origin_id = models.CharField(max_length=23, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_commodity_origins'

class KSCommCategories(models.Model):
    code = models.CharField(max_length=9, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_comm_categories'

class KSCommPacked(models.Model):
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_comm_packed'

class KSCompasJob(models.Model):
    job = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_compas_job'

class KSCompasMenu(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    code_menu = models.CharField(max_length=30, blank=True)
    code_role = models.BigIntegerField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_compas_menu'

class KSCompasMessages(models.Model):
    message_type = models.CharField(max_length=3, blank=True)
    message_number = models.BigIntegerField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_compas_messages'

class KSCompasUsers(models.Model):
    compas_user_id = models.CharField(max_length=25, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_compas_users'

class KSCountries(models.Model):
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_countries'

class KSCurrencies(models.Model):
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_currencies'

class KSCustomizedFormItems(models.Model):
    record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_customized_form_items'

class KSCustomizedPrivileges(models.Model):
    compas_user_id = models.CharField(max_length=25, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    menu_record_id = models.CharField(max_length=25, blank=True)
    standard_role_code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_customized_privileges'

class KSCustomizedPrvData(models.Model):
    compas_user_id = models.CharField(max_length=25, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    menu_record_id = models.CharField(max_length=25, blank=True)
    standard_role_code = models.CharField(max_length=3, blank=True)
    data_org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_customized_prv_data'

class KSCPrjTypes(models.Model):
    code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_c_prj_types'

class KSDispatchDetails(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_dispatch_details'

class KSDispatchFormItems(models.Model):
    item_record_id = models.CharField(max_length=25, blank=True)
    dispatch_code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_dispatch_form_items'

class KSDispatchMasters(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_dispatch_masters'

class KSDistanceRates(models.Model):
    org_unit_code = models.CharField(max_length=13)
    origin_warehouse_code = models.CharField(max_length=13)
    destination_warehouse_code = models.CharField(max_length=13)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_distance_rates'

class KSDistributionDetails(models.Model):
    dst_record_id = models.CharField(max_length=25, blank=True)
    dst_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_distribution_details'

class KSDistributionMasters(models.Model):
    dst_record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_distribution_masters'

class KSDocumentTypes(models.Model):
    code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_document_types'

class KSDspcstTrntypes(models.Model):
    record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_dspcst_trntypes'

class KSDstActualBeneficiaries(models.Model):
    dst_record_id = models.CharField(max_length=25, blank=True)
    beneficiary_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_dst_actual_beneficiaries'

class KSExchangeRates(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    currency_code = models.CharField(max_length=3, blank=True)
    currency_code_referred_to = models.CharField(max_length=3, blank=True)
    start_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_exchange_rates'

class KSGeoPoints(models.Model):
    code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_geo_points'

class KSHelp2Forms(models.Model):
    canvasname = models.CharField(max_length=100, blank=True)
    tabpagename = models.CharField(max_length=100, blank=True)
    formname = models.CharField(max_length=100, blank=True)
    helpfilename = models.CharField(max_length=100, blank=True)
    topicname = models.CharField(max_length=100, blank=True)
    nodename = models.CharField(max_length=100, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_help2forms'

class KSHstCnfdspdtl(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    quality_received = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_cnfdspdtl'

class KSHstCnfdspmst(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_cnfdspmst'

class KSHstDspdtl(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    si_record_id = models.CharField(max_length=25, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_dspdtl'

class KSHstDspmst(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_dspmst'

class KSHstLtidtl(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    si_record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_ltidtl'

class KSHstLtimst(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_hst_ltimst'

class KSInstallationStatus(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'k$_installation_status'

class KSInternalAdjustments(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    adjustment_date = models.DateField(null=True, blank=True)
    adjustment_id = models.IntegerField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_internal_adjustments'

class KSInterConsignments(models.Model):
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    intcns_code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_inter_consignments'

class KSInterDeliveries(models.Model):
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_inter_deliveries'

class KSInterVoyages(models.Model):
    intvyg_code = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_inter_voyages'

class KSInvmstFormItems(models.Model):
    item_record_id = models.CharField(max_length=25, blank=True)
    invoice_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_invmst_form_items'

class KSInvoiceDetails(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    invoice_line_id = models.BigIntegerField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_invoice_details'

class KSInvoiceMasters(models.Model):
    invoice_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_invoice_masters'

class KSLoanDetails(models.Model):
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_loan_details'

class KSLoanMasters(models.Model):
    lonmst_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_loan_masters'

class KSLocalCurrency(models.Model):
    org_unit_code = models.CharField(max_length=13)
    currency = models.CharField(max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_local_currency'

class KSLossDamageCauses(models.Model):
    name_record_id = models.CharField(max_length=25)
    record_id = models.DecimalField(max_digits=127, decimal_places=127)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_loss_damage_causes'

class KSLossDamageNames(models.Model):
    record_id = models.CharField(max_length=25)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_loss_damage_names'

class KSLtiDetails(models.Model):
    lti_id = models.CharField(max_length=25, blank=True)
    si_record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_lti_details'

class KSLtiFormItems(models.Model):
    item_record_id = models.CharField(max_length=25, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_lti_form_items'

class KSLtiMasters(models.Model):
    lti_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_lti_masters'

class KSMemoInvoices(models.Model):
    memo_number = models.CharField(max_length=25, blank=True)
    memo_date = models.DateField(null=True, blank=True)
    invoice_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_memo_invoices'

class KSMenuItems(models.Model):
    menu_record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_menu_items'

class KSModules(models.Model):
    module_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_modules'

class KSNotifications(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    notify_number = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    notify_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_notifications'

class KSOrganizations(models.Model):
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_organizations'

class KSOrgUnits(models.Model):
    code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_org_units'

class KSOrgUnitTypes(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_org_unit_types'

class KSOtsOverview(models.Model):
    record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_ots_overview'

class KSOverlandArrDetails(models.Model):
    code = models.CharField(max_length=25, blank=True)
    lndarrd_code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_overland_arr_details'

class KSOverlandArrMasters(models.Model):
    code = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_overland_arr_masters'

class KSPackageTypes(models.Model):
    code = models.CharField(max_length=17, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_package_types'

class KSPaMaster(models.Model):
    wis_code = models.CharField(max_length=8, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=13, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_pa_master'

class KSPersons(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    code = models.CharField(max_length=7, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_persons'

class KSPhysicalInventory(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    storage_code = models.CharField(max_length=13, blank=True)
    si_record_id = models.CharField(max_length=25, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    date_inventory = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_physical_inventory'

class KSPrjOrgUnits(models.Model):
    project_code = models.CharField(max_length=8, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_prj_org_units'

class KSProgramName(models.Model):
    program_name = models.CharField(max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_program_name'

class KSProjects(models.Model):
    code = models.CharField(max_length=8, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_projects'

class KSProActivities(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    code = models.CharField(max_length=6, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_pro_activities'

class KSRateTypes(models.Model):
    rate_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_rate_types'

class KSRcvcstTrntypes(models.Model):
    dsp_record_id = models.CharField(max_length=25, blank=True)
    tran_type_code = models.CharField(max_length=4, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_rcvcst_trntypes'

class KSReceiptDetails(models.Model):
    code = models.CharField(max_length=25)
    document_code = models.CharField(max_length=2)
    org_unit_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_destination_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_receipt_details'

class KSReceiptFormItems(models.Model):
    item_record_id = models.CharField(max_length=25, blank=True)
    receipt_code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_receipt_form_items'

class KSReceiptMasters(models.Model):
    code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_receipt_masters'

class KSReconstitutions(models.Model):
    org_unit_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    creation_date = models.DateField()
    new_package_code = models.CharField(max_length=17)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_reconstitutions'

class KSRepackings(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    repacked_package_code = models.CharField(max_length=17, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_repackings'

class KSRepayDetails(models.Model):
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_repay_details'

class KSSapBlDetails(models.Model):
    shipment_number = models.CharField(max_length=10, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    load_point_code = models.CharField(max_length=10, blank=True)
    discharge_point_code = models.CharField(max_length=10, blank=True)
    bl_date = models.DateField(null=True, blank=True)
    bl_code = models.CharField(max_length=30, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_bl_details'

class KSSapDeliveries(models.Model):
    delivery_number = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_deliveries'

class KSSapGoodReceipts(models.Model):
    po_number = models.CharField(max_length=10, blank=True)
    po_line_number = models.CharField(max_length=5, blank=True)
    document_date = models.DateField(null=True, blank=True)
    document_number = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=7, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_good_receipts'

class KSSapLtshRates(models.Model):
    rate_seqnum = models.CharField(max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_ltsh_rates'

class KSSapPrRates(models.Model):
    pr_number = models.CharField(max_length=10)
    pr_line_number = models.CharField(max_length=5)
    rate_seqnum = models.CharField(max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_pr_rates'

class KSSapPurchaseOrders(models.Model):
    po_number = models.CharField(max_length=10, blank=True)
    po_line_number = models.CharField(max_length=5, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_purchase_orders'

class KSSapPurchaseRequisitions(models.Model):
    pr_number = models.CharField(max_length=10, blank=True)
    pr_line_number = models.CharField(max_length=5, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_purchase_requisitions'

class KSSapResourceRequests(models.Model):
    rr_number = models.CharField(max_length=10, blank=True)
    rr_line_number = models.CharField(max_length=5, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_resource_requests'

class KSSapShipments(models.Model):
    shipment_number = models.CharField(max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_shipments'

class KSSapShpdates(models.Model):
    shipment_number = models.CharField(max_length=10, blank=True)
    load_point_code = models.CharField(max_length=10, blank=True)
    discharge_point_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_shpdates'

class KSSapStages(models.Model):
    shipment_number = models.CharField(max_length=10, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    load_point_code = models.CharField(max_length=10, blank=True)
    discharge_point_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_stages'

class KSSapTodTdd(models.Model):
    fund_number = models.CharField(max_length=10, blank=True)
    donor_code = models.CharField(max_length=10, blank=True)
    applctn = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sap_tod_tdd'

class KSSectors(models.Model):
    country_code = models.CharField(max_length=3, blank=True)
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sectors'

class KSSiDetails(models.Model):
    si_record_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_si_details'

class KSSiToProjects(models.Model):
    si_record_id = models.CharField(max_length=25, blank=True)
    start_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_si_to_projects'

class KSSiToProjectsMt(models.Model):
    si_record_id = models.CharField(max_length=25, blank=True)
    start_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_si_to_projects_mt'

class KSStandardPrivileges(models.Model):
    menu_record_id = models.CharField(max_length=25, blank=True)
    standard_role_code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_standard_privileges'

class KSStandardRoles(models.Model):
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_standard_roles'

class KSStockTrans(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    record_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    creation_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_stock_trans'

class KSStoredCommodities(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_stored_commodities'

class KSSubSectors(models.Model):
    country_code = models.CharField(max_length=3, blank=True)
    sector_code = models.CharField(max_length=3, blank=True)
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_sub_sectors'

class KSSuperintendentDetails(models.Model):
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    intcns_code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    quantity_type = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_superintendent_details'

class KSSuppliers(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    code = models.CharField(max_length=4, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_suppliers'

class KSSupplierTypes(models.Model):
    supplier_ouc = models.CharField(max_length=13, blank=True)
    code = models.CharField(max_length=4, blank=True)
    type = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_supplier_types'

class KSSCommodities(models.Model):
    sap_code = models.CharField(max_length=18, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_commodities'

class KSSCommCategories(models.Model):
    sap_code = models.CharField(max_length=18, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_comm_categories'

class KSSCountries(models.Model):
    compas_code = models.CharField(max_length=3, blank=True)
    sap_code_pk = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_countries'

class KSSGeoPoints(models.Model):
    sap_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_geo_points'

class KSSOrganizations(models.Model):
    sap_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_organizations'

class KSSPackageCodes(models.Model):
    sap_code = models.CharField(max_length=17, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_package_codes'

class KSSPrjtypeCountries(models.Model):
    sap_prj_type_code = models.CharField(max_length=2, blank=True)
    sap_countries_code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_prjtype_countries'

class KSSPrjTypes(models.Model):
    sap_prj_type_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_prj_types'

class KSSProjects(models.Model):
    sap_code = models.CharField(max_length=7, blank=True)
    sap_wbs_element = models.CharField(max_length=24, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_projects'

class KSSRbs(models.Model):
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_rbs'

class KSSRrNumbers(models.Model):
    rr_number = models.CharField(max_length=10, blank=True)
    rr_line_number = models.CharField(max_length=5, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_rr_numbers'

class KSSSiNumbers(models.Model):
    new_si_number = models.CharField(max_length=8, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_si_numbers'

class KSSSuppliers(models.Model):
    sap_code = models.CharField(max_length=10, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'k$_s_suppliers'

class KSSSupplierTypes(models.Model):
    sap_code = models.CharField(max_length=10, blank=True)
    sap_supplier_type = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u'k$_s_supplier_types'

class KSSVoyageNumbers(models.Model):
    shipment_number = models.CharField(max_length=10, blank=True)
    voyage_number = models.CharField(max_length=7, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_s_voyage_numbers'

class KSTpoDetails(models.Model):
    tpo_id = models.CharField(max_length=25, blank=True)
    tpo_line_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_tpo_details'

class KSTpoMasters(models.Model):
    tpo_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_tpo_masters'

class KSTrailerDetails(models.Model):
    nmbtrl_id = models.CharField(max_length=20, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'k$_trailer_details'

class KSTransaTypes(models.Model):
    code = models.CharField(max_length=4, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_transa_types'

class KSTransformations(models.Model):
    trnsfr_id = models.CharField(max_length=25)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_transformations'

class KSTranslatedLabels(models.Model):
    lbl_record_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    language_code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_translated_labels'

class KSTransportModes(models.Model):
    code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_transport_modes'

class KSTransDamages(models.Model):
    receipt_code = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    damage_code = models.CharField(max_length=25, blank=True)
    damage_record_id = models.CharField(max_length=25, blank=True)
    damage_cause_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    damage_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_trans_damages'

class KSTransLosses(models.Model):
    trnloss_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_trans_losses'

class KSTPurchaseTypes(models.Model):
    compas_code = models.CharField(max_length=1, blank=True)
    sap_code = models.CharField(max_length=4)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_purchase_types'

class KSTReleaseCodes(models.Model):
    release_type = models.CharField(max_length=2, blank=True)
    code = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_release_codes'

class KSTShipmentStatus(models.Model):
    code = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_shipment_status'

class KSTShippingAreas(models.Model):
    code = models.CharField(max_length=8)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_shipping_areas'

class KSTShippingTypes(models.Model):
    code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_shipping_types'

class KSTSupplierTypes(models.Model):
    sap_code = models.CharField(max_length=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_t_supplier_types'

class KSUpstreamAss(models.Model):
    upsass_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_upstream_ass'

class KSVehicleDetails(models.Model):
    nmbplt_id = models.CharField(max_length=20, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_vehicle_details'

class KSVesselDischarges(models.Model):
    discharge_id = models.CharField(max_length=25, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_vessel_discharges'

class KSVWbsStructure(models.Model):
    pr_pa_num = models.CharField(max_length=7, blank=True)
    cp_pa_num = models.CharField(max_length=7, blank=True)
    sap_num = models.CharField(max_length=7, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_v_wbs_structure'

class KSWarehouseDamages(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    damage_code = models.CharField(max_length=25, blank=True)
    damage_record_id = models.CharField(max_length=25, blank=True)
    damage_cause_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    damage_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_warehouse_damages'

class KSWarehouseLosses(models.Model):
    org_unit_code = models.CharField(max_length=13, blank=True)
    origin_id = models.CharField(max_length=23, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(max_length=1, blank=True)
    loss_code = models.CharField(max_length=25, blank=True)
    loss_record_id = models.CharField(max_length=25, blank=True)
    loss_cause_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    loss_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_warehouse_losses'

class KSWisBooking2(models.Model):
    voyage_id = models.CharField(max_length=7, blank=True)
    si_num = models.CharField(max_length=7, blank=True)
    load_pnt_cde = models.CharField(max_length=3, blank=True)
    dschrg_pnt_cde = models.CharField(max_length=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'k$_wis_booking2'

class LoanDetails(models.Model):
    lonmst_id = models.CharField(unique=True, max_length=25)
    londtl_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    sending_gp_code = models.CharField(unique=True, max_length=10)
    sending_wh_code = models.CharField(unique=True, max_length=13, blank=True)
    si_record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    receiving_wbs_element = models.CharField(max_length=24)
    receiving_si_id = models.CharField(max_length=25)
    receiving_origin_id = models.CharField(max_length=25)
    repaying_origin_id = models.CharField(max_length=25)
    delete_user_id = models.CharField(unique=True, max_length=25, blank=True)
    delete_ouc = models.CharField(unique=True, max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'loan_details'

class LoanMasters(models.Model):
    lonmst_id = models.CharField(unique=True, max_length=25)
    loan_code = models.CharField(unique=True, max_length=25)
    loan_date = models.DateField()
    loan_type = models.CharField(max_length=1)
    expected_closure_date = models.DateField()
    actual_closure_date = models.DateField(null=True, blank=True)
    loaning_org_id = models.CharField(max_length=12)
    loaning_person_code = models.CharField(max_length=7)
    loaning_person_ouc = models.CharField(max_length=13)
    repaying_org_id = models.CharField(max_length=12)
    repaying_person_code = models.CharField(max_length=7)
    repaying_person_ouc = models.CharField(max_length=13)
    terms_and_conditions = models.CharField(max_length=250, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'loan_masters'

class LocalCurrency(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    currency = models.CharField(unique=True, max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'local_currency'

class LossDamageCauses(models.Model):
    name_record_id = models.CharField(unique=True, max_length=25)
    record_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    code = models.CharField(unique=True, max_length=4)
    cause = models.CharField(unique=True, max_length=100)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'loss_damage_causes'

class LossDamageNames(models.Model):
    record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(unique=True, max_length=9)
    type = models.CharField(unique=True, max_length=1)
    nature = models.CharField(unique=True, max_length=100)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'loss_damage_names'

class LtiDetails(models.Model):
    lti_id = models.CharField(unique=True, max_length=25)
    si_record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'lti_details'

class LtiFormItems(models.Model):
    item_record_id = models.CharField(unique=True, max_length=25)
    lti_id = models.CharField(unique=True, max_length=25)
    item_value = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'lti_form_items'

class LtiMasters(models.Model):
    lti_id = models.CharField(unique=True, max_length=25)
    code = models.CharField(unique=True, max_length=25)
    lti_date = models.DateField()
    contract_code = models.CharField(max_length=20, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    origin_type = models.CharField(max_length=1)
    origin_location_code = models.CharField(max_length=10)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    organization_id = models.CharField(max_length=12)
    requested_dispatch_date = models.DateField(null=True, blank=True)
    inspection_indicator = models.CharField(max_length=1, blank=True)
    officer_code = models.CharField(max_length=7)
    person2_ouc = models.CharField(max_length=13)
    title_of_officer = models.CharField(max_length=50, blank=True)
    issuing_code = models.CharField(max_length=7)
    person1_ouc = models.CharField(max_length=13)
    title_of_issuing = models.CharField(max_length=50, blank=True)
    transporter_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    transport_rate_type = models.CharField(max_length=10, blank=True)
    transport_currency = models.CharField(max_length=3, blank=True)
    transport_rate = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_entitlement = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_rate = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    fuel_currency = models.CharField(max_length=3, blank=True)
    food_release = models.CharField(max_length=6, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    remarks_b = models.CharField(max_length=250, blank=True)
    observations = models.CharField(max_length=250, blank=True)
    status_indicator = models.CharField(max_length=1)
    org_unit_code = models.CharField(max_length=13)
    printed_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'lti_masters'

class MemoInvoices(models.Model):
    memo_number = models.CharField(unique=True, max_length=25)
    memo_date = models.DateField(unique=True)
    invoice_id = models.CharField(unique=True, max_length=25)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'memo_invoices'

class MemoInvoicesBck(models.Model):
    memo_number = models.CharField(max_length=25)
    memo_date = models.DateField()
    invoice_id = models.CharField(max_length=25)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'memo_invoices_bck'

class MenuItems(models.Model):
    menu_record_id = models.CharField(unique=True, max_length=25)
    description = models.CharField(max_length=200)
    role_create_name = models.CharField(max_length=10)
    role_edit_name = models.CharField(max_length=10)
    role_view_name = models.CharField(max_length=10)
    menu_parent = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    display_order = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    prgname_create = models.CharField(max_length=80, blank=True)
    prgtitle_create = models.CharField(max_length=200, blank=True)
    prgmode_create = models.CharField(max_length=1, blank=True)
    prgwhere_create = models.CharField(max_length=200, blank=True)
    prgcallprg_create = models.CharField(max_length=10, blank=True)
    prgcallproc_create = models.CharField(max_length=20, blank=True)
    prgname_edit = models.CharField(max_length=80, blank=True)
    prgtitle_edit = models.CharField(max_length=200, blank=True)
    prgmode_edit = models.CharField(max_length=1, blank=True)
    prgwhere_edit = models.CharField(max_length=200, blank=True)
    prgcallprg_edit = models.CharField(max_length=10, blank=True)
    prgcallproc_edit = models.CharField(max_length=20, blank=True)
    prgname_view = models.CharField(max_length=80, blank=True)
    prgtitle_view = models.CharField(max_length=200, blank=True)
    prgmode_view = models.CharField(max_length=1, blank=True)
    prgwhere_view = models.CharField(max_length=200, blank=True)
    prgcallprg_view = models.CharField(max_length=10, blank=True)
    prgcallproc_view = models.CharField(max_length=20, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    menu_state = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    menu_child = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'menu_items'

class Modules(models.Model):
    module_code = models.CharField(unique=True, max_length=2)
    module_description = models.CharField(max_length=100)
    module_program = models.CharField(max_length=15)
    file_name = models.CharField(max_length=8)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'modules'

class MvLtiStatus(models.Model):
    lti_id = models.CharField(max_length=25)
    si_record_id = models.CharField(max_length=25)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    lti_qty_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    lti_qty_gross = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    dsp_qty_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    dsp_qty_gross = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvg_qty_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvg_qty_gross = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvd_qty_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvd_qty_gross = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvl_qty_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvl_qty_gross = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_refresh = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'mv_lti_status'

class MvOrgUnits(models.Model):
    code = models.CharField(max_length=13)
    name = models.CharField(max_length=50, blank=True)
    reporting_code = models.CharField(max_length=13, blank=True)
    geo_point_code = models.CharField(max_length=4, blank=True)
    last_refresh = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'mv_org_units'

class MvSiqtyarr(models.Model):
    discharge_point_code = models.CharField(max_length=10, blank=True)
    dsc_point_name = models.CharField(max_length=30, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    si_record_id = models.CharField(max_length=25, blank=True)
    tot_arr_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    tot_lossdsc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    tot_dsc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    label1 = models.CharField(max_length=10, blank=True)
    ata_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'mv_siqtyarr'

class MvSiqtymov(models.Model):
    si_record_id = models.CharField(max_length=25, blank=True)
    origin_location_code = models.CharField(max_length=13, blank=True)
    origin_name = models.CharField(max_length=30)
    destination_location_code = models.CharField(max_length=10, blank=True)
    destination_name = models.CharField(max_length=30)
    allocation_destination_code = models.CharField(max_length=10, blank=True)
    allocation_name = models.CharField(max_length=50, blank=True)
    transaction_type = models.CharField(max_length=25, blank=True)
    tot_dsp_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    tot_rcv_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    tot_dmg_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    tot_loss_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'mv_siqtymov'

class MvSiqtystock(models.Model):
    si_record_id = models.CharField(max_length=25, blank=True)
    allocation_name = models.CharField(max_length=50, blank=True)
    code = models.CharField(max_length=10, blank=True)
    location_name = models.CharField(max_length=30, blank=True)
    location_code = models.CharField(max_length=10, blank=True)
    intstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rcvstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    dspstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    ingdstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    indmstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    inspstc_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'mv_siqtystock'

class Notifications(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    notify_number = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    notify_date = models.DateField(unique=True)
    notify_type = models.CharField(max_length=3)
    notify_priority = models.CharField(max_length=1, blank=True)
    notify_hint = models.CharField(max_length=80, blank=True)
    notify_text = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'notifications'

class NotifyStatus(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    notify_number = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    notify_date = models.DateField(unique=True)
    compas_username = models.CharField(unique=True, max_length=30)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'notify_status'

class Organizations(models.Model):
    short_name = models.CharField(max_length=12, blank=True)
    name = models.CharField(max_length=80)
    type = models.CharField(max_length=3)
    phone_number = models.CharField(max_length=20, blank=True)
    fax_number = models.CharField(max_length=20, blank=True)
    donor_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    country_code = models.CharField(max_length=3, blank=True)
    class Meta:
        db_table = u'organizations'

class OrgUnits(models.Model):
    code = models.CharField(unique=True, max_length=13)
    name = models.CharField(unique=True, max_length=50, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    fax_number = models.BigIntegerField(null=True, blank=True)
    radio_call_sign = models.CharField(max_length=18, blank=True)
    e_mail_address = models.CharField(max_length=1, blank=True)
    geo_point_code = models.CharField(unique=True, max_length=4, blank=True)
    reporting_code = models.CharField(max_length=13, blank=True)
    ro_rep_net = models.CharField(max_length=13, blank=True)
    organization_id = models.CharField(max_length=12, blank=True)
    compas_indicator = models.CharField(max_length=1)
    total_capacity = models.IntegerField(null=True, blank=True)
    max_file_limit = models.CharField(max_length=4, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=7, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    stock_indicator = models.CharField(max_length=4000, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'org_units'

class OrgUnitTypes(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=7)
    code = models.CharField(unique=True, max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'org_unit_types'

class OtsOverview(models.Model):
    record_id = models.CharField(unique=True, max_length=25)
    project = models.CharField(max_length=7)
    sap_prj_type_code = models.CharField(max_length=2, blank=True)
    rec_ctry_code = models.CharField(max_length=3, blank=True)
    rec_ctry_name = models.CharField(max_length=15, blank=True)
    wbs_element = models.CharField(max_length=24, blank=True)
    od_rb = models.CharField(max_length=4, blank=True)
    donor_organization = models.CharField(max_length=80, blank=True)
    donor_code = models.CharField(max_length=10, blank=True)
    donor_country_code = models.CharField(max_length=3, blank=True)
    donor_country_name = models.CharField(max_length=15, blank=True)
    fund_center = models.CharField(max_length=16, blank=True)
    fund_number = models.CharField(max_length=10, blank=True)
    year = models.CharField(max_length=4, blank=True)
    pledge = models.CharField(max_length=4, blank=True)
    ec_usa = models.CharField(max_length=20, blank=True)
    fund_win_desc = models.CharField(max_length=30, blank=True)
    rr_code = models.CharField(max_length=10, blank=True)
    rr_line = models.CharField(max_length=10, blank=True)
    clc_cik = models.CharField(max_length=4, blank=True)
    pr_code = models.CharField(max_length=10)
    pr_line = models.CharField(max_length=5)
    po_code = models.CharField(max_length=10)
    po_line = models.CharField(max_length=5)
    po_del_flag = models.CharField(max_length=1, blank=True)
    po_qty = models.DecimalField(null=True, max_digits=17, decimal_places=3, blank=True)
    delivery_terms = models.CharField(max_length=3, blank=True)
    po_local_indicator = models.CharField(max_length=1, blank=True)
    si_date = models.DateField(null=True, blank=True)
    si_code = models.CharField(max_length=10, blank=True)
    delivery = models.CharField(max_length=10, blank=True)
    delivery_qty = models.DecimalField(null=True, max_digits=19, decimal_places=3, blank=True)
    commodity = models.CharField(max_length=15, blank=True)
    package = models.CharField(max_length=3, blank=True)
    voyage_type_code = models.CharField(max_length=2, blank=True)
    voyage_type_name = models.CharField(max_length=11, blank=True)
    number_ots_charter = models.CharField(max_length=12, blank=True)
    shipment_number = models.CharField(max_length=10, blank=True)
    vessel_name = models.CharField(max_length=20, blank=True)
    vessel_flag = models.CharField(max_length=10, blank=True)
    net_bl_qty = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    gross_bl_qty = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    bl_date = models.DateField(null=True, blank=True)
    bl_code = models.CharField(max_length=30, blank=True)
    container_flag = models.CharField(max_length=3, blank=True)
    ttl_frt_usd = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    frt_mtn = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    ttl_rate_usd = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    new_indicator = models.CharField(max_length=5, blank=True)
    load_point_code = models.CharField(max_length=10, blank=True)
    load_point_name = models.CharField(max_length=15, blank=True)
    load_region = models.CharField(max_length=15, blank=True)
    discharge_point_code = models.CharField(max_length=10, blank=True)
    discharge_point_name = models.CharField(max_length=28, blank=True)
    discharge_region = models.CharField(max_length=15, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    eta = models.DateField(null=True, blank=True)
    ata = models.DateField(null=True, blank=True)
    document_date = models.DateField(null=True, blank=True)
    cts_ata = models.DateField(null=True, blank=True)
    ata_overdue = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    lp_sa_code = models.CharField(max_length=3, blank=True)
    dp_sa_code = models.CharField(max_length=3, blank=True)
    po_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'ots_overview'

class OverlandArrDetails(models.Model):
    code = models.CharField(unique=True, max_length=25)
    lndarrd_code = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    si_record_id = models.CharField(unique=True, max_length=25)
    delivery_number = models.CharField(unique=True, max_length=10, blank=True)
    load_point_code = models.CharField(max_length=10, blank=True)
    discharge_point_code = models.CharField(max_length=10)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    etd_date = models.DateField(null=True, blank=True)
    atd_date = models.DateField(null=True, blank=True)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField(null=True, blank=True)
    mode_transport_code = models.CharField(max_length=2, blank=True)
    clearing_agent_code = models.CharField(max_length=4, blank=True)
    clearing_agent_ouc = models.CharField(max_length=13, blank=True)
    wis_indicator = models.CharField(max_length=1)
    origin_id = models.CharField(max_length=23, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'overland_arr_details'

class OverlandArrMasters(models.Model):
    code = models.CharField(unique=True, max_length=25)
    document_number = models.CharField(max_length=16, blank=True)
    document_date = models.DateField(null=True, blank=True)
    supplier_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    wis_indicator = models.CharField(max_length=1)
    remarks = models.CharField(max_length=250, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    class Meta:
        db_table = u'overland_arr_masters'

class PackageTypes(models.Model):
    code = models.CharField(unique=True, max_length=17)
    description = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'package_types'

class PaMaster(models.Model):
    wis_code = models.CharField(unique=True, max_length=8)
    short_title = models.CharField(max_length=25, blank=True)
    pa_prj_type = models.CharField(max_length=12, blank=True)
    rcpnt_cntry_cde = models.CharField(max_length=3, blank=True)
    gg_duration = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'pa_master'

class Persons(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    code = models.CharField(unique=True, max_length=7)
    type_of_document = models.CharField(max_length=2, blank=True)
    organization_id = models.CharField(max_length=12)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=25)
    title = models.CharField(max_length=50, blank=True)
    document_number = models.CharField(max_length=25, blank=True)
    e_mail_address = models.CharField(max_length=100, blank=True)
    mobile_phone_number = models.CharField(max_length=20, blank=True)
    official_tel_number = models.CharField(max_length=20, blank=True)
    fax_number = models.CharField(max_length=20, blank=True)
    effective_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    location_code = models.CharField(max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'persons'

class PhysicalInventory(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    storage_code = models.CharField(unique=True, max_length=13)
    si_record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    quality = models.CharField(unique=True, max_length=1)
    date_inventory = models.DateField(unique=True)
    person_ouc = models.CharField(max_length=13)
    person_code = models.CharField(max_length=7)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    old_stock_date = models.DateField()
    old_quality = models.CharField(max_length=1)
    old_quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    old_quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    old_number_of_units = models.IntegerField()
    old_unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    old_unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'physical_inventory'


class PrjOrgUnits(models.Model):
    project_code = models.CharField(unique=True, max_length=8)
    org_unit_code = models.CharField(unique=True, max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'prj_org_units'

class ProgramName(models.Model):
    program_name = models.CharField(unique=True, max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'program_name'

class Projects(models.Model):
    code = models.CharField(unique=True, max_length=8)
    title = models.CharField(max_length=40, blank=True)
    type = models.CharField(max_length=40)
    country_code = models.CharField(max_length=3)
    approval_date = models.DateField(null=True, blank=True)
    estimated_duration_days = models.IntegerField(null=True, blank=True)
    closed_date = models.DateField(null=True, blank=True)
    wfp_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'projects'

class ProActivities(models.Model):
    code = models.CharField(unique=True, max_length=6)
    org_unit_code = models.CharField(unique=True, max_length=13)
    wfp_code = models.CharField(max_length=15)
    description = models.CharField(max_length=50)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'pro_activities'

class Prps(models.Model):
    mandt = models.CharField(max_length=3)
    pspnr = models.CharField(max_length=8)
    posid = models.CharField(max_length=24)
    post1 = models.CharField(max_length=40)
    objnr = models.CharField(max_length=22)
    psphi = models.CharField(max_length=8)
    poski = models.CharField(max_length=16)
    ernam = models.CharField(max_length=12)
    erdat = models.CharField(max_length=8)
    aenam = models.CharField(max_length=12)
    aedat = models.CharField(max_length=8)
    vernr = models.CharField(max_length=8)
    verna = models.CharField(max_length=25)
    astnr = models.CharField(max_length=8)
    astna = models.CharField(max_length=25)
    pbukr = models.CharField(max_length=4)
    pgsbr = models.CharField(max_length=4)
    pkokr = models.CharField(max_length=4)
    prctr = models.CharField(max_length=10)
    prart = models.CharField(max_length=2)
    stufe = models.IntegerField()
    plakz = models.CharField(max_length=1)
    belkz = models.CharField(max_length=1)
    fakkz = models.CharField(max_length=1)
    npfaz = models.CharField(max_length=1)
    zuord = models.CharField(max_length=1)
    trmeq = models.CharField(max_length=1)
    kvewe = models.CharField(max_length=1)
    kappl = models.CharField(max_length=2)
    kalsm = models.CharField(max_length=6)
    zschl = models.CharField(max_length=6)
    abgsl = models.CharField(max_length=6)
    akokr = models.CharField(max_length=4)
    akstl = models.CharField(max_length=10)
    fkokr = models.CharField(max_length=4)
    fkstl = models.CharField(max_length=10)
    fabkl = models.CharField(max_length=2)
    pspri = models.CharField(max_length=1)
    equnr = models.CharField(max_length=18)
    tplnr = models.CharField(max_length=30)
    pwpos = models.CharField(max_length=5)
    werks = models.CharField(max_length=4)
    txtsp = models.CharField(max_length=1)
    slwid = models.CharField(max_length=7)
    usr00 = models.CharField(max_length=20)
    usr01 = models.CharField(max_length=20)
    usr02 = models.CharField(max_length=10)
    usr03 = models.CharField(max_length=10)
    usr04 = models.DecimalField(max_digits=13, decimal_places=3)
    use04 = models.CharField(max_length=3)
    usr05 = models.DecimalField(max_digits=13, decimal_places=3)
    use05 = models.CharField(max_length=3)
    usr06 = models.DecimalField(max_digits=13, decimal_places=3)
    use06 = models.CharField(max_length=5)
    usr07 = models.DecimalField(max_digits=13, decimal_places=3)
    use07 = models.CharField(max_length=5)
    usr08 = models.CharField(max_length=8)
    usr09 = models.CharField(max_length=8)
    usr10 = models.CharField(max_length=1)
    usr11 = models.CharField(max_length=1)
    kostl = models.CharField(max_length=10)
    ktrg = models.CharField(max_length=12)
    berst = models.CharField(max_length=16)
    bertr = models.CharField(max_length=16)
    berko = models.CharField(max_length=16)
    berbu = models.CharField(max_length=16)
    clasf = models.CharField(max_length=1)
    spsnr = models.CharField(max_length=8)
    scope = models.CharField(max_length=2)
    xstat = models.CharField(max_length=1)
    txjcd = models.CharField(max_length=15)
    zschm = models.CharField(max_length=7)
    imprf = models.CharField(max_length=6)
    evgew = models.IntegerField()
    aennr = models.CharField(max_length=12)
    subpr = models.CharField(max_length=12)
    postu = models.CharField(max_length=40)
    plint = models.CharField(max_length=1)
    loevm = models.CharField(max_length=1)
    kzbws = models.CharField(max_length=1)
    fplnr = models.CharField(max_length=10)
    tadat = models.CharField(max_length=8)
    izwek = models.CharField(max_length=2)
    isize = models.CharField(max_length=2)
    iumkz = models.CharField(max_length=5)
    abukr = models.CharField(max_length=4)
    grpkz = models.CharField(max_length=1)
    pgprf = models.CharField(max_length=6)
    logsystem = models.CharField(max_length=10)
    stort = models.CharField(max_length=10)
    pspkz = models.CharField(max_length=1)
    matnr = models.CharField(max_length=18)
    vlpsp = models.CharField(max_length=8)
    vlpkz = models.CharField(max_length=1)
    sort1 = models.CharField(max_length=10)
    sort2 = models.CharField(max_length=10)
    sort3 = models.CharField(max_length=10)
    vname = models.CharField(max_length=6)
    recid = models.CharField(max_length=2)
    etype = models.CharField(max_length=3)
    otype = models.CharField(max_length=4)
    jibcl = models.CharField(max_length=3)
    jibsa = models.CharField(max_length=5)
    cgpl_guid16 = models.TextField() # This field type is a guess.
    cgpl_logsys = models.CharField(max_length=10)
    cgpl_objtype = models.CharField(max_length=3)
    class Meta:
        db_table = u'prps'

class RateTypes(models.Model):
    rate_code = models.CharField(unique=True, max_length=10)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'rate_types'

class RcvcstTrntypes(models.Model):
    dsp_record_id = models.CharField(unique=True, max_length=25)
    tran_type_code = models.CharField(unique=True, max_length=4)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'rcvcst_trntypes'

class ReceiptDetails(models.Model):
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_destination_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    unit_weight_net = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    unit_weight_gross = models.DecimalField(null=True, max_digits=8, decimal_places=3, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'receipt_details'

class ReceiptFormItems(models.Model):
    item_record_id = models.CharField(unique=True, max_length=25)
    receipt_code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    item_value = models.CharField(max_length=2000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'receipt_form_items'

class ReceiptMasters(models.Model):
    code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    extra_code = models.CharField(max_length=25, blank=True)
    receipt_location_code = models.CharField(max_length=10)
    receipt_code = models.CharField(max_length=13)
    person_ouc_rec = models.CharField(max_length=13)
    person_code_rec = models.CharField(max_length=7)
    tran_type_code_rec = models.CharField(max_length=4)
    tran_type_descr_rec = models.CharField(max_length=50, blank=True)
    arrival_date = models.DateField()
    start_discharge_date = models.DateField()
    end_discharge_date = models.DateField()
    distance_traveled = models.DecimalField(null=True, max_digits=7, decimal_places=3, blank=True)
    comments_rec = models.CharField(max_length=250, blank=True)
    lti_id = models.CharField(max_length=25, blank=True)
    origin_location_code = models.CharField(max_length=10)
    origin_type = models.CharField(max_length=1)
    intvyg_code = models.CharField(max_length=25, blank=True)
    intdlv_code = models.IntegerField(null=True, blank=True)
    origin_code = models.CharField(max_length=13, blank=True)
    origin_descr = models.CharField(max_length=50, blank=True)
    destination_location_code = models.CharField(max_length=10)
    destination_code = models.CharField(max_length=13, blank=True)
    pro_activity_code = models.CharField(max_length=6, blank=True)
    activity_ouc = models.CharField(max_length=13, blank=True)
    dispatch_date = models.DateField()
    loading_date = models.DateField()
    organization_id = models.CharField(max_length=12)
    tran_type_code = models.CharField(max_length=4)
    tran_type_descr = models.CharField(max_length=50, blank=True)
    lndarrm_code = models.CharField(max_length=25, blank=True)
    modetrans_code = models.CharField(max_length=2)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    certifing_title = models.CharField(max_length=50, blank=True)
    trans_contractor_code = models.CharField(max_length=4)
    supplier1_ouc = models.CharField(max_length=13)
    trans_subcontractor_code = models.CharField(max_length=4, blank=True)
    supplier2_ouc = models.CharField(max_length=13, blank=True)
    nmbplt_id = models.CharField(max_length=25, blank=True)
    nmbtrl_id = models.CharField(max_length=25, blank=True)
    atl_li_code = models.CharField(max_length=8, blank=True)
    driver_name = models.CharField(max_length=50, blank=True)
    vehicle_registration = models.CharField(max_length=20, blank=True)
    license = models.CharField(max_length=20, blank=True)
    trailer_plate = models.CharField(max_length=20, blank=True)
    container_number = models.CharField(max_length=15, blank=True)
    customised = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'receipt_masters'

class Reconstitutions(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    creation_date = models.DateField(unique=True)
    new_package_code = models.CharField(unique=True, max_length=17)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    r_quality = models.CharField(max_length=1, blank=True)
    r_quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    r_quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    r_number_of_units = models.IntegerField(null=True, blank=True)
    l_quality = models.CharField(max_length=1, blank=True)
    l_quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    l_quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    l_number_of_units = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    s_quality = models.CharField(max_length=1, blank=True)
    s_quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    s_quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    s_number_of_units = models.IntegerField(null=True, blank=True)
    person_ouc = models.CharField(max_length=13)
    person_code = models.CharField(max_length=7)
    title = models.CharField(max_length=50, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'reconstitutions'

class Repackings(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    creation_date = models.DateField(unique=True)
    number_of_units = models.IntegerField()
    quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    repacked_package_code = models.CharField(unique=True, max_length=17)
    repacked_number_of_units = models.IntegerField()
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    title = models.CharField(max_length=50, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'repackings'

class RepayDetails(models.Model):
    lonmst_id = models.CharField(max_length=25)
    londtl_id = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    rpydtl_id = models.DecimalField(max_digits=127, decimal_places=127)
    sending_gp_code = models.CharField(unique=True, max_length=10)
    sending_wh_code = models.CharField(unique=True, max_length=13, blank=True)
    si_record_id = models.CharField(unique=True, max_length=25)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    delete_user_id = models.CharField(unique=True, max_length=25, blank=True)
    delete_ouc = models.CharField(unique=True, max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'repay_details'

class SapBlDetails(models.Model):
    shipment_number = models.CharField(unique=True, max_length=10)
    delivery_number = models.CharField(max_length=10)
    load_point_code = models.CharField(unique=True, max_length=10)
    discharge_point_code = models.CharField(unique=True, max_length=10)
    bl_date = models.DateField(unique=True)
    bl_code = models.CharField(unique=True, max_length=30)
    net_metric_tons = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    gross_metric_tons = models.DecimalField(null=True, max_digits=15, decimal_places=3, blank=True)
    container_type = models.CharField(max_length=10, blank=True)
    pallet_number = models.BigIntegerField(null=True, blank=True)
    packaging_number = models.BigIntegerField(null=True, blank=True)
    empty_bag_number = models.BigIntegerField(null=True, blank=True)
    container_number = models.BigIntegerField(null=True, blank=True)
    remark_text = models.CharField(max_length=75, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_bl_details'

class SapDeliveries(models.Model):
    delivery_number = models.CharField(unique=True, max_length=10)
    po_number = models.CharField(max_length=10, blank=True)
    po_line_number = models.CharField(max_length=5, blank=True)
    si_code = models.CharField(max_length=8)
    load_point_code = models.CharField(max_length=10)
    discharge_point_code = models.CharField(max_length=10)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    net_weight_qty = models.DecimalField(null=True, max_digits=19, decimal_places=3, blank=True)
    gross_weight_qty = models.DecimalField(null=True, max_digits=19, decimal_places=3, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_deliveries'

class SapGoodReceipts(models.Model):
    po_number = models.CharField(unique=True, max_length=10)
    po_line_number = models.CharField(unique=True, max_length=5)
    document_date = models.DateField(unique=True)
    document_number = models.CharField(unique=True, max_length=10)
    quantity_net = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    offid = models.CharField(max_length=7, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_good_receipts'

class SapLtshRates(models.Model):
    rate_seqnum = models.CharField(unique=True, max_length=10)
    pr_number = models.CharField(max_length=10, blank=True)
    pr_line_number = models.CharField(max_length=5, blank=True)
    po_number = models.CharField(max_length=10, blank=True)
    po_line_number = models.CharField(max_length=5, blank=True)
    shipment_number = models.CharField(max_length=10, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    ltsh_to_release = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    ltsh_released = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    dsc_to_release = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    dsc_released = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    odoc_to_release = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    odoc_released = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_ltsh_rates'

class SapPrRates(models.Model):
    pr_number = models.CharField(unique=True, max_length=10)
    pr_line_number = models.CharField(unique=True, max_length=5)
    rate_seqnum = models.CharField(unique=True, max_length=3)
    ltsh_fund = models.CharField(max_length=10, blank=True)
    ltsh_rate = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    ltsh_er_amount = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    dsc_fund = models.CharField(max_length=10, blank=True)
    dsc_rate = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    dsc_er_amount = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    odoc_fund = models.CharField(max_length=10, blank=True)
    odoc_rate = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    odoc_er_amount = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_pr_rates'

class SapPurchaseOrders(models.Model):
    po_number = models.CharField(unique=True, max_length=10)
    po_line_number = models.CharField(unique=True, max_length=5)
    pr_number = models.CharField(max_length=10, blank=True)
    pr_line_number = models.CharField(max_length=5, blank=True)
    po_type = models.CharField(max_length=4, blank=True)
    si_code = models.CharField(max_length=8, blank=True)
    si_status = models.CharField(max_length=2, blank=True)
    supplier_code = models.CharField(max_length=10, blank=True)
    donor_code = models.CharField(max_length=10, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(max_length=17, blank=True)
    po_quantity = models.DecimalField(null=True, max_digits=17, decimal_places=3, blank=True)
    recipient_country_code = models.CharField(max_length=3, blank=True)
    delivery_term_code = models.CharField(max_length=3, blank=True)
    delivery_term_descr = models.CharField(max_length=28, blank=True)
    project_code = models.CharField(max_length=7, blank=True)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    po_fund = models.CharField(max_length=10, blank=True)
    fund_donor_code = models.CharField(max_length=10, blank=True)
    release_status = models.CharField(max_length=2, blank=True)
    release_final_indicator = models.CharField(max_length=1, blank=True)
    remarks = models.CharField(max_length=200, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    local_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_purchase_orders'

class SapPurchaseRequisitions(models.Model):
    pr_number = models.CharField(unique=True, max_length=10)
    pr_line_number = models.CharField(unique=True, max_length=5)
    rr_number = models.CharField(max_length=10, blank=True)
    rr_line_number = models.CharField(max_length=5, blank=True)
    pr_type = models.CharField(max_length=4, blank=True)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    pr_quantity = models.DecimalField(null=True, max_digits=17, decimal_places=3, blank=True)
    project_code = models.CharField(max_length=7, blank=True)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    pr_fund = models.CharField(max_length=10, blank=True)
    fund_donor_code = models.CharField(max_length=10, blank=True)
    release_status = models.CharField(max_length=2, blank=True)
    release_final_indicator = models.CharField(max_length=1, blank=True)
    transport_fund = models.CharField(max_length=10, blank=True)
    transport_donor_code = models.CharField(max_length=10, blank=True)
    transport_amount = models.DecimalField(null=True, max_digits=14, decimal_places=3, blank=True)
    delete_indicator = models.CharField(max_length=240, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_purchase_requisitions'

class SapResourceRequests(models.Model):
    rr_number = models.CharField(unique=True, max_length=10)
    rr_line_number = models.CharField(unique=True, max_length=5)
    comm_category_code = models.CharField(max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    rr_quantity = models.DecimalField(null=True, max_digits=17, decimal_places=3, blank=True)
    project_code = models.CharField(max_length=7, blank=True)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    release_status = models.CharField(max_length=2, blank=True)
    release_final_indicator = models.CharField(max_length=1, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_resource_requests'

class SapShipments(models.Model):
    shipment_number = models.CharField(unique=True, max_length=10)
    shipment_type = models.CharField(max_length=4, blank=True)
    shipping_type = models.CharField(max_length=2, blank=True)
    shipment_status = models.CharField(max_length=1, blank=True)
    service_agent_code = models.CharField(max_length=10, blank=True)
    vessel_name = models.CharField(max_length=20, blank=True)
    tpo_number = models.CharField(max_length=10, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    eta_date = models.DateField(null=True, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_shipments'

class SapShpdates(models.Model):
    shipment_number = models.CharField(unique=True, max_length=10)
    load_point_code = models.CharField(unique=True, max_length=10)
    discharge_point_code = models.CharField(unique=True, max_length=10)
    departure_date = models.DateField(null=True, blank=True)
    eta_date = models.DateField(null=True, blank=True)
    ata_date = models.DateField(null=True, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    ata_date_from_cts = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_shpdates'

class SapStages(models.Model):
    shipment_number = models.CharField(unique=True, max_length=10)
    delivery_number = models.CharField(max_length=10)
    load_point_code = models.CharField(max_length=10)
    discharge_point_code = models.CharField(max_length=10)
    last_load_date = models.CharField(max_length=240, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_stages'

class SapTodTdd(models.Model):
    fund_number = models.CharField(max_length=10, blank=True)
    donor_code = models.CharField(unique=True, max_length=10, blank=True)
    applctn = models.CharField(unique=True, max_length=10, blank=True)
    tod_date = models.DateField(null=True, blank=True)
    tod_dsf = models.CharField(max_length=1, blank=True)
    tdd_date = models.DateField(null=True, blank=True)
    tdd_dsf = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sap_tod_tdd'

class Sectors(models.Model):
    country_code = models.CharField(unique=True, max_length=3)
    code = models.CharField(max_length=3)
    short_name = models.CharField(unique=True, max_length=30)
    long_name = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sectors'

class Site(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'site'

class SiDetails(models.Model):
    si_record_id = models.CharField(unique=True, max_length=25)
    si_code = models.CharField(unique=True, max_length=8)
    org_unit_code = models.CharField(unique=True, max_length=13)
    si_type = models.CharField(max_length=1)
    created_date = models.DateField()
    donor_code = models.CharField(max_length=12)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    closed_date = models.DateField(null=True, blank=True)
    rr_number = models.CharField(max_length=10, blank=True)
    rr_line_number = models.CharField(max_length=5, blank=True)
    pr_number = models.CharField(max_length=10, blank=True)
    pr_line_number = models.CharField(max_length=5, blank=True)
    po_number = models.CharField(max_length=10)
    po_line_number = models.CharField(max_length=5)
    po_type = models.CharField(max_length=1)
    po_local = models.CharField(max_length=1)
    si_quantity_net = models.DecimalField(max_digits=17, decimal_places=3)
    delivery_term_code = models.CharField(max_length=3, blank=True)
    delivery_term_descr = models.CharField(max_length=28, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'si_details'

class SiToProjects(models.Model):
    si_record_id = models.CharField(unique=True, max_length=25)
    project_code = models.CharField(max_length=8)
    project_wbs_element = models.CharField(max_length=24, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'si_to_projects'

class SiToProjectsMt(models.Model):
    si_record_id = models.CharField(unique=True, max_length=25)
    start_date = models.DateField(unique=True)
    quantity_net = models.DecimalField(null=True, max_digits=17, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'si_to_projects_mt'

class StandardPrivileges(models.Model):
    menu_record_id = models.CharField(unique=True, max_length=25)
    standard_role_code = models.CharField(unique=True, max_length=3)
    flag_create = models.CharField(max_length=1)
    flag_edit = models.CharField(max_length=1)
    flag_view = models.CharField(max_length=1)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'standard_privileges'

class StandardRoles(models.Model):
    code = models.CharField(unique=True, max_length=3)
    description = models.CharField(max_length=100, blank=True)
    module_code = models.CharField(max_length=2)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'standard_roles'

class StockTrans(models.Model):
    org_unit_code = models.CharField(max_length=13, primary_key=True)
    record_id = models.DecimalField(max_digits=127, decimal_places=127, primary_key=True)
    creation_date = models.DateField(primary_key=True)
    creation_type = models.CharField(max_length=2)
    creation_mode = models.CharField(max_length=1)
    compas_username = models.CharField(max_length=30)
    programm_name = models.CharField(max_length=64)
    storage_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    discharge_id = models.CharField(max_length=25, blank=True)
    document_number = models.CharField(max_length=25, blank=True)
    document_code = models.CharField(max_length=2, blank=True)
    receiving_code = models.CharField(max_length=13, blank=True)
    transaction_ouc = models.CharField(max_length=13, blank=True)
    transaction_date = models.DateField(null=True, blank=True)
    transaction_id = models.IntegerField(null=True, blank=True)
    loss_damage_code = models.CharField(max_length=25, blank=True)
    new_package_code = models.CharField(max_length=17, blank=True)
    transformation_type = models.CharField(max_length=1, blank=True)
    state = models.CharField(max_length=1, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'stock_trans'

class StoredCommodities(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'stored_commodities'

class StoredCommodities15072004(models.Model):
    org_unit_code = models.CharField(max_length=13)
    origin_id = models.CharField(max_length=23)
    comm_category_code = models.CharField(max_length=9)
    commodity_code = models.CharField(max_length=18)
    package_code = models.CharField(max_length=17)
    allocation_code = models.CharField(max_length=10)
    quality = models.CharField(max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'stored_commodities_15072004'

class SubSectors(models.Model):
    country_code = models.CharField(unique=True, max_length=3)
    sector_code = models.CharField(unique=True, max_length=3)
    code = models.CharField(unique=True, max_length=3)
    short_name = models.CharField(unique=True, max_length=30)
    long_name = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'sub_sectors'

class SuperintendentDetails(models.Model):
    intvyg_code = models.CharField(unique=True, max_length=25)
    intdlv_code = models.IntegerField(unique=True)
    intcns_code = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    quantity_type = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'superintendent_details'

class Suppliers(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    code = models.CharField(unique=True, max_length=4)
    name = models.CharField(unique=True, max_length=30)
    country_code = models.CharField(max_length=3)
    city_code = models.CharField(max_length=10, blank=True)
    address_line_1 = models.CharField(max_length=30, blank=True)
    address_line_2 = models.CharField(max_length=30, blank=True)
    address_line_3 = models.CharField(max_length=30, blank=True)
    address_line_4 = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    telephone_number = models.CharField(max_length=20, blank=True)
    fax_number = models.CharField(max_length=20, blank=True)
    telegram_number = models.CharField(max_length=20, blank=True)
    telex_number = models.CharField(max_length=15, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'suppliers'

class SupplierTypes(models.Model):
    code = models.CharField(unique=True, max_length=4)
    supplier_ouc = models.CharField(unique=True, max_length=13)
    type = models.CharField(unique=True, max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'supplier_types'

class SCommodities(models.Model):
    compas_cat_code = models.CharField(max_length=9, blank=True)
    compas_code = models.CharField(max_length=18, blank=True)
    sap_cat_code = models.CharField(max_length=9)
    sap_code = models.CharField(max_length=18, primary_key=True)
    sap_description = models.CharField(max_length=40)
    sap_delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_commodities'

class SCommCategories(models.Model):
    compas_code = models.CharField(max_length=9, blank=True)
    sap_code = models.CharField(max_length=9, primary_key=True)
    sap_name = models.CharField(max_length=60, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_comm_categories'

class SCountries(models.Model):
    compas_code = models.CharField(max_length=3, blank=True)
    sap_code_pk = models.CharField(max_length=3, primary_key=True)
    sap_iso_code = models.CharField(max_length=2, blank=True)
    sap_name = models.CharField(max_length=15)
    donor_indicator = models.CharField(max_length=1, blank=True)
    rb_code = models.CharField(max_length=4, blank=True)
    last_load_date = models.DateField()
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_countries'

class SGeoPoints(models.Model):
    compas_code = models.CharField(max_length=10)
    sap_code = models.CharField(unique=True, max_length=10)
    sap_name = models.CharField(max_length=30)
    sap_port_indicator = models.CharField(max_length=1, blank=True)
    sap_country_code = models.CharField(max_length=3)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_geo_points'

class SGetCountry(models.Model):
    sap_code = models.CharField(max_length=10, primary_key=True)
    compas_country_code = models.CharField(max_length=3)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_get_country'

class SOrganizations(models.Model):
    compas_id = models.CharField(max_length=12, blank=True)
    sap_code = models.CharField(unique=True, max_length=10)
    sap_name = models.CharField(max_length=80)
    sap_country_code = models.CharField(max_length=3)
    sap_type = models.CharField(max_length=4, blank=True)
    sap_donor_indicator = models.CharField(max_length=1, blank=True)
    sap_delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_organizations'

class SPackageCodes(models.Model):
    compas_code = models.CharField(max_length=17, blank=True)
    sap_code = models.CharField(max_length=17, primary_key=True)
    sap_name = models.CharField(max_length=40, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_package_codes'

class SPrjtypeCountries(models.Model):
    sap_prj_type_code = models.CharField(unique=True, max_length=2)
    sap_prj_type_desc = models.CharField(max_length=40, blank=True)
    sap_country_code = models.CharField(unique=True, max_length=3)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_prjtype_countries'

class SPrjTypes(models.Model):
    sap_prj_type_code = models.CharField(max_length=2, primary_key=True)
    sap_prj_type_desc = models.CharField(max_length=40, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_prj_types'

class SProjects(models.Model):
    compas_code = models.CharField(max_length=8, blank=True)
    sap_code = models.CharField(unique=True, max_length=7)
    sap_wbs_element = models.CharField(unique=True, max_length=24, blank=True)
    sap_prj_type_code = models.CharField(max_length=2, blank=True)
    sap_prj_type_desc = models.CharField(max_length=40, blank=True)
    sap_prj_title = models.CharField(max_length=40, blank=True)
    sap_country_code = models.CharField(max_length=3, blank=True)
    sap_approval_date = models.DateField(null=True, blank=True)
    sap_delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_projects'

class SRbs(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    descr = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_rbs'

class SRrNumbers(models.Model):
    rr_number = models.CharField(max_length=10, primary_key=True)
    risi_sub_line = models.CharField(max_length=10, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    rr_line_number = models.CharField(max_length=5, primary_key=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_rr_numbers'

class SSiNumbers(models.Model):
    new_si_number = models.CharField(max_length=8, primary_key=True)
    old_si_number = models.CharField(max_length=7, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_si_numbers'

class SSuppliers(models.Model):
    compas_code = models.CharField(max_length=4, blank=True)
    compas_ouc_code = models.CharField(max_length=13, blank=True)
    sap_code = models.CharField(max_length=10, primary_key=True)
    sap_name = models.CharField(max_length=40)
    sap_country_code = models.CharField(max_length=3, blank=True)
    sap_city = models.CharField(max_length=35, blank=True)
    sap_postal_code = models.CharField(max_length=10, blank=True)
    sap_address_line_1 = models.CharField(max_length=35, blank=True)
    sap_address_line_2 = models.CharField(max_length=40, blank=True)
    sap_address_line_3 = models.CharField(max_length=40, blank=True)
    sap_address_line_4 = models.CharField(max_length=40, blank=True)
    sap_telephone_n = models.CharField(max_length=16, blank=True)
    sap_fax_n = models.CharField(max_length=31, blank=True)
    sap_telefax_n = models.CharField(max_length=30, blank=True)
    sap_telex_n = models.CharField(max_length=30, blank=True)
    sap_delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_suppliers'

class SSupplierTypes(models.Model):
    sap_code = models.CharField(max_length=10, primary_key=True)
    sap_supplier_type = models.CharField(max_length=2, primary_key=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u's_supplier_types'

class SVoyageNumbers(models.Model):
    shipment_number = models.CharField(unique=True, max_length=10, blank=True)
    voyage_number = models.CharField(unique=True, max_length=7, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u's_voyage_numbers'

class TpoDetails(models.Model):
    tpo_id = models.CharField(max_length=25, primary_key=True)
    tpo_line_id = models.DecimalField(max_digits=127, decimal_places=127, primary_key=True)
    mandt = models.CharField(unique=True, max_length=3)
    po_number = models.CharField(unique=True, max_length=10)
    po_line_number = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    net_price = models.DecimalField(null=True, max_digits=11, decimal_places=2, blank=True)
    delivery_number = models.CharField(max_length=10, blank=True)
    final_invoice = models.CharField(max_length=1, blank=True)
    delivery_completed = models.CharField(max_length=1, blank=True)
    changed_date = models.DateField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True)
    delete_indicator = models.CharField(max_length=1, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'tpo_details'

class TpoMasters(models.Model):
    tpo_id = models.CharField(max_length=25, primary_key=True)
    mandt = models.CharField(max_length=3)
    po_number = models.CharField(unique=True, max_length=10)
    lti_id = models.CharField(max_length=25, blank=True)
    document_type = models.CharField(max_length=4, blank=True)
    document_date = models.DateField(null=True, blank=True)
    vendor_code = models.CharField(max_length=10, blank=True)
    vendor_ouc = models.CharField(max_length=13, blank=True)
    release_indicator = models.CharField(max_length=1, blank=True)
    release_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=5, blank=True)
    delivery_term_code = models.CharField(max_length=3, blank=True)
    delivery_term_descr = models.CharField(max_length=10, blank=True)
    purchasing_org = models.CharField(max_length=4, blank=True)
    purchasing_group = models.CharField(max_length=3, blank=True)
    last_load_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'tpo_masters'

class TrailerDetails(models.Model):
    nmbtrl_id = models.CharField(max_length=20, primary_key=True)
    supplier_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    plate_number = models.CharField(max_length=20)
    fleet_number = models.CharField(max_length=20, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'trailer_details'

class TransaTypes(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    type = models.CharField(max_length=2)
    short_description = models.CharField(max_length=25)
    long_description = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'transa_types'

class Transformations(models.Model):
    trnsfr_id = models.CharField(max_length=25, primary_key=True)
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    transformation_type = models.CharField(unique=True, max_length=1)
    creation_date = models.DateField(unique=True)
    old_quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    old_quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    old_number_of_units = models.IntegerField()
    new_comm_category_code = models.CharField(max_length=9)
    new_commodity_code = models.CharField(max_length=18)
    new_package_code = models.CharField(max_length=17)
    new_quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    new_quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    new_number_of_units = models.IntegerField()
    lost_quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    lost_quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    lost_number_of_units = models.IntegerField(null=True, blank=True)
    transformation_factor = models.DecimalField(max_digits=11, decimal_places=3)
    transf_facility_code = models.CharField(max_length=13, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    title = models.CharField(max_length=50, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'transformations'

class TranslatedLabels(models.Model):
    lbl_record_id = models.DecimalField(max_digits=127, decimal_places=127, primary_key=True)
    language_code = models.CharField(max_length=3, primary_key=True)
    translate_text = models.CharField(max_length=200)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'translated_labels'

class TransportModes(models.Model):
    code = models.CharField(unique=True, max_length=2)
    description = models.CharField(max_length=50)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'transport_modes'

class TransDamages(models.Model):
    receipt_code = models.CharField(unique=True, max_length=25)
    document_code = models.CharField(unique=True, max_length=2)
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    package_code = models.CharField(unique=True, max_length=17)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    damage_code = models.CharField(unique=True, max_length=25)
    damage_record_id = models.CharField(unique=True, max_length=25, blank=True)
    damage_cause_id = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    damage_date = models.DateField(unique=True)
    quantity_net = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    quantity_gross = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    number_units = models.IntegerField(null=True, blank=True)
    remarks = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7, blank=True)
    person_ouc = models.CharField(max_length=13, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'trans_damages'

class TransLosses(models.Model):
    trnloss_id = models.CharField(max_length=25, primary_key=True)
    intvyg_code = models.CharField(unique=True, max_length=25, blank=True)
    intdlv_code = models.IntegerField(unique=True, null=True, blank=True)
    intcns_code = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    receipt_code = models.CharField(unique=True, max_length=25, blank=True)
    document_code = models.CharField(unique=True, max_length=2, blank=True)
    org_unit_code = models.CharField(unique=True, max_length=13, blank=True)
    origin_id = models.CharField(unique=True, max_length=23, blank=True)
    comm_category_code = models.CharField(unique=True, max_length=9, blank=True)
    commodity_code = models.CharField(max_length=18, blank=True)
    package_code = models.CharField(unique=True, max_length=17, blank=True)
    allocation_code = models.CharField(max_length=10, blank=True)
    quality = models.CharField(unique=True, max_length=1, blank=True)
    loss_code = models.CharField(unique=True, max_length=25)
    loss_record_id = models.CharField(unique=True, max_length=25, blank=True)
    loss_cause_id = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    loss_date = models.DateField(unique=True)
    loss_type = models.CharField(max_length=5)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_units = models.IntegerField()
    remarks = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    lonmst_id = models.CharField(max_length=25, blank=True)
    londtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    rpydtl_id = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    class Meta:
        db_table = u'trans_losses'

class TPurchaseTypes(models.Model):
    compas_code = models.CharField(max_length=1, primary_key=True)
    sap_code = models.CharField(max_length=4, primary_key=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u't_purchase_types'

class TReleaseCodes(models.Model):
    release_type = models.CharField(max_length=2, primary_key=True)
    code = models.CharField(max_length=3, primary_key=True)
    description = models.CharField(max_length=100)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u't_release_codes'

class TShipmentStatus(models.Model):
    code = models.CharField(max_length=1, primary_key=True)
    description = models.CharField(max_length=100)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u't_shipment_status'

class TShippingAreas(models.Model):
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=30, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u't_shipping_areas'

class TShippingTypes(models.Model):
    code = models.CharField(max_length=2, primary_key=True)
    description = models.CharField(max_length=100)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u't_shipping_types'

class TSupplierTypes(models.Model):
    compas_code = models.CharField(max_length=4)
    sap_code = models.CharField(max_length=2, primary_key=True)
    last_load_date = models.DateField(null=True, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    class Meta:
        db_table = u't_supplier_types'

class UpstreamAss(models.Model):
    upsass_id = models.CharField(max_length=25, primary_key=True)
    intvyg_code = models.CharField(unique=True, max_length=25, blank=True)
    intdlv_code = models.IntegerField(unique=True, null=True, blank=True)
    intcns_code = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    lndarrm_code = models.CharField(unique=True, max_length=25, blank=True)
    lndarrd_code = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    allocation_code = models.CharField(unique=True, max_length=10)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    org_unit_code = models.CharField(max_length=13)
    remarks = models.CharField(max_length=250, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'upstream_ass'

class V1V2Commodities(models.Model):
    v1_cat_code = models.CharField(max_length=3)
    v1_commodity_code = models.CharField(max_length=12)
    v2_cat_code = models.CharField(max_length=9)
    v2_commodity_code = models.CharField(max_length=18)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'v1_v2_commodities'

class V1V2Countries(models.Model):
    v1_code = models.CharField(max_length=3)
    v2_code = models.CharField(max_length=3, blank=True)
    class Meta:
        db_table = u'v1_v2_countries'

class VehicleDetails(models.Model):
    nmbplt_id = models.CharField(max_length=25, primary_key=True)
    supplier_code = models.CharField(max_length=4)
    supplier_ouc = models.CharField(max_length=13)
    vehicle_registration = models.CharField(max_length=20)
    fleet_number = models.CharField(max_length=20)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'vehicle_details'

class VesselDischarges(models.Model):
    discharge_id = models.CharField(max_length=25, primary_key=True)
    intvyg_code = models.CharField(unique=True, max_length=25)
    intdlv_code = models.IntegerField(unique=True)
    intcns_code = models.DecimalField(unique=True, max_digits=127, decimal_places=127)
    allocation_code = models.CharField(unique=True, max_length=10)
    discharge_date = models.DateField(unique=True)
    quality = models.CharField(unique=True, max_length=1)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    package_code = models.CharField(unique=True, max_length=17, blank=True)
    unload_to_type = models.CharField(max_length=1, blank=True)
    storage_code = models.CharField(unique=True, max_length=13, blank=True)
    organization_id = models.CharField(unique=True, max_length=12, blank=True)
    forwarding_agent_code = models.CharField(unique=True, max_length=4, blank=True)
    supplier_ouc1 = models.CharField(unique=True, max_length=13, blank=True)
    damage_code = models.CharField(unique=True, max_length=25, blank=True)
    damage_record_id = models.CharField(unique=True, max_length=25, blank=True)
    damage_cause_id = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    org_unit_code = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'vessel_discharges'

class VWbsStructure(models.Model):
    h_level = models.CharField(max_length=3)
    pr_pa_num = models.CharField(unique=True, max_length=7, blank=True)
    cp_pa_num = models.CharField(unique=True, max_length=7, blank=True)
    sap_num = models.CharField(unique=True, max_length=7)
    hierarchy = models.CharField(unique=True, max_length=33, blank=True)
    definition = models.CharField(max_length=7)
    sap_title = models.CharField(max_length=40, blank=True)
    wbs_description = models.CharField(max_length=40, blank=True)
    bdgt_item = models.CharField(max_length=4000, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    recv_pack = models.DecimalField(null=True, max_digits=127, decimal_places=127, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'v_wbs_structure'

class WarehouseDamages(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    damage_code = models.CharField(unique=True, max_length=25, blank=True)
    damage_record_id = models.CharField(unique=True, max_length=25, blank=True)
    damage_cause_id = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    damage_date = models.DateField(unique=True)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    remarks = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'warehouse_damages'

class WarehouseLosses(models.Model):
    org_unit_code = models.CharField(unique=True, max_length=13)
    origin_id = models.CharField(unique=True, max_length=23)
    comm_category_code = models.CharField(unique=True, max_length=9)
    commodity_code = models.CharField(unique=True, max_length=18)
    package_code = models.CharField(unique=True, max_length=17)
    allocation_code = models.CharField(unique=True, max_length=10)
    quality = models.CharField(unique=True, max_length=1)
    loss_code = models.CharField(unique=True, max_length=25)
    loss_record_id = models.CharField(unique=True, max_length=25, blank=True)
    loss_cause_id = models.DecimalField(unique=True, null=True, max_digits=127, decimal_places=127, blank=True)
    loss_date = models.DateField(unique=True)
    loss_type = models.CharField(max_length=5)
    quantity_net = models.DecimalField(max_digits=11, decimal_places=3)
    quantity_gross = models.DecimalField(max_digits=11, decimal_places=3)
    number_of_units = models.IntegerField()
    remarks = models.CharField(max_length=250, blank=True)
    person_code = models.CharField(max_length=7)
    person_ouc = models.CharField(max_length=13)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'warehouse_losses'

class WisBlDetail(models.Model):
    voyage_id = models.CharField(max_length=7, primary_key=True)
    si_num = models.CharField(max_length=7, primary_key=True)
    load_pnt_cde = models.CharField(max_length=3, primary_key=True)
    dschrg_pnt_cde = models.CharField(max_length=3, primary_key=True)
    bill_lading_num = models.CharField(max_length=10, primary_key=True)
    bill_lading_dte = models.DateField(primary_key=True)
    mtg_ldd_qty = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    mtn_ldd_qty = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    number_of_units = models.IntegerField(null=True, blank=True)
    containers_cnt = models.CharField(max_length=10, blank=True)
    remarks_txt_1 = models.CharField(max_length=50, blank=True)
    remarks_txt_2 = models.CharField(max_length=50, blank=True)
    remarks_txt_3 = models.CharField(max_length=50, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_bl_detail'

class WisBooking2(models.Model):
    voyage_id = models.CharField(max_length=7, primary_key=True)
    si_num = models.CharField(max_length=7, primary_key=True)
    load_pnt_cde = models.CharField(max_length=3, primary_key=True)
    dschrg_pnt_cde = models.CharField(max_length=3, primary_key=True)
    crrge_type_cde = models.CharField(max_length=1, blank=True)
    eta_date = models.DateField(null=True, blank=True)
    tot_shipment_qty = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_booking2'

class WisRisiFund(models.Model):
    risi_subline = models.CharField(max_length=10, primary_key=True)
    donor_cde = models.CharField(max_length=3, primary_key=True)
    percentage = models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_risi_fund'

class WisRisiQty(models.Model):
    risi_num = models.CharField(max_length=6, primary_key=True)
    risi_qty = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_risi_qty'

class WisRisiScom(models.Model):
    risi_subline = models.CharField(max_length=10, primary_key=True)
    risi_line = models.CharField(max_length=8, blank=True)
    risi_num = models.CharField(max_length=6, blank=True)
    risi_line_num = models.CharField(max_length=2, blank=True)
    risi_sline_num = models.CharField(max_length=2, blank=True)
    si_num = models.CharField(max_length=7, blank=True)
    si_status_cde = models.CharField(max_length=1, blank=True)
    slne_status_cde = models.CharField(max_length=4, blank=True)
    dlvry_ctry_cde = models.CharField(max_length=3, blank=True)
    project_code = models.CharField(max_length=8, blank=True)
    pur_num = models.CharField(max_length=6, blank=True)
    cmmdty_cat_cde = models.CharField(max_length=3, blank=True)
    cmmdty_cde = models.CharField(max_length=12, blank=True)
    package_cde = models.CharField(max_length=4, blank=True)
    cmmdty_qty = models.DecimalField(null=True, max_digits=11, decimal_places=3, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    rta_date = models.DateField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_risi_scom'

class WisVoyageMast(models.Model):
    voyage_id = models.CharField(max_length=7, primary_key=True)
    voyage_stat_cde = models.CharField(max_length=1, blank=True)
    vessel_nme = models.CharField(max_length=35, blank=True)
    offid = models.CharField(max_length=13, blank=True)
    send_pack = models.BigIntegerField(null=True, blank=True)
    recv_pack = models.BigIntegerField(null=True, blank=True)
    last_mod_user = models.CharField(max_length=30, blank=True)
    last_mod_date = models.DateField(null=True, blank=True)
    class Meta:
        db_table = u'wis_voyage_mast'

###

