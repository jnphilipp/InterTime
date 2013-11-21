from django.shortcuts import get_object_or_404, get_list_or_404, render
from timetable.models import Modul
from timetable.models import Deparment


def index(request):
    return render(request, 'index.html')


def moduls(request):
	moduls = Modul.objects.all().order_by('number')
	return render(request, 'timetable/index.html', {'moduls':moduls})

def details(request, modul_id):
    modul = get_object_or_404(Modul, pk=modul_id)
    return render(request, 'timetable/details.html', {'modul': modul})

def departments(request):
	departments = Deparment.objects.all().order_by('name')
	return render(request, 'timetable/departments.html', {'departments':departments})

def department_details(request, department_id):
    department = get_object_or_404(Deparment, pk=department_id)
    return render(request, 'timetable/department_details.html', {'department': department})

def plan(request):
    return render(request, 'timetable/plan.html')
