from django.contrib import admin
from django.forms import TextInput
from django.db import models
from timetable.models import Deparment, Event, EventType, Instructor, Modul, ModulType, Semester, Source

class SourceAdmin(admin.ModelAdmin):
	list_display = ('url', 'regex')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		('URL', {'fields': ['url', 'regex']}),
	]

class ModulTypeAdmin(admin.ModelAdmin):
	list_display = ('name',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['name']}),
	]

class DeparmentAdmin(admin.ModelAdmin):
	list_display = ('name',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['name']}),
	]

class ModulAdmin(admin.ModelAdmin):
	list_display = ('number', 'name',)
	search_fields = ('number', 'name')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['number', 'name', 'lp', 'modultype', 'description', 'deparment']}),
	]

class InstructorAdmin(admin.ModelAdmin):
	list_display = ('lastname', 'firstname', 'title')
	search_fields = ('lastname', 'firstname')
	ordering = ('lastname', 'firstname')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['title', 'firstname', 'lastname']}),
	]

class SemesterAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	ordering = ('name',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['name']}),
	]

class EventAdmin(admin.ModelAdmin):
	list_display = ('name', 'modul', 'semester', 'get_instructors')
	search_fields = ('name', 'modul')
	ordering = ('name', 'modul')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['name', 'eventtype', 'modul']}),
		('Time', {'fields': ['weekday', 'begin', 'end', 'semester']}),
		('Instructors', {'fields': ['instructors']}),
	]

	filter_horizontal = ('instructors',)

admin.site.register(EventType)
admin.site.register(Source, SourceAdmin)
admin.site.register(ModulType, ModulTypeAdmin)
admin.site.register(Deparment, DeparmentAdmin)
admin.site.register(Modul, ModulAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Event, EventAdmin)