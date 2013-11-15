from django.contrib import admin
from django.forms import TextInput
from django.db import models
from timetable.models import Modul

class ModulAdmin(admin.ModelAdmin):
	list_display = ('name',)

	formfield_overrides = {
		models.CharField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['number', 'name']}),
	]

admin.site.register(Modul, ModulAdmin)