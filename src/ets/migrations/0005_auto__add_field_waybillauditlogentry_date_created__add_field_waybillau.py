# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'WaybillAuditLogEntry.date_created'
        db.add_column('ets_waybillauditlogentry', 'date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Adding field 'WaybillAuditLogEntry.date_modified'
        db.add_column('ets_waybillauditlogentry', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Adding field 'WaybillAuditLogEntry.date_removed'
        db.add_column('ets_waybillauditlogentry', 'date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Waybill.date_created'
        db.add_column('ets_waybill', 'date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Adding field 'Waybill.date_modified'
        db.add_column('ets_waybill', 'date_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now), keep_default=False)

        # Adding field 'Waybill.date_removed'
        db.add_column('ets_waybill', 'date_removed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'WaybillAuditLogEntry.date_created'
        db.delete_column('ets_waybillauditlogentry', 'date_created')

        # Deleting field 'WaybillAuditLogEntry.date_modified'
        db.delete_column('ets_waybillauditlogentry', 'date_modified')

        # Deleting field 'WaybillAuditLogEntry.date_removed'
        db.delete_column('ets_waybillauditlogentry', 'date_removed')

        # Deleting field 'Waybill.date_created'
        db.delete_column('ets_waybill', 'date_created')

        # Deleting field 'Waybill.date_modified'
        db.delete_column('ets_waybill', 'date_modified')

        # Deleting field 'Waybill.date_removed'
        db.delete_column('ets_waybill', 'date_removed')


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
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Warehouse']", 'db_column': "'org_unit_code'"})
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
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
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
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
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
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'number_units_damaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_good': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'number_units_lost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23'}),
            'over_offload_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloaded_units': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'package': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
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
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'db_column': "'NUMBER_OF_UNITS'", 'decimal_places': '3', 'max_digits': '7'}),
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
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'commodity_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'lti_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '3'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['ets.Order']"}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'})
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
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'commodity_code': ('django.db.models.fields.CharField', [], {'max_length': '18'}),
            'commodity_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'origin_id': ('django.db.models.fields.CharField', [], {'max_length': '23', 'primary_key': 'True'}),
            'package_code': ('django.db.models.fields.CharField', [], {'max_length': '17'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'project_number': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'quality_code': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'quality_description': ('django.db.models.fields.CharField', [], {'max_length': '11', 'blank': 'True'}),
            'si_code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'unit_weight_gross': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
            'unit_weight_net': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'recipient_remarks': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'recipient_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_start_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'default': "u'WIT'", 'max_length': '10'}),
            'transport_delivery_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'default': "u'02'", 'max_length': '10'}),
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
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_removed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'recipient_remarks': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'recipient_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipient_start_discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'sent_compas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_type': ('django.db.models.fields.CharField', [], {'default': "u'WIT'", 'max_length': '10'}),
            'transport_delivery_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_dispach_signed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transport_driver_licence': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_driver_name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'transport_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transport_sub_contractor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_trailer_registration': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'transport_type': ('django.db.models.fields.CharField', [], {'default': "u'02'", 'max_length': '10'}),
            'transport_vehicle_registration': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_auditlog_dispatch_waybills'", 'to': "orm['ets.Warehouse']"})
        }
    }

    complete_apps = ['ets']
