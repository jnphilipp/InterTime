from django.core.management.base import BaseCommand, CommandError
from timetable.models import Parser, Source, Sportkurs, SportkursEvent
from timetable.parser import process

class Command(BaseCommand):
	args = ''
	help = 'Runs the IFIWS13 parser.'

	def handle(self, *args, **options):
		kurse = Sportkurs.objects.count()
		events = SportkursEvent.objects.count()

		parser = Parser.objects.get(name='hss')
		for source in Source.objects.filter(parser=parser):
			process.process_source_hss(source)

		kurse = Sportkurs.objects.count() - kurse
		events = SportkursEvent.objects.count() - events
		self.stdout.write('Added ' + str(kurse) + ' Kurse')
		self.stdout.write('Added ' + str(events) + ' Events')