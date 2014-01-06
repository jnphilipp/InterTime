from django.core.management.base import BaseCommand, CommandError
from timetable.models import Event, Modul
from timetable.parser.ba import PdfparserBA

class Command(BaseCommand):
	args = ''
	help = 'Runs the PdfparserBA parser.'

	def handle(self, *args, **options):
		moduls = Modul.objects.count()
		events = Event.objects.count()
		ifiws13 = PdfparserBA()
		ifiws13.fetch()
		moduls = Modul.objects.count() - moduls
		events = Event.objects.count() - events
		self.stdout.write('Added ' + str(moduls) + ' Module')
		self.stdout.write('Added ' + str(events) + ' Events')
