# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Deparment'
        db.create_table(u'timetable_deparment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'timetable', ['Deparment'])

        # Adding model 'Semester'
        db.create_table(u'timetable_semester', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'timetable', ['Semester'])

        # Adding model 'Source'
        db.create_table(u'timetable_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('regex', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Source'])

        # Adding model 'Instructor'
        db.create_table(u'timetable_instructor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Instructor'])

        # Adding model 'ModulType'
        db.create_table(u'timetable_modultype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1024)),
        ))
        db.send_create_signal(u'timetable', ['ModulType'])

        # Adding model 'Event'
        db.create_table(u'timetable_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('modul', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Modul'])),
            ('semester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Semester'])),
            ('eventtype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.EventType'])),
            ('begin', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('weekday', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Event'])

        # Adding M2M table for field instructor on 'Event'
        m2m_table_name = db.shorten_name(u'timetable_event_instructor')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'timetable.event'], null=False)),
            ('instructor', models.ForeignKey(orm[u'timetable.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'instructor_id'])

        # Adding model 'EventType'
        db.create_table(u'timetable_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal(u'timetable', ['EventType'])

        # Adding field 'Modul.lp'
        db.add_column(u'timetable_modul', 'lp',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Modul.modultype'
        db.add_column(u'timetable_modul', 'modultype',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.ModulType'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Modul.describtion'
        db.add_column(u'timetable_modul', 'describtion',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Modul.deparment'
        db.add_column(u'timetable_modul', 'deparment',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Deparment'], null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Deparment'
        db.delete_table(u'timetable_deparment')

        # Deleting model 'Semester'
        db.delete_table(u'timetable_semester')

        # Deleting model 'Source'
        db.delete_table(u'timetable_source')

        # Deleting model 'Instructor'
        db.delete_table(u'timetable_instructor')

        # Deleting model 'ModulType'
        db.delete_table(u'timetable_modultype')

        # Deleting model 'Event'
        db.delete_table(u'timetable_event')

        # Removing M2M table for field instructor on 'Event'
        db.delete_table(db.shorten_name(u'timetable_event_instructor'))

        # Deleting model 'EventType'
        db.delete_table(u'timetable_eventtype')

        # Deleting field 'Modul.lp'
        db.delete_column(u'timetable_modul', 'lp')

        # Deleting field 'Modul.modultype'
        db.delete_column(u'timetable_modul', 'modultype_id')

        # Deleting field 'Modul.describtion'
        db.delete_column(u'timetable_modul', 'describtion')

        # Deleting field 'Modul.deparment'
        db.delete_column(u'timetable_modul', 'deparment_id')


    models = {
        u'timetable.deparment': {
            'Meta': {'object_name': 'Deparment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'timetable.event': {
            'Meta': {'object_name': 'Event'},
            'begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'eventtype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.EventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Instructor']", 'symmetrical': 'False'}),
            'modul': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Modul']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Semester']"}),
            'weekday': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'timetable.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'timetable.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'timetable.modul': {
            'Meta': {'object_name': 'Modul'},
            'deparment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Deparment']", 'null': 'True', 'blank': 'True'}),
            'describtion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modultype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.ModulType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'timetable.modultype': {
            'Meta': {'object_name': 'ModulType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'timetable.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'timetable.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['timetable']