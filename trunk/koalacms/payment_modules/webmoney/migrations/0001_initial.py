# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PaymentSettings'
        db.create_table('webmoney_paymentsettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('purse', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('secret_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('webmoney', ['PaymentSettings'])


    def backwards(self, orm):
        
        # Deleting model 'PaymentSettings'
        db.delete_table('webmoney_paymentsettings')


    models = {
        'webmoney.paymentsettings': {
            'Meta': {'object_name': 'PaymentSettings'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'purse': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'secret_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['webmoney']
