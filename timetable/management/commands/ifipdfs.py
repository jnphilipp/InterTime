from django.core.management.base import BaseCommand, CommandError
from timetable.models import Event, Modul
from timetable.parser.pdfparsers import BAInfParser, MAInfParser

class Command(BaseCommand):
	args = ''
	help = 'Runs the ifi pdfparsers parser.'

	def handle(self, *args, **options):
		moduls = Modul.objects.count()
		events = Event.objects.count()
		ba = BAInfParser()
		ba.fetch()
		ma = AInfParser()
		ma.fetch()
		moduls = Modul.objects.count() - moduls
		events = Event.objects.count() - events
		self.stdout.write('Added ' + str(moduls) + ' Module')
		self.stdout.write('Added ' + str(events) + ' Events')