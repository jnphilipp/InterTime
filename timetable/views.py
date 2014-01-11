from datetime import timedelta
from django.shortcuts import get_object_or_404, get_list_or_404, render
from timetable.models import Department, Event, Modul, Semester, Sportkurs

def index(request):
	return render(request, 'index.html')

def moduls(request):
	moduls = Modul.objects.all().order_by('number')
	return render(request, 'timetable/index.html', {'moduls':moduls})

def details(request, modul_id):
	modul = get_object_or_404(Modul, pk=modul_id)
	return render(request, 'timetable/details.html', {'modul': modul})

def departments(request):
	departments = Department.objects.all().order_by('name')
	return render(request, 'timetable/departments.html', {'departments':departments})

def department_details(request, department_id):
	department = get_object_or_404(Department, pk=department_id)
	return render(request, 'timetable/department_details.html', {'department': department})

def plan(request):
	semesters = Semester.objects.all().order_by('name')
	kurse = Sportkurs.objects.all().order_by('name')
	return render(request, 'timetable/plan.html', locals())

def timetable(request):
	req = request.GET.get('events')
	events = Event.objects.filter(id__in=req.split(',') if req else '').filter(weekday__isnull=False).order_by('weekday')
	event_list = []
	for event in events:
		duration = timedelta(hours=event.end.hour - event.begin.hour, minutes=event.end.minute - event.begin.minute)
		seconds = duration.total_seconds()
		hours = seconds // 3600
		minutes = (seconds % 3600) // 60 / 60
		title = '%s (%s - %s)' % (event.name, event.begin, event.end)
		event_list.append('<li class="tt-event btn-success" data-id="%s" data-day="%s" data-start="%s" data-duration="%s" rel="tooltip" unselectable="on" style="-moz-user-select: none; height: 36px; top: 224px; left: 0px; width: 414px;" data-original-title="%s">%s</li>' % (event.id, event.weekday, (event.begin.hour - 7) + (event.begin.minute / 60.0), hours + minutes, title, title))

	own_events = request.GET.get('own').split('#')
	for oevent in own_events:
		if not oevent:
			name,day,begin,end = oevent.split(';')
			beginh,beginm = begin.split(':')
			endh,endm = end.split(':')

			duration = timedelta(hours=endh - beginh, minutes=endm - beginm)
			seconds = duration.total_seconds()
			hours = seconds // 3600
			minutes = (seconds % 3600) // 60 / 60
			title = '%s (%s - %s)' % (name, begin, end)
			event_list.append('<li class="tt-event btn-success" data-id="%s" data-day="%s" data-start="%s" data-duration="%s" rel="tooltip" unselectable="on" style="-moz-user-select: none; height: 36px; top: 224px; left: 0px; width: 414px;" data-original-title="%s">%s</li>' % (123, day, (beginh - 7) + (beginm / 60.0), hours + minutes, title, title))		
			
	return render(request, 'timetable/timetable.html', locals())
