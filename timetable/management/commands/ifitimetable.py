from django.core.management.base import BaseCommand, CommandError
from timetable.models import Event, Modul, Parser, Source
from timetable.parser import process

class Command(BaseCommand):
	args = ''
	help = 'Runs the IFIWS13 parser.'

	def handle(self, *args, **options):
		moduls = Modul.objects.count()
		events = Event.objects.count()

		parser = Parser.objects.get(name='ifitimetable')
		for source in Source.objects.filter(parser=parser):
			process.process_source_ifitimetable(source)

		moduls = Modul.objects.count() - moduls
		events = Event.objects.count() - events
		self.stdout.write('Added ' + str(moduls) + ' Module')
		self.stdout.write('Added ' + str(events) + ' Events')