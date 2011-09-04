# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'CompasLogger'
        db.delete_table(u'loggercompas')

        # Deleting model 'EpicStock'
        db.delete_table(u'epic_stock')

        # Deleting model 'Place'
        db.delete_table(u'epic_geo')

        # Deleting model 'DispatchMaster'
        db.delete_table(u'dispatch_masters')

        # Deleting model 'LtiOriginal'
        db.delete_table(u'epic_lti')

        # Deleting model 'CompasPerson'
        db.delete_table(u'epic_persons')

        # Deleting model 'DispatchDetail'
        db.delete_table(u'dispatch_details')


    def backwards(self, orm):
        
        # Adding model 'CompasLogger'
        db.create_table(u'loggercompas', (
            ('errorRec', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('wb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Waybill'], primary_key=True)),
            ('errorDisp', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('lti', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('data_in', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
            ('data_out', self.gf('django.db.models.fields.CharField')(max_length=5000, blank=True)),
        ))
        db.send_create_signal('ets', ['CompasLogger'])

        # Adding model 'EpicStock'
        db.create_table(u'epic_stock', (
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('qualitycode', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23)),
            ('wh_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('wh_location', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=12, decimal_places=3, blank=True)),
            ('qualitydescr', self.gf('django.db.models.fields.CharField')(max_length=11, blank=True)),
            ('wh_pk', self.gf('django.db.models.fields.CharField')(max_length=90, primary_key=True)),
            ('wh_country', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('wh_regional', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('wh_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('allocation_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('packagename', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('package_code', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('project_wbs_element', self.gf('django.db.models.fields.CharField')(max_length=24, blank=True)),
            ('cmmname', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('reference_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(max_digits=12, decimal_places=3)),
        ))
        db.send_create_signal('ets', ['EpicStock'])

        # Adding model 'Place'
        db.create_table(u'epic_geo', (
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('geo_point_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('reporting_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('org_code', self.gf('django.db.models.fields.CharField')(max_length=7, primary_key=True)),
            ('geo_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('ets', ['Place'])

        # Adding model 'DispatchMaster'
        db.create_table(u'dispatch_masters', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('destination_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('destination_location_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('last_mod_user', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('customised', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('trailer_plate', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('person_code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('notify_indicator', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('trans_contractor_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('activity_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('notify_org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('offid', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('modetrans_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('intdlv_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('printed_indicator', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('atl_li_code', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('origin_code', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('loading_date', self.gf('django.db.models.fields.DateField')()),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('vehicle_registration', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('pro_activity_code', self.gf('django.db.models.fields.CharField')(max_length=6, blank=True)),
            ('nmbtrl_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('last_mod_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('origin_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('origin_location_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('loan_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('dispatch_date', self.gf('django.db.models.fields.DateField')()),
            ('container_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('recv_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('tran_type_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('lndarrm_code', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('tran_type_descr', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('lti_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('supplier1_ouc', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('person_ouc', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('supplier2_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('nmbplt_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('certifing_title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('document_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('send_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('origin_descr', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('driver_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('trans_subcontractor_code', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('intvyg_code', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
        ))
        db.send_create_signal('ets', ['DispatchMaster'])

        # Adding model 'LtiOriginal'
        db.create_table(u'epic_lti', (
            ('origin_location_code', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='ORIGIN_LOCATION_CODE')),
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25, db_column='SI_RECORD_ID', blank=True)),
            ('origin_loc_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='ORIGIN_LOC_NAME')),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='CODE')),
            ('destination_location_code', self.gf('django.db.models.fields.CharField')(max_length=10, db_column='DESTINATION_LOCATION_CODE')),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(decimal_places=3, db_column='QUANTITY_NET', max_digits=11)),
            ('consegnee_code', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='CONSEGNEE_CODE')),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(decimal_places=3, db_column='QUANTITY_GROSS', max_digits=11)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18, db_column='COMMODITY_CODE')),
            ('destination_loc_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='DESTINATION_LOC_NAME')),
            ('requested_dispatch_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='REQUESTED_DISPATCH_DATE', blank=True)),
            ('transport_name', self.gf('django.db.models.fields.CharField')(max_length=30, db_column='TRANSPORT_NAME')),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(max_digits=8, null=True, decimal_places=3, db_column='UNIT_WEIGHT_NET', blank=True)),
            ('transport_ouc', self.gf('django.db.models.fields.CharField')(max_length=13, db_column='TRANSPORT_OUC')),
            ('origin_wh_code', self.gf('django.db.models.fields.CharField')(max_length=13, db_column='ORIGIN_WH_CODE', blank=True)),
            ('lti_id', self.gf('django.db.models.fields.CharField')(max_length=40, db_column='LTI_ID')),
            ('number_of_units', self.gf('django.db.models.fields.DecimalField')(decimal_places=3, db_column='NUMBER_OF_UNITS', max_digits=7)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=8, null=True, decimal_places=3, db_column='UNIT_WEIGHT_GROSS', blank=True)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9, db_column='COMM_CATEGORY_CODE')),
            ('origin_wh_name', self.gf('django.db.models.fields.CharField')(max_length=50, db_column='ORIGIN_WH_NAME', blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, db_column='EXPIRY_DATE', blank=True)),
            ('project_wbs_element', self.gf('django.db.models.fields.CharField')(max_length=24, db_column='PROJECT_WBS_ELEMENT', blank=True)),
            ('cmmname', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='CMMNAME', blank=True)),
            ('lti_date', self.gf('django.db.models.fields.DateField')(db_column='LTI_DATE')),
            ('consegnee_name', self.gf('django.db.models.fields.CharField')(max_length=80, db_column='CONSEGNEE_NAME')),
            ('lti_pk', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True, db_column='LTI_PK')),
            ('origintype_desc', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='ORIGINTYPE_DESC', blank=True)),
            ('transport_code', self.gf('django.db.models.fields.CharField')(max_length=4, db_column='TRANSPORT_CODE')),
            ('origin_type', self.gf('django.db.models.fields.CharField')(max_length=1, db_column='ORIGIN_TYPE')),
            ('si_code', self.gf('django.db.models.fields.CharField')(max_length=8, db_column='SI_CODE')),
        ))
        db.send_create_signal('ets', ['LtiOriginal'])

        # Adding model 'CompasPerson'
        db.create_table(u'epic_persons', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('person_pk', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, db_column='e_mail_address', blank=True)),
            ('location_code', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal('ets', ['CompasPerson'])

        # Adding model 'DispatchDetail'
        db.create_table(u'dispatch_details', (
            ('si_record_id', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.DispatchMaster'])),
            ('origin_id', self.gf('django.db.models.fields.CharField')(max_length=23, blank=True)),
            ('last_mod_user', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('commodity_code', self.gf('django.db.models.fields.CharField')(max_length=18)),
            ('quantity_gross', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('document_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('quantity_net', self.gf('django.db.models.fields.DecimalField')(max_digits=11, decimal_places=3)),
            ('quality', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit_weight_net', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('recv_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('allocation_destination_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('offid', self.gf('django.db.models.fields.CharField')(max_length=13, blank=True)),
            ('rpydtl_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('unit_weight_gross', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=3, blank=True)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('package_code', self.gf('django.db.models.fields.CharField')(max_length=17)),
            ('londtl_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('send_pack', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('last_mod_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('lonmst_id', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('number_of_units', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('ets', ['DispatchDetail'])


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
        'ets.commodity': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Commodity'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commodities'", 'to': "orm['ets.CommodityCategory']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '18', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ets.commoditycategory': {
            'Meta': {'ordering': "('code',)", 'object_name': 'CommodityCategory'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '9', 'primary_key': 'True'})
        },
        'ets.compas': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Compas'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'db_engine': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'db_host': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '100'}),
            'db_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'db_password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'db_port': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'db_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'officers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'compases'", 'symmetrical': 'False', 'to': "orm['auth.User']"})
        },
        'ets.loadingdetail': {
            'Meta': {'ordering': "('_order',)", 'unique_together': "(('waybill', 'stock_item'),)", 'object_name': 'LoadingDetail'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'stock_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dispatches'", 'to': "orm['ets.StockItem']"}),
            'units_damaged_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'damage_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'lost_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'waybill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loading_details'", 'to': "orm['ets.Waybill']"})
        },
        'ets.loadingdetailauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'LoadingDetailAuditLogEntry'},
            '_order': ('django.db.models.fields.proxy.OrderWrt', [], {}),
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_loadingdetail_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'stock_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_dispatches'", 'to': "orm['ets.StockItem']"}),
            'units_damaged_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_damage_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'units_lost_reason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_lost_reason'", 'null': 'True', 'to': "orm['ets.LossDamageType']"}),
            'waybill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_loading_details'", 'to': "orm['ets.Waybill']"})
        },
        'ets.location': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Location'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ets.lossdamagetype': {
            'Meta': {'object_name': 'LossDamageType', 'db_table': "u'epic_lossdamagereason'"},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'loss_damages'", 'db_column': "'comm_category_code'", 'to': "orm['ets.CommodityCategory']"}),
            'cause': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'ets.order': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Order'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'consignee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['ets.Organization']"}),
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
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_items'", 'to': "orm['ets.Commodity']"}),
            'lti_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['ets.Order']"}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        'ets.organization': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Organization'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'ets.package': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Package'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '17', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'ets.person': {
            'Meta': {'ordering': "('code',)", 'object_name': 'Person'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'compas': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'to': "orm['ets.Compas']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'to': "orm['ets.Location']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'to': "orm['ets.Organization']"}),
            'person_pk': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'person'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'ets.receiptwaybill': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'ReceiptWaybill'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'arrival_date': ('django.db.models.fields.DateField', [], {}),
            'container_one_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_reciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'distance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'end_discharge_date': ('django.db.models.fields.DateField', [], {}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recipient_waybills'", 'to': "orm['ets.Person']"}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'start_discharge_date': ('django.db.models.fields.DateField', [], {}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybill': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'receipt'", 'unique': 'True', 'to': "orm['ets.Waybill']"})
        },
        'ets.stockitem': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'StockItem'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'allocation_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'commodity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stocks'", 'to': "orm['ets.Commodity']"}),
            'is_bulk': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23', 'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stocks'", 'to': "orm['ets.Package']"}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'quality_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quality_description': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stock_items'", 'to': "orm['ets.Warehouse']"})
        },
        'ets.warehouse': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Warehouse'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '13', 'primary_key': 'True'}),
            'compas': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warehouses'", 'to': "orm['ets.Compas']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warehouses'", 'to': "orm['ets.Location']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'warehouses'", 'null': 'True', 'to': "orm['ets.Organization']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'ets.waybill': {
            'Meta': {'ordering': "('_order',)", 'object_name': 'Waybill'},
            '_order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'container_one_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receipt_waybills'", 'to': "orm['ets.Warehouse']"}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'dispatch_remarks': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'dispatcher_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dispatch_waybills'", 'to': "orm['ets.Person']"}),
            'loading_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'waybills'", 'to': "orm['ets.Order']"}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'default': "u'WIT'", 'max_length': '10'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'default': "u'02'", 'max_length': '10'}),
            'transport_vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ets.waybillauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'WaybillAuditLogEntry'},
            '_order': ('django.db.models.fields.proxy.OrderWrt', [], {}),
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_waybill_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'container_one_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_one_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_remarks_dispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'container_two_seal_number': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_receipt_waybills'", 'to': "orm['ets.Warehouse']"}),
            'dispatch_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'dispatch_remarks': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'dispatcher_person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_dispatch_waybills'", 'to': "orm['ets.Person']"}),
            'loading_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_waybills'", 'to': "orm['ets.Order']"}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'default': "u'WIT'", 'max_length': '10'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'default': "u'02'", 'max_length': '10'}),
            'transport_vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['ets']
