from django.template import Library

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
