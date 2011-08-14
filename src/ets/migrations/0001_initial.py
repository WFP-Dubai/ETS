# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Place'
        db.create_table(u'epic_geo', (
            ('org_code', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('geo_point_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('geo_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('reporting_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
        ))
        db.send_create_signal('ets', ['Place'])

        # Adding model 'Location'
        db.create_table('ets_location', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('compas', self.gf('django.db.models.fields.CharField')(max_length=7)),
        ))
        db.send_create_signal('ets', ['Location'])

        # Adding model 'Consignee'
        db.create_table('ets_consignee', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('ets', ['Consignee'])

        # Adding model 'Warehouse'
        db.create_table('ets_warehouse', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=13, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warehouses', to=orm['ets.Location'])),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='warehouses', null=True, to=orm['ets.Consignee'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ets', ['Warehouse'])

        # Adding model 'CompasPerson'
        db.create_table(u'epic_persons', (
            ('person_pk', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('type_of_document', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('document_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('e_mail_address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('mobile_phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('official_tel_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('fax_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('effective_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('warehouse', self.gf('django.db.models.fields.CharField')(max_length=13, db_column='org_unit_code')),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('location_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('ets', ['CompasPerson'])

        # Adding model 'EpicStock'
        db.create_table(u'epic_stock', (
            ('wh_pk', self.gf('django.db.models.fields.CharField')(max_length=90, primary_key=True)),
            ('wh_regional', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('wh_country', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('wh_location', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('wh_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('wh_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('project_wbs_element', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('cmmname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('package_code', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('packagename', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('qualitycode', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('qualitydescr', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.IntegerField')()),
            ('allocation_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('reference_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('ets', ['EpicStock'])

        # Adding model 'StockItem'
        db.create_table('ets_stockitem', (
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23, primary_key=True)),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stock_items', to=orm['ets.Warehouse'])),
            ('project_number', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('package_code', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('package_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('quality_code', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('quality_description', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.IntegerField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ets', ['StockItem'])

        # Adding model 'PackagingDescriptionShort'
        db.create_table('ets_packagingdescriptionshort', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('ets', ['PackagingDescriptionShort'])

        # Adding model 'LossDamageType'
        db.create_table(u'epic_lossdamagereason', (
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, primary_key=True, unique=True, populate_from=None, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('cause', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('ets', ['LossDamageType'])

        # Adding model 'LtiOriginal'
        db.create_table(u'epic_lti', (
            ('lti_pk', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True, db_column='LTI_PK')),
            ('lti_id', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='LTI_ID')),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='CODE')),
            ('lti_date', self.gf('django.db.models.fields.DateField')(db_column='LTI_DATE')),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='EXPIRY_DATE', blank=True)),
            ('transport_code', self.gf('django.db.models.fields.CharField')(max_length=4, db_column='TRANSPORT_CODE')),
            ('transport_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, db_column='TRANSPORT_OUC')),
            ('transport_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='TRANSPORT_NAME')),
            ('origin_type', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='ORIGIN_TYPE')),
            ('origintype_desc', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='ORIGINTYPE_DESC', blank=True)),
            ('origin_location_code', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='ORIGIN_LOCATION_CODE')),
            ('origin_loc_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='ORIGIN_LOC_NAME')),
            ('origin_wh_code', self.gf('django.db.models.fields.CharField')(max_length=13, db_column='ORIGIN_WH_CODE', blank=True)),
            ('origin_wh_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='ORIGIN_WH_NAME', blank=True)),
            ('destination_location_code', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='DESTINATION_LOCATION_CODE')),
            ('destination_loc_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='DESTINATION_LOC_NAME')),
            ('consegnee_code', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='CONSEGNEE_CODE')),
            ('consegnee_name', self.gf('django.db.models.fields.CharField')(max_length=80, db_column='CONSEGNEE_NAME')),
            ('requested_dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='REQUESTED_DISPATCH_DATE', blank=True)),
            ('project_wbs_element', self.gf('django.db.models.fields.CharField')(max_length=24, db_column='PROJECT_WBS_ELEMENT', blank=True)),
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25, db_column='SI_RECORD_ID', blank=True)),
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8, db_column='SI_CODE')),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9, db_column='COMM_CATEGORY_CODE')),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18, db_column='COMMODITY_CODE')),
            ('cmmname', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='CMMNAME', blank=True)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(db_column='QUANTITY_NET', decimal_places=3, max_digits=11)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(db_column='QUANTITY_GROSS', decimal_places=3, max_digits=11)),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(db_column='NUMBER_OF_UNITS', decimal_places=0, max_digits=7)),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(blank=True, null=True, db_column='UNIT_WEIGHT_NET', decimal_places=3, max_digits=8)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(blank=True, null=True, db_column='UNIT_WEIGHT_GROSS', decimal_places=3, max_digits=8)),
        ))
        db.send_create_signal('ets', ['LtiOriginal'])

        # Adding model 'Order'
        db.create_table('ets_order', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateField')()),
            ('expiry', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transport_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('transport_ouc', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('transport_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('origin_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('project_number', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['ets.Warehouse'])),
            ('consignee', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['ets.Consignee'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['ets.Location'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('ets', ['Order'])

        # Adding model 'OrderItem'
        db.create_table('ets_orderitem', (
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('commodity_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=0)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('lti_pk', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['ets.Order'])),
            ('removed', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('_order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('ets', ['OrderItem'])

        # Adding model 'WaybillAuditLogEntry'
        db.create_table('ets_waybillauditlogentry', (
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None, db_index=True)),
            ('order_code', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('project_number', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('transport_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_auditlog_dispatch_waybills', to=orm['ets.Warehouse'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('loading_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('transport_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dispatch_remarks', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('dispatcher_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_auditlog_dispatch_waybills', to=orm['ets.CompasPerson'])),
            ('transport_sub_contractor', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('transport_driver_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_driver_licence', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_vehicle_registration', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_trailer_registration', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('transport_dispach_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('transport_delivery_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('container_one_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_seal_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_seal_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_remarks_dispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_remarks_dispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_remarks_reciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_remarks_reciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('recipient_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_recipient_waybills', null=True, to=orm['ets.CompasPerson'])),
            ('recipient_arrival_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_start_discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_end_discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_distance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('recipient_remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recipient_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_auditlog_receipt_waybills', to=orm['ets.Warehouse'])),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receipt_validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rec_sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('processed_for_payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audit_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_waybill_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['WaybillAuditLogEntry'])

        # Adding model 'Waybill'
        db.create_table('ets_waybill', (
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, primary_key=True, unique=True, populate_from=None, db_index=True)),
            ('order_code', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('project_number', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('transport_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dispatch_waybills', to=orm['ets.Warehouse'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('loading_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transaction_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('transport_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dispatch_remarks', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('dispatcher_person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dispatch_waybills', to=orm['ets.CompasPerson'])),
            ('transport_sub_contractor', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('transport_driver_name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_driver_licence', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_vehicle_registration', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('transport_trailer_registration', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('transport_dispach_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('transport_delivery_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('container_one_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_seal_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_seal_number', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_remarks_dispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_remarks_dispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_one_remarks_reciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('container_two_remarks_reciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('recipient_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='recipient_waybills', null=True, to=orm['ets.CompasPerson'])),
            ('recipient_arrival_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_start_discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_end_discharge_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipient_distance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('recipient_remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recipient_signed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receipt_waybills', to=orm['ets.Warehouse'])),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receipt_validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('rec_sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('processed_for_payment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('audit_comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('ets', ['Waybill'])

        # Adding model 'LoadingDetailAuditLogEntry'
        db.create_table('ets_loadingdetailauditlogentry', (
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('commodity_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=0)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('waybill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_auditlog_loading_details', to=orm['ets.Waybill'])),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, populate_from=None, db_index=True)),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23)),
            ('package', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('number_units_good', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('number_units_lost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('number_units_damaged', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('units_lost_reason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_lost_reason', null=True, to=orm['ets.LossDamageType'])),
            ('units_damaged_reason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_damage_reason', null=True, to=orm['ets.LossDamageType'])),
            ('units_damaged_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_damage_type', null=True, to=orm['ets.LossDamageType'])),
            ('units_lost_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_loss_type', null=True, to=orm['ets.LossDamageType'])),
            ('overloaded_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loading_detail_sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('over_offload_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_loadingdetail_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['LoadingDetailAuditLogEntry'])

        # Adding model 'LoadingDetail'
        db.create_table('ets_loadingdetail', (
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('commodity_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=0)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('waybill', self.gf('django.db.models.fields.related.ForeignKey')(related_name='loading_details', to=orm['ets.Waybill'])),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=50, primary_key=True, unique=True, populate_from=None, db_index=True)),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23)),
            ('package', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('number_units_good', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('number_units_lost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('number_units_damaged', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('units_lost_reason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='lost_reason', null=True, to=orm['ets.LossDamageType'])),
            ('units_damaged_reason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='damage_reason', null=True, to=orm['ets.LossDamageType'])),
            ('units_damaged_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='damage_type', null=True, to=orm['ets.LossDamageType'])),
            ('units_lost_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='loss_type', null=True, to=orm['ets.LossDamageType'])),
            ('overloaded_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loading_detail_sent_compas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('over_offload_units', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ets', ['LoadingDetail'])

        # Adding model 'UserProfileAuditLogEntry'
        db.create_table('ets_userprofileauditlogentry', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('dispatch_warehouse', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_dispatcher_profiles', null=True, to=orm['ets.Warehouse'])),
            ('reception_warehouse', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_receipient_profiles', null=True, to=orm['ets.Warehouse'])),
            ('is_compas_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_dispatcher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_reciever', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_all_receiver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compas_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_profiles', null=True, to=orm['ets.CompasPerson'])),
            ('super_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reader_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_userprofile_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['UserProfileAuditLogEntry'])

        # Adding model 'UserProfile'
        db.create_table('ets_userprofile', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('dispatch_warehouse', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='dispatcher_profiles', null=True, to=orm['ets.Warehouse'])),
            ('reception_warehouse', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='receipient_profiles', null=True, to=orm['ets.Warehouse'])),
            ('is_compas_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_dispatcher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_reciever', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_all_receiver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compas_person', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profiles', null=True, to=orm['ets.CompasPerson'])),
            ('super_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reader_user', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ets', ['UserProfile'])

        # Adding model 'CompasLogger'
        db.create_table(u'loggercompas', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('errorRec', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('errorDisp', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('wb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Waybill'], primary_key=True)),
            ('lti', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('data_in', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('data_out', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal('ets', ['CompasLogger'])

        # Adding model 'DispatchMaster'
        db.create_table(u'dispatch_masters', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('document_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('dispatch_date', self.gf('django.db.models.fields.DateField')()),
            ('origin_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('origin_location_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('intvyg_code', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('intdlv_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('origin_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('origin_descr', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('destination_location_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('destination_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('pro_activity_code', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('activity_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('lndarrm_code', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('lti_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('loan_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('loading_date', self.gf('django.db.models.fields.DateField')()),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('tran_type_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('tran_type_descr', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('modetrans_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('person_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('person_ouc', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('certifing_title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('trans_contractor_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('supplier1_ouc', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('trans_subcontractor_code', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('supplier2_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('nmbplt_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('nmbtrl_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('driver_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('vehicle_registration', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('trailer_plate', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('container_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('atl_li_code', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('notify_indicator', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('customised', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('printed_indicator', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('notify_org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('offid', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('send_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('recv_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('last_mod_user', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_mod_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('ets', ['DispatchMaster'])

        # Adding model 'DispatchDetail'
        db.create_table(u'dispatch_details', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.DispatchMaster'])),
            ('document_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23, blank=True)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('package_code', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('allocation_destination_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('number_of_units', self.gf('django.db.models.fields.IntegerField')()),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('lonmst_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('londtl_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('rpydtl_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('offid', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('send_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('recv_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('last_mod_user', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_mod_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('ets', ['DispatchDetail'])


    def backwards(self, orm):
        
        # Deleting model 'Place'
        db.delete_table(u'epic_geo')

        # Deleting model 'Location'
        db.delete_table('ets_location')

        # Deleting model 'Consignee'
        db.delete_table('ets_consignee')

        # Deleting model 'Warehouse'
        db.delete_table('ets_warehouse')

        # Deleting model 'CompasPerson'
        db.delete_table(u'epic_persons')

        # Deleting model 'EpicStock'
        db.delete_table(u'epic_stock')

        # Deleting model 'StockItem'
        db.delete_table('ets_stockitem')

        # Deleting model 'PackagingDescriptionShort'
        db.delete_table('ets_packagingdescriptionshort')

        # Deleting model 'LossDamageType'
        db.delete_table(u'epic_lossdamagereason')

        # Deleting model 'LtiOriginal'
        db.delete_table(u'epic_lti')

        # Deleting model 'Order'
        db.delete_table('ets_order')

        # Deleting model 'OrderItem'
        db.delete_table('ets_orderitem')

        # Deleting model 'WaybillAuditLogEntry'
        db.delete_table('ets_waybillauditlogentry')

        # Deleting model 'Waybill'
        db.delete_table('ets_waybill')

        # Deleting model 'LoadingDetailAuditLogEntry'
        db.delete_table('ets_loadingdetailauditlogentry')

        # Deleting model 'LoadingDetail'
        db.delete_table('ets_loadingdetail')

        # Deleting model 'UserProfileAuditLogEntry'
        db.delete_table('ets_userprofileauditlogentry')

        # Deleting model 'UserProfile'
        db.delete_table('ets_userprofile')

        # Deleting model 'CompasLogger'
        db.delete_table(u'loggercompas')

        # Deleting model 'DispatchMaster'
        db.delete_table(u'dispatch_masters')

        # Deleting model 'DispatchDetail'
        db.delete_table(u'dispatch_details')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ets.compaslogger': {
            'Meta': {'object_name': 'CompasLogger', 'db_table': "u'loggercompas'"},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'data_in': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'data_out': ('django.db.models.fields.CharField', [], {'max_length': '5000', 'blank': 'True'}),
            'errorDisp': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'errorRec': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'lti': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'wb': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Waybill']", 'primary_key': 'True'})
        },
        'ets.compasperson': {
            'Meta': {'ordering': "('code',)", 'object_name': 'CompasPerson', 'db_table': "u'epic_persons'"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'document_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'e_mail_address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'effective_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fax_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'location_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'mobile_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'official_tel_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organization_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'person_pk': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type_of_document': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'warehouse': ('django.db.models.fields.CharField', [], {'max_length': '13', 'db_column': "'org_unit_code'"})
        },
        'ets.consignee': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Consignee'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'ets.dispatchdetail': {
            'Meta': {'object_name': 'DispatchDetail', 'db_table': "u'dispatch_details'"},
            'allocation_destination_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.DispatchMaster']"}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'document_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_mod_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_mod_user': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'londtl_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'lonmst_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'number_of_units': ('django.db.models.fields.IntegerField', [], {}),
            'offid': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23', 'blank': 'True'}),
            'package_code': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'quality': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'recv_pack': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'rpydtl_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'send_pack': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'si_record_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'})
        },
        'ets.dispatchmaster': {
            'Meta': {'object_name': 'DispatchMaster', 'db_table': "u'dispatch_masters'"},
            'activity_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'atl_li_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'certifing_title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'comments': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'container_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'customised': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'destination_code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'destination_location_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {}),
            'document_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'driver_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'intdlv_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'intvyg_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'last_mod_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_mod_user': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'lndarrm_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'loading_date': ('django.db.models.fields.DateField', [], {}),
            'loan_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'lti_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'modetrans_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'nmbplt_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'nmbtrl_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'notify_indicator': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'notify_org_unit_code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'offid': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'org_unit_code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'organization_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'origin_code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'origin_descr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'origin_location_code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'origin_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'person_code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'person_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'printed_indicator': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'pro_activity_code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'blank': 'True'}),
            'recv_pack': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'send_pack': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supplier1_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'supplier2_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'trailer_plate': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'tran_type_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'tran_type_descr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'trans_contractor_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'trans_subcontractor_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'ets.epicstock': {
            'Meta': {'object_name': 'EpicStock', 'db_table': "u'epic_stock'"},
            'allocation_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'cmmname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'number_of_units': ('django.db.models.fields.IntegerField', [], {}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'package_code': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'packagename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'project_wbs_element': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'qualitycode': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'qualitydescr': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'reference_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'si_record_id': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'wh_code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'wh_country': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'wh_location': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'wh_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'wh_pk': ('django.db.models.fields.CharField', [], {'max_length': '90', 'primary_key': 'True'}),
            'wh_regional': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        'ets.loadingdetail': {
            'Meta': {'object_name': 'LoadingDetail'},
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'commodity_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'loading_detail_sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '0'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'units_damaged_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'damage_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_damaged_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'damage_type'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lost_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'loss_type'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'waybill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loading_details'", 'to': "orm['ets.Waybill']"})
        },
        'ets.loadingdetailauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'LoadingDetailAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_loadingdetail_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'commodity_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'loading_detail_sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '0'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'units_damaged_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_damage_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_damaged_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_damage_type'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_lost_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_loss_type'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'waybill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_loading_details'", 'to': "orm['ets.Waybill']"})
        },
        'ets.location': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'compas': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ets.lossdamagetype': {
            'Meta': {'object_name': 'LossDamageType', 'db_table': "u'epic_lossdamagereason'"},
            'cause': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'ets.ltioriginal': {
            'Meta': {'object_name': 'LtiOriginal', 'db_table': "u'epic_lti'"},
            'cmmname': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_column': "'CMMNAME'", 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'CODE'"}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_column': "'COMM_CATEGORY_CODE'"}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18', 'db_column': "'COMMODITY_CODE'"}),
            'consegnee_code': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_column': "'CONSEGNEE_CODE'"}),
            'consegnee_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_column': "'CONSEGNEE_NAME'"}),
            'destination_loc_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'DESTINATION_LOC_NAME'"}),
            'destination_location_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'DESTINATION_LOCATION_CODE'"}),
            'expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'EXPIRY_DATE'", 'blank': 'True'}),
            'lti_date': ('django.db.models.fields.DateField', [], {'db_column': "'LTI_DATE'"}),
            'lti_id': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_column': "'LTI_ID'"}),
            'lti_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True', 'db_column': "'LTI_PK'"}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'db_column': "'NUMBER_OF_UNITS'", 'decimal_places': '0', 'max_digits': '7'}),
            'origin_loc_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'ORIGIN_LOC_NAME'"}),
            'origin_location_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_column': "'ORIGIN_LOCATION_CODE'"}),
            'origin_type': ('django.db.models.fields.CharField', [], {'max_length': '1', 'db_column': "'ORIGIN_TYPE'"}),
            'origin_wh_code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'db_column': "'ORIGIN_WH_CODE'", 'blank': 'True'}),
            'origin_wh_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_column': "'ORIGIN_WH_NAME'", 'blank': 'True'}),
            'origintype_desc': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_column': "'ORIGINTYPE_DESC'", 'blank': 'True'}),
            'project_wbs_element': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_column': "'PROJECT_WBS_ELEMENT'", 'blank': 'True'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'db_column': "'QUANTITY_GROSS'", 'decimal_places': '3', 'max_digits': '11'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'db_column': "'QUANTITY_NET'", 'decimal_places': '3', 'max_digits': '11'}),
            'requested_dispatch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'db_column': "'REQUESTED_DISPATCH_DATE'", 'blank': 'True'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'SI_CODE'"}),
            'si_record_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_column': "'SI_RECORD_ID'", 'blank': 'True'}),
            'transport_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'db_column': "'TRANSPORT_CODE'"}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_column': "'TRANSPORT_NAME'"}),
            'transport_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13', 'db_column': "'TRANSPORT_OUC'"}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'null': 'True', 'db_column': "'UNIT_WEIGHT_GROSS'", 'decimal_places': '3', 'max_digits': '8'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'blank': 'True', 'null': 'True', 'db_column': "'UNIT_WEIGHT_NET'", 'decimal_places': '3', 'max_digits': '8'})
        },
        'ets.order': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Order'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'consignee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['ets.Consignee']"}),
            'created': ('django.db.models.fields.DateField', [], {}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'expiry': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['ets.Location']"}),
            'origin_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'transport_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_ouc': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['ets.Warehouse']"})
        },
        'ets.orderitem': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'OrderItem'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'commodity_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lti_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '0'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['ets.Order']"}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '11', 'decimal_places': '3'}),
            'removed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '3', 'blank': 'True'})
        },
        'ets.packagingdescriptionshort': {
            'Meta': {'object_name': 'PackagingDescriptionShort'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'ets.place': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Place', 'db_table': "u'epic_geo'"},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'geo_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'geo_point_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'org_code': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'organization_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'reporting_code': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'ets.stockitem': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'StockItem'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'number_of_units': ('django.db.models.fields.IntegerField', [], {}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23', 'primary_key': 'True'}),
            'package_code': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'quality_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quality_description': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'quantity_gross': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'quantity_net': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '3', 'blank': 'True'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock_items'", 'to': "orm['ets.Warehouse']"})
        },
        'ets.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'compas_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profiles'", 'null': 'True', 'to': "orm['ets.CompasPerson']"}),
            'dispatch_warehouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'dispatcher_profiles'", 'null': 'True', 'to': "orm['ets.Warehouse']"}),
            'is_all_receiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_compas_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_dispatcher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_reciever': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reader_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reception_warehouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receipient_profiles'", 'null': 'True', 'to': "orm['ets.Warehouse']"}),
            'super_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'ets.userprofileauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'UserProfileAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_userprofile_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'compas_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_profiles'", 'null': 'True', 'to': "orm['ets.CompasPerson']"}),
            'dispatch_warehouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_dispatcher_profiles'", 'null': 'True', 'to': "orm['ets.Warehouse']"}),
            'is_all_receiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_compas_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_dispatcher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_reciever': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reader_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reception_warehouse': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_receipient_profiles'", 'null': 'True', 'to': "orm['ets.Warehouse']"}),
            'super_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ets.warehouse': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Warehouse'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warehouses'", 'to': "orm['ets.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'warehouses'", 'null': 'True', 'to': "orm['ets.Consignee']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'ets.waybill': {
            'Meta': {'object_name': 'Waybill'},
            'audit_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'container_one_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipt_waybills'", 'to': "orm['ets.Warehouse']"}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dispatch_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'dispatcher_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dispatch_waybills'", 'to': "orm['ets.CompasPerson']"}),
            'invalidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loading_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'order_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'processed_for_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'rec_sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receipt_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient_arrival_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_end_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'recipient_waybills'", 'null': 'True', 'to': "orm['ets.CompasPerson']"}),
            'recipient_remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recipient_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_start_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transport_delivery_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transport_vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dispatch_waybills'", 'to': "orm['ets.Warehouse']"})
        },
        'ets.waybillauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'WaybillAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_waybill_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'audit_comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'container_one_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_receipt_waybills'", 'to': "orm['ets.Warehouse']"}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dispatch_remarks': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'dispatcher_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_dispatch_waybills'", 'to': "orm['ets.CompasPerson']"}),
            'invalidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loading_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'order_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'processed_for_payment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'rec_sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receipt_validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipient_arrival_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_end_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_person': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_recipient_waybills'", 'null': 'True', 'to': "orm['ets.CompasPerson']"}),
            'recipient_remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recipient_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_start_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transport_delivery_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transport_vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_dispatch_waybills'", 'to': "orm['ets.Warehouse']"})
        }
    }

    complete_apps = ['ets']
