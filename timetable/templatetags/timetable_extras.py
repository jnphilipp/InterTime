from django.template import Library
from timetable.models import Modul, SportkursEvent
register = Library()

@register.filter
def convert_weekday(weekday):
	if weekday == 0 or weekday == '0':
		return "Montag"
	elif weekday == 1 or weekday == '1':
		return "Dienstag"
	elif weekday==2 or weekday == '2':
		return "Mittwoch"
	elif weekday==3 or weekday == '3':
		return "Donnerstag"
	elif weekday==4 or weekday == '4':
		return "Freitag"
	elif weekday==5 or weekday == '5':
		return "Samstag"
	elif weekday==6 or weekday == '6':
		return "Sonntag"
	else:
		return ""

@register.filter
def module(semester):
	return Modul.objects.all().order_by('name').filter(event__semester=semester).filter(number__isnull=False).distinct()

@register.filter
def spmodule(name):
	return SportkursEvent.objects.all().order_by('kurs').filter(kurs__name=name).filter(id__isnull=False).distinct()

@register.filter
def events(modul, semester):
	return modul.event_set.filter(semester=semester)
