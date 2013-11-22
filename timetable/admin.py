from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import TextInput
from django.db import models
from timetable.models import Deparment, Event, EventType, FieldOfStudy, Location, Instructor, Modul, ModulType, ModulFieldOfStudy, Selection, Semester, Source, Student

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
		(None, {'fields': ['number', 'name', 'lp', 'modultype', 'description']}),
		('Field of Study', {'fields': ['deparment', 'fields']}),
	]
	filter_horizontal = ('fields',)

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

class LocationAdmin(admin.ModelAdmin):
	list_display = ('building','room')
	search_fields = ('building','room')
	ordering = ('building','room')

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['building', 'room']}),
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
		('Course informations', {'fields': ['semester_numbers']}),
		('Time', {'fields': ['weekday', 'begin', 'end', 'semester', 'location']}),
		('Instructors', {'fields': ['instructors']}),
	]

	filter_horizontal = ('instructors',)

class StudentAdmin(admin.ModelAdmin):
	list_display = ('user',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	filter_horizontal = ('field_of_studies',)

class SelectionAdmin(admin.ModelAdmin):
	filter_horizontal = ('events',)

class StudentInline(admin.StackedInline):
	model = Student
	can_delete = False
	filter_horizontal = ('field_of_studies',)

class UserAdmin(UserAdmin):
	inlines = (StudentInline, )

admin.site.register(Deparment, DeparmentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType)
admin.site.register(FieldOfStudy)
admin.site.register(Location, LocationAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Modul, ModulAdmin)
admin.site.register(ModulFieldOfStudy)
admin.site.register(ModulType, ModulTypeAdmin)
admin.site.register(Selection, SelectionAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(Student, StudentAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)