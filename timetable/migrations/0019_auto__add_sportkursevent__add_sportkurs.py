# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SportkursEvent'
        db.create_table(u'timetable_sportkursevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('kurs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Sportkurs'])),
            ('details', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('weekday', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('begin', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('begin_day', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_day', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Location'], null=True)),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Instructor'], null=True)),
        ))
        db.send_create_signal(u'timetable', ['SportkursEvent'])

        # Adding model 'Sportkurs'
        db.create_table(u'timetable_sportkurs', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2048, blank=True)),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetable.Instructor'], blank=True)),
        ))
        db.send_create_signal(u'timetable', ['Sportkurs'])


    def backwards(self, orm):
        # Deleting model 'SportkursEvent'
        db.delete_table(u'timetable_sportkursevent')

        # Deleting model 'Sportkurs'
        db.delete_table(u'timetable_sportkurs')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'timetable.department': {
            'Meta': {'object_name': 'Department'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'timetable.event': {
            'Meta': {'object_name': 'Event'},
            'begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'eventtype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.EventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Instructor']", 'symmetrical': 'False'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Location']", 'null': 'True'}),
            'modul': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Modul']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'semester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Semester']"}),
            'weekday': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'weeknumber': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'timetable.eventtype': {
            'Meta': {'object_name': 'EventType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'timetable.fieldofstudy': {
            'Meta': {'object_name': 'FieldOfStudy'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Department']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'timetable.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'timetable.location': {
            'Meta': {'unique_together': "(('building', 'room'),)", 'object_name': 'Location'},
            'building': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'timetable.modul': {
            'Meta': {'object_name': 'Modul'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.ModulFieldOfStudy']", 'null': 'True', 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lp': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modultype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.ModulType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '256', 'unique': 'True', 'null': 'True'})
        },
        u'timetable.modulfieldofstudy': {
            'Meta': {'object_name': 'ModulFieldOfStudy'},
            'field_of_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.FieldOfStudy']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester_numbers': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '256', 'null': 'True'})
        },
        u'timetable.modultype': {
            'Meta': {'object_name': 'ModulType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1024'})
        },
        u'timetable.selection': {
            'Meta': {'object_name': 'Selection'},
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.Event']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Student']"})
        },
        u'timetable.semester': {
            'Meta': {'object_name': 'Semester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'timetable.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'regex': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'timetable.sportkurs': {
            'Meta': {'object_name': 'Sportkurs'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Instructor']", 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256'})
        },
        u'timetable.sportkursevent': {
            'Meta': {'object_name': 'SportkursEvent'},
            'begin': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'begin_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
            'end': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'end_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Instructor']", 'null': 'True'}),
            'kurs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Sportkurs']"}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timetable.Location']", 'null': 'True'}),
            'weekday': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'timetable.student': {
            'Meta': {'object_name': 'Student'},
            'current_semester': ('django.db.models.fields.IntegerField', [], {}),
            'field_of_studies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['timetable.FieldOfStudy']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['timetable']