# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Compas.start_date'
        db.add_column('ets_compas', 'start_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Compas.start_date'
        db.delete_column('ets_compas', 'start_date')


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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'db_engine': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'db_host': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '100'}),
            'db_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'db_password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'db_port': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'db_user': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'officers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'compases'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'})
        },
        'ets.compaslogger': {
            'Meta': {'ordering': "('-when_attempted',)", 'object_name': 'CompasLogger'},
            'action': ('django.db.models.fields.IntegerField', [], {}),
            'compas': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': "orm['ets.Compas']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'waybill': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'compass_loggers'", 'to': "orm['ets.Waybill']"}),
            'when_attempted': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
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
            'number_of_units': ('django.db.models.fields.DecimalField', [], {'max_digits': '12', 'decimal_places': '3'}),
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
            'external_ident': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'to': "orm['ets.Location']"}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'persons'", 'to': "orm['ets.Organization']"}),
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
            'sent_compas': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'sent_compas': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'primary_key': 'True', 'unique': 'True', 'populate_from': 'None', 'db_index': 'True'}),
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
            'sent_compas': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': 'None', 'db_index': 'True'}),
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
