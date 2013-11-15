from django.shortcuts import get_object_or_404, get_list_or_404, render
from timetable.models import Modul

def index(request):
	moduls = get_list_or_404(Modul.objects.order_by('number'))

	return render(request, 'timetable/index.html', {'moduls':moduls})

def details(request, modul_id):
	modul = get_object_or_404(Modul, pk=modul_id)

	return render(request, 'timetable/details.html', {'modul': modul})