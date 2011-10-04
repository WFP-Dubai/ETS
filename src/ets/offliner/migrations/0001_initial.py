# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UpdateLog'
        db.create_table('offliner_updatelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2011, 10, 4, 9, 14, 56, 180084))),
            ('serialized_data', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('offliner', ['UpdateLog'])


    def backwards(self, orm):
        
        # Deleting model 'UpdateLog'
        db.delete_table('offliner_updatelog')


    models = {
        'offliner.updatelog': {
            'Meta': {'object_name': 'UpdateLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2011, 10, 4, 9, 14, 56, 180084)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'serialized_data': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['offliner']
