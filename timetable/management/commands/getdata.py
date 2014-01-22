from django.core.management.base import BaseCommand, CommandError
from timetable.models import Event, Modul, Source, Sportkurs, SportkursEvent
from timetable.parser import process

class Command(BaseCommand):
	args = ''
	help = 'Parser all sources.'

	def handle(self, *args, **options):
		kurse = Sportkurs.objects.count()
		sevents = SportkursEvent.objects.count()
		modul = Modul.objects.count()
		events = Event.objects.count()

		for source in Source.objects.all():
			process.process_source(source)

		kurse = Sportkurs.objects.count() - kurse
		sevents = SportkursEvent.objects.count() - sevents
		modul = Modul.objects.count() - modul
		events = Event.objects.count() - events

		self.stdout.write('Added ' + str(kurse) + ' Kurse.')
		self.stdout.write('Added ' + str(sevents) + ' Sporkurs events.')
		self.stdout.write('Added ' + str(kurse) + ' Module.')
		self.stdout.write('Added ' + str(events) + ' Events.')