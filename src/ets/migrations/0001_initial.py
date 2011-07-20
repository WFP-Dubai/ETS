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
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('ets', ['Place'])

        # Adding model 'WaybillAuditLogEntry'
        db.create_table('ets_waybillauditlogentry', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('ltiNumber', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('waybillNumber', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dateOfLoading', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dateOfDispatch', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transactionType', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('transportType', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dispatchRemarks', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispatcherName', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dispatcherTitle', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('dispatcherSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportContractor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportSubContractor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDriverName', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDriverLicenceID', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportVehicleRegistration', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportTrailerRegistration', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDispachSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportDispachSignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('transportDeliverySigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportDeliverySignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('containerOneNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneSealNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoSealNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneRemarksDispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoRemarksDispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneRemarksReciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoRemarksReciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('recipientLocation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientConsingee', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientTitle', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientArrivalDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientStartDischargeDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientEndDischargeDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientDistance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('recipientRemarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recipientSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recipientSignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('destinationWarehouse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Place'], blank=True)),
            ('waybillValidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillReceiptValidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillRecSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillProcessedForPayment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auditComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_waybill_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['WaybillAuditLogEntry'])

        # Adding model 'Waybill'
        db.create_table('ets_waybill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ltiNumber', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('waybillNumber', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('dateOfLoading', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('dateOfDispatch', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('transactionType', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('transportType', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dispatchRemarks', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dispatcherName', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('dispatcherTitle', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('dispatcherSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportContractor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportSubContractor', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDriverName', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDriverLicenceID', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportVehicleRegistration', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportTrailerRegistration', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('transportDispachSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportDispachSignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('transportDeliverySigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('transportDeliverySignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('containerOneNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneSealNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoSealNumber', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneRemarksDispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoRemarksDispatch', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerOneRemarksReciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('containerTwoRemarksReciept', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('recipientLocation', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientConsingee', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientName', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientTitle', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('recipientArrivalDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientStartDischargeDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientEndDischargeDate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('recipientDistance', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('recipientRemarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('recipientSigned', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('recipientSignedTimestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('destinationWarehouse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Place'], blank=True)),
            ('waybillValidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillReceiptValidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillRecSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('waybillProcessedForPayment', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invalidated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('auditComment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('ets', ['Waybill'])

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

        # Adding model 'RemovedLtis'
        db.create_table(u'waybill_removed_ltis', (
            ('lti', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.LtiOriginal'], primary_key=True)),
        ))
        db.send_create_signal('ets', ['RemovedLtis'])

        # Adding model 'EpicPerson'
        db.create_table(u'epic_persons', (
            ('person_pk', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('org_unit_code', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('type_of_document', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('organization_id', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('document_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('e_mail_address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('mobile_phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('official_tel_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('fax_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('effective_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('expiry_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('ets', ['EpicPerson'])

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

        # Adding model 'EpicLossDamages'
        db.create_table(u'epic_lossdamagereason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('comm_category_code', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('cause', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('ets', ['EpicLossDamages'])

        # Adding model 'LtiWithStock'
        db.create_table('ets_ltiwithstock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lti_line', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.LtiOriginal'])),
            ('stock_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.EpicStock'])),
            ('lti_code', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
        ))
        db.send_create_signal('ets', ['LtiWithStock'])

        # Adding model 'LoadingDetailAuditLogEntry'
        db.create_table('ets_loadingdetailauditlogentry', (
            ('id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('wbNumber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Waybill'])),
            ('order_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.LtiWithStock'])),
            ('numberUnitsLoaded', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('numberUnitsGood', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('numberUnitsLost', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('numberUnitsDamaged', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('unitsLostReason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_LD_LostReason', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsDamagedReason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_LD_DamagedReason', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsDamagedType', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_LD_DamagedType', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsLostType', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='_auditlog_LD_LossType', null=True, to=orm['ets.EpicLossDamages'])),
            ('overloadedUnits', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loadingDetailSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('overOffloadUnits', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_loadingdetail_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['LoadingDetailAuditLogEntry'])

        # Adding model 'LoadingDetail'
        db.create_table('ets_loadingdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('wbNumber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.Waybill'])),
            ('order_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.LtiWithStock'])),
            ('numberUnitsLoaded', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=3)),
            ('numberUnitsGood', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('numberUnitsLost', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('numberUnitsDamaged', self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=3, blank=True)),
            ('unitsLostReason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LD_LostReason', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsDamagedReason', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LD_DamagedReason', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsDamagedType', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LD_DamagedType', null=True, to=orm['ets.EpicLossDamages'])),
            ('unitsLostType', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LD_LossType', null=True, to=orm['ets.EpicLossDamages'])),
            ('overloadedUnits', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loadingDetailSentToCompas', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('overOffloadUnits', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ets', ['LoadingDetail'])

        # Adding model 'DispatchPoint'
        db.create_table('ets_dispatchpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('origin_loc_name', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('origin_location_code', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('origin_wh_code', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('origin_wh_name', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('ACTIVE_START_DATE', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('ets', ['DispatchPoint'])

        # Adding model 'ReceptionPoint'
        db.create_table('ets_receptionpoint', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('LOC_NAME', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('LOCATION_CODE', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('consegnee_code', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('consegnee_name', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
            ('ACTIVE_START_DATE', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('ets', ['ReceptionPoint'])

        # Adding model 'UserProfileAuditLogEntry'
        db.create_table('ets_userprofileauditlogentry', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('warehouses', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.DispatchPoint'], null=True, blank=True)),
            ('receptionPoints', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.ReceptionPoint'], null=True, blank=True)),
            ('isCompasUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isDispatcher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isReciever', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAllReceiver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compasUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.EpicPerson'], null=True, blank=True)),
            ('superUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('readerUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('action_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('action_user', self.gf('audit_log.models.fields.LastUserField')(related_name='_userprofile_audit_log_entry', null=True, to=orm['auth.User'])),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('ets', ['UserProfileAuditLogEntry'])

        # Adding model 'UserProfile'
        db.create_table('ets_userprofile', (
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('warehouses', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.DispatchPoint'], null=True, blank=True)),
            ('receptionPoints', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.ReceptionPoint'], null=True, blank=True)),
            ('isCompasUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isDispatcher', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isReciever', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('isAllReceiver', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compasUser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ets.EpicPerson'], null=True, blank=True)),
            ('superUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('readerUser', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('ets', ['UserProfile'])

        # Adding model 'SiTracker'
        db.create_table('ets_sitracker', (
            ('LTI', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['ets.LtiOriginal'], unique=True, primary_key=True)),
            ('number_units_left', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
            ('number_units_start', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=3)),
        ))
        db.send_create_signal('ets', ['SiTracker'])

        # Adding model 'PackagingDescriptionShort'
        db.create_table('ets_packagingdescriptionshort', (
            ('packageCode', self.gf('django.db.models.fields.CharField')(max_length=5, primary_key=True)),
            ('packageShortName', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('ets', ['PackagingDescriptionShort'])

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

        # Deleting model 'WaybillAuditLogEntry'
        db.delete_table('ets_waybillauditlogentry')

        # Deleting model 'Waybill'
        db.delete_table('ets_waybill')

        # Deleting model 'LtiOriginal'
        db.delete_table(u'epic_lti')

        # Deleting model 'RemovedLtis'
        db.delete_table(u'waybill_removed_ltis')

        # Deleting model 'EpicPerson'
        db.delete_table(u'epic_persons')

        # Deleting model 'EpicStock'
        db.delete_table(u'epic_stock')

        # Deleting model 'EpicLossDamages'
        db.delete_table(u'epic_lossdamagereason')

        # Deleting model 'LtiWithStock'
        db.delete_table('ets_ltiwithstock')

        # Deleting model 'LoadingDetailAuditLogEntry'
        db.delete_table('ets_loadingdetailauditlogentry')

        # Deleting model 'LoadingDetail'
        db.delete_table('ets_loadingdetail')

        # Deleting model 'DispatchPoint'
        db.delete_table('ets_dispatchpoint')

        # Deleting model 'ReceptionPoint'
        db.delete_table('ets_receptionpoint')

        # Deleting model 'UserProfileAuditLogEntry'
        db.delete_table('ets_userprofileauditlogentry')

        # Deleting model 'UserProfile'
        db.delete_table('ets_userprofile')

        # Deleting model 'SiTracker'
        db.delete_table('ets_sitracker')

        # Deleting model 'PackagingDescriptionShort'
        db.delete_table('ets_packagingdescriptionshort')

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
        'ets.dispatchpoint': {
            'ACTIVE_START_DATE': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'DispatchPoint'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'origin_loc_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'origin_location_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'origin_wh_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'origin_wh_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'})
        },
        'ets.epiclossdamages': {
            'Meta': {'object_name': 'EpicLossDamages', 'db_table': "u'epic_lossdamagereason'"},
            'cause': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'comm_category_code': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'ets.epicperson': {
            'Meta': {'object_name': 'EpicPerson', 'db_table': "u'epic_persons'"},
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
            'org_unit_code': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'organization_id': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'person_pk': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type_of_document': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loadingDetailSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numberUnitsDamaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'numberUnitsGood': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'numberUnitsLoaded': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'numberUnitsLost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'order_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.LtiWithStock']"}),
            'overOffloadUnits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloadedUnits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitsDamagedReason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LD_DamagedReason'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsDamagedType': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LD_DamagedType'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsLostReason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LD_LostReason'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsLostType': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LD_LossType'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'wbNumber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Waybill']"})
        },
        'ets.loadingdetailauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'LoadingDetailAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_loadingdetail_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'loadingDetailSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'numberUnitsDamaged': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'numberUnitsGood': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'numberUnitsLoaded': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '3'}),
            'numberUnitsLost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '3', 'blank': 'True'}),
            'order_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.LtiWithStock']"}),
            'overOffloadUnits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'overloadedUnits': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitsDamagedReason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_LD_DamagedReason'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsDamagedType': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_LD_DamagedType'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsLostReason': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_LD_LostReason'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'unitsLostType': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_auditlog_LD_LossType'", 'null': 'True', 'to': "orm['ets.EpicLossDamages']"}),
            'wbNumber': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Waybill']"})
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
        'ets.ltiwithstock': {
            'Meta': {'object_name': 'LtiWithStock'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lti_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'lti_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.LtiOriginal']"}),
            'stock_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.EpicStock']"})
        },
        'ets.packagingdescriptionshort': {
            'Meta': {'object_name': 'PackagingDescriptionShort'},
            'packageCode': ('django.db.models.fields.CharField', [], {'max_length': '5', 'primary_key': 'True'}),
            'packageShortName': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'ets.place': {
            'Meta': {'object_name': 'Place', 'db_table': "u'epic_geo'"},
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'geo_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'geo_point_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'org_code': ('django.db.models.fields.CharField', [], {'max_length': '7', 'primary_key': 'True'}),
            'organization_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'reporting_code': ('django.db.models.fields.CharField', [], {'max_length': '7'})
        },
        'ets.receptionpoint': {
            'ACTIVE_START_DATE': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'LOCATION_CODE': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'LOC_NAME': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'Meta': {'ordering': "('LOC_NAME', 'consegnee_name')", 'object_name': 'ReceptionPoint'},
            'consegnee_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'consegnee_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'ets.removedltis': {
            'Meta': {'object_name': 'RemovedLtis', 'db_table': "u'waybill_removed_ltis'"},
            'lti': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.LtiOriginal']", 'primary_key': 'True'})
        },
        'ets.sitracker': {
            'LTI': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ets.LtiOriginal']", 'unique': 'True', 'primary_key': 'True'}),
            'Meta': {'object_name': 'SiTracker'},
            'number_units_left': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'}),
            'number_units_start': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '3'})
        },
        'ets.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'compasUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.EpicPerson']", 'null': 'True', 'blank': 'True'}),
            'isAllReceiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isCompasUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isDispatcher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isReciever': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readerUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receptionPoints': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.ReceptionPoint']", 'null': 'True', 'blank': 'True'}),
            'superUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'warehouses': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.DispatchPoint']", 'null': 'True', 'blank': 'True'})
        },
        'ets.userprofileauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'UserProfileAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_userprofile_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'compasUser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.EpicPerson']", 'null': 'True', 'blank': 'True'}),
            'isAllReceiver': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isCompasUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isDispatcher': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isReciever': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'readerUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receptionPoints': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.ReceptionPoint']", 'null': 'True', 'blank': 'True'}),
            'superUser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'warehouses': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.DispatchPoint']", 'null': 'True', 'blank': 'True'})
        },
        'ets.waybill': {
            'Meta': {'object_name': 'Waybill'},
            'auditComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'containerOneNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneRemarksDispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneRemarksReciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneSealNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoRemarksDispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoRemarksReciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoSealNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'dateOfDispatch': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateOfLoading': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'destinationWarehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Place']", 'blank': 'True'}),
            'dispatchRemarks': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispatcherName': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dispatcherSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dispatcherTitle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invalidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ltiNumber': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'recipientArrivalDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientConsingee': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientDistance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipientEndDischargeDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientLocation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientRemarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recipientSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipientSignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipientStartDischargeDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientTitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'transactionType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transportContractor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportDeliverySigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transportDeliverySignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transportDispachSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transportDispachSignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transportDriverLicenceID': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportDriverName': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportSubContractor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportTrailerRegistration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transportVehicleRegistration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'waybillNumber': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'waybillProcessedForPayment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillRecSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillReceiptValidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillValidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'ets.waybillauditlogentry': {
            'Meta': {'ordering': "('-action_date',)", 'object_name': 'WaybillAuditLogEntry'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'action_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'action_user': ('audit_log.models.fields.LastUserField', [], {'related_name': "'_waybill_audit_log_entry'", 'null': 'True', 'to': "orm['auth.User']"}),
            'auditComment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'containerOneNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneRemarksDispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneRemarksReciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerOneSealNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoRemarksDispatch': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoRemarksReciept': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'containerTwoSealNumber': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'dateOfDispatch': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dateOfLoading': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'destinationWarehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ets.Place']", 'blank': 'True'}),
            'dispatchRemarks': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'dispatcherName': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dispatcherSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dispatcherTitle': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'invalidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ltiNumber': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'recipientArrivalDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientConsingee': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientDistance': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'recipientEndDischargeDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientLocation': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'recipientRemarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'recipientSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'recipientSignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'recipientStartDischargeDate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'recipientTitle': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'transactionType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transportContractor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportDeliverySigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transportDeliverySignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transportDispachSigned': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transportDispachSignedTimestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'transportDriverLicenceID': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportDriverName': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportSubContractor': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportTrailerRegistration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'transportType': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'transportVehicleRegistration': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'waybillNumber': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'waybillProcessedForPayment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillRecSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillReceiptValidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillSentToCompas': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'waybillValidated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['ets']
