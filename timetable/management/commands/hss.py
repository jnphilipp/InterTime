from django.core.management.base import BaseCommand, CommandError
from timetable.models import Sportkurs, SportkursEvent
from timetable.parser.htmlparsers import HSS

class Command(BaseCommand):
	args = ''
	help = 'Runs the IFIWS13 parser.'

	def handle(self, *args, **options):
		kurse = Sportkurs.objects.count()
		events = SportkursEvent.objects.count()
		hss = HSS()
		hss.fetch()
		kurse = Sportkurs.objects.count() - kurse
		events = SportkursEvent.objects.count() - events
		self.stdout.write('Added ' + str(kurse) + ' Kurse')
		self.stdout.write('Added ' + str(events) + ' Events')