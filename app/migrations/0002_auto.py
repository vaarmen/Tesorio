# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field buyers on 'Company'
        db.delete_table(db.shorten_name(u'app_company_buyers'))

        # Adding M2M table for field suppliers on 'Company'
        m2m_table_name = db.shorten_name(u'app_company_suppliers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_company', models.ForeignKey(orm[u'app.company'], null=False)),
            ('to_company', models.ForeignKey(orm[u'app.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_company_id', 'to_company_id'])


    def backwards(self, orm):
        # Adding M2M table for field buyers on 'Company'
        m2m_table_name = db.shorten_name(u'app_company_buyers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_company', models.ForeignKey(orm[u'app.company'], null=False)),
            ('to_company', models.ForeignKey(orm[u'app.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_company_id', 'to_company_id'])

        # Removing M2M table for field suppliers on 'Company'
        db.delete_table(db.shorten_name(u'app_company_suppliers'))


    models = {
        u'app.company': {
            'Meta': {'object_name': 'Company'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'apr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '5'}),
            'cash_commited': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ein': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'has_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_buyer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_supplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'suppliers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'buyers'", 'null': 'True', 'to': u"orm['app.Company']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'app.historicalcompany': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalCompany'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'apr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '5'}),
            'cash_commited': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'ein': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'has_registered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'is_buyer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_supplier': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'app.historicalinvoice': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalInvoice'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            u'buyer_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'buyer_inv_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'current_bid_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'inv_date': ('django.db.models.fields.DateField', [], {}),
            'po_num': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '254'}),
            u'supplier_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'supplier_inv_number': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'app.historicaloffer': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalOffer'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'apr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '5'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'date_due': ('django.db.models.fields.DateTimeField', [], {}),
            'days_accelerated': ('django.db.models.fields.IntegerField', [], {}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '10'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            u'invoice_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'offer_type': ('django.db.models.fields.CharField', [], {'default': "'BID'", 'max_length': '254'}),
            u'parameters_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'profit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'app.historicalofferparameters': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalOfferParameters'},
            'alt_1_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_1_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            'alt_2_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_2_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            'alt_3_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_3_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            u'buyer_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'parameters_type': ('django.db.models.fields.CharField', [], {'default': "'BID'", 'max_length': '254'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'supplier_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'app.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buyer_invoices'", 'to': u"orm['app.Company']"}),
            'buyer_inv_key': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_bid': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'current_invoice'", 'unique': 'True', 'to': u"orm['app.Offer']"}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inv_date': ('django.db.models.fields.DateField', [], {}),
            'po_num': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'OPEN'", 'max_length': '254'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_invoices'", 'to': u"orm['app.Company']"}),
            'supplier_inv_number': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'app.offer': {
            'Meta': {'object_name': 'Offer'},
            'amount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'apr': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '5'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_due': ('django.db.models.fields.DateTimeField', [], {}),
            'days_accelerated': ('django.db.models.fields.IntegerField', [], {}),
            'discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '11', 'decimal_places': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Invoice']"}),
            'offer_type': ('django.db.models.fields.CharField', [], {'default': "'BID'", 'max_length': '254'}),
            'parameters': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'offers'", 'to': u"orm['app.OfferParameters']"}),
            'profit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '20', 'decimal_places': '4'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'app.offerparameters': {
            'Meta': {'object_name': 'OfferParameters'},
            'alt_1_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_1_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            'alt_2_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_2_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            'alt_3_days': ('django.db.models.fields.IntegerField', [], {}),
            'alt_3_percent': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '5'}),
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'buyer_offerparams'", 'to': u"orm['app.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameters_type': ('django.db.models.fields.CharField', [], {'default': "'BID'", 'max_length': '254'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'supplier': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supplier_offerparams'", 'to': u"orm['app.Company']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'app.person': {
            'Meta': {'object_name': 'Person'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'people'", 'to': u"orm['app.Company']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'time_zone': ('django.db.models.fields.CharField', [], {'default': "'America/New_York'", 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'person'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']