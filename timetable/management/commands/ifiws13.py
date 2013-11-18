from django.core.management.base import BaseCommand, CommandError
from timetable.models import Modul
from timetable.parser.parsers import IFIWS13

class Command(BaseCommand):
	args = ''
	help = 'Runs the IFIWS13 parser.'

	def handle(self, *args, **options):
		count = Modul.objects.count()
		ifiws13 = IFIWS13()
		ifiws13.fetch()
		ncount = Modul.objects.count()
		self.stdout.write('Added ' + str(ncount - count) + ' Module')