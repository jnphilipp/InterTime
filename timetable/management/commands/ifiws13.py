from django.core.management.base import BaseCommand, CommandError
from timetable.models import Event, Modul
from timetable.parser.parsers import IFIWS13

class Command(BaseCommand):
	args = ''
	help = 'Runs the IFIWS13 parser.'

	def handle(self, *args, **options):
		moduls = Modul.objects.count()
		events = Event.objects.count()
		ifiws13 = IFIWS13()
		ifiws13.fetch()
		moduls = Modul.objects.count() - moduls
		events = Event.objects.count() - events
		self.stdout.write('Added ' + str(moduls) + ' Module')
		self.stdout.write('Added ' + str(events) + ' Events')