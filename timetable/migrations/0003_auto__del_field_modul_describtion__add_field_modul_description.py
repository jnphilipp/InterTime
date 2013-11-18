# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Modul.describtion'
        db.delete_column(u'timetable_modul', 'describtion')

        # Adding field 'Modul.description'
        db.add_column(u'timetable_modul', 'description',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field instructor on 'Event'
        db.delete_table(db.shorten_name(u'timetable_event_instructor'))

        # Adding M2M table for field instructors on 'Event'
        m2m_table_name = db.shorten_name(u'timetable_event_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'timetable.event'], null=False)),
            ('instructor', models.ForeignKey(orm[u'timetable.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'instructor_id'])


    def backwards(self, orm):
        # Adding field 'Modul.describtion'
        db.add_column(u'timetable_modul', 'describtion',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Modul.description'
        db.delete_column(u'timetable_modul', 'description')

        # Adding M2M table for field instructor on 'Event'
        m2m_table_name = db.shorten_name(u'timetable_event_instructor')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'timetable.event'], null=False)),
            ('instructor', models.ForeignKey(orm[u'timetable.instructor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'instructor_id'])

        # Removing M2M table for field instructors on 'Event'
        db.delete_table(db.shorten_name(u'timetable_event_instructors'))


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
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Instructor']", 'symmetrical': 'False'}),
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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