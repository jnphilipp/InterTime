# -*- coding: utf-8 -*-

from timetable.models import Department, Event, EventType, FieldOfStudy, Instructor, Location, Modul, ModulFieldOfStudy, Semester
from urllib2 import urlopen
import HTMLParser
import re

class BaseParser(object):
	def fetch(self, url):
		r = urlopen(url)
		encoding = r.headers['content-type'].split('charset=')[-1]
		html = unicode(r.read(), encoding)
		r.close

		parser = HTMLParser.HTMLParser()
		text = parser.unescape(html)
		return text

class IFIWS13(BaseParser):
	weekdays =["montags","dienstags","mittwochs","donnerstags","freitags","samstags","sonntags"]

	def fetch(self):
		html = super(IFIWS13, self).fetch('http://www.informatik.uni-leipzig.de/ifi/studium/stundenplan/ws2013/w13stdgang.html')
		department, created = Department.objects.get_or_create(name='Institut für Informatik')
		semester, created = Semester.objects.get_or_create(name='Wintersemester')


		matchs = re.finditer(r'<!--###s_modul### begin -->(.+?)(?=<!--###s_modul### end -->)', html, flags=re.M|re.S)
		for match in matchs:
			moduls = set()
			instructors = set()
			header = re.search(r'<table class="full border s_modul_head">(.+?)(?=</table>)', match.group(1), flags=re.M|re.S)
			if header:
				ms = re.finditer(r'name="(\d[^"]+?)">', header.group(1), flags=re.M|re.S)
				numbers = set()
				for m in ms:
					numbers.add(m.group(1))

				name = ''
				m = re.search('<td align="center">(<a[^>]+>)?<b>(.+?)</b>', header.group(1), flags=re.M|re.S)
				if m:
					name = m.group(2)

				for number in numbers:
					modul, created = Modul.objects.get_or_create(number=number)
					if created:
						modul.name = name
						modul.department = department
						modul.save()
					moduls.add(modul)

				if len(numbers) == 0:
					modul, created = Modul.objects.get_or_create(number=None, name=name)
					if created:
						modul.department = department
						modul.save()
					moduls.add(modul)

				if not len(moduls) > 0:
					continue

				ms = re.finditer(r'<a href="studium/stundenplan/ws2013/w13dozent.html#.+?>(.+?),(.+?)</a>', header.group(1), flags=re.M|re.S)
				for m in ms:
					instructor, created = Instructor.objects.get_or_create(firstname=m.group(2), lastname=m.group(1))
					instructors.add(instructor)

				m = re.search(r'href="studium/stundenplan/ws2013/w13stdgang.html#.+?">(.+?)</a>', header.group(1), flags=re.M|re.S)
				if m:
					field, created = FieldOfStudy.objects.get_or_create(name=m.group(1), department=department)

				m = re.search(r'<td nowrap="nowrap">(\d+?). Sem.</td>', header.group(1), flags=re.M|re.S)
				if m:
					modulfield, created = ModulFieldOfStudy.objects.get_or_create(field_of_study=field, semester_numbers=m.group(1))
					for modul in moduls:
						if not modul.fields.filter(id=modulfield.id):
							modul.fields.add(modulfield)

			ms = re.finditer(r'<table class="full s_veranstaltung">.*?(?=<table class="full s_veranstaltung">)', match.group(1), flags=re.M|re.S)
			for m in ms:
				mm = re.search(r's_termin_titel[^>]*><b>([^<]*)<', m.group(0), flags=re.M|re.S)
				if mm:
					eventname = mm.group(1)

				events = re.finditer(r'<table class="full">.*?(?=</table>)', m.group(0), flags=re.M|re.S)
				for e in events:
					mm = re.search(r'<td class="s_termin_typ">([^<]*)</td>', e.group(0), flags=re.M|re.S)
					if mm:
						eventtype, created = EventType.objects.get_or_create(name=mm.group(1))
					mm = re.search(r'<td class="s_termin_von">(\d\d?:\d\d)</td>', e.group(0), flags=re.M|re.S)
					if mm:
						event_begin = mm.group(1)
					mm = re.search(r'<td class="s_termin_bis">(\d\d?:\d\d)</td>', e.group(0), flags=re.M|re.S)
					if mm:
						event_end = mm.group(1)
					mm = re.search(r'<td class="s_termin_zeit">([^ <]+)\s?\(?([^<\)]+)?</td>', e.group(0), flags=re.M|re.S)
					if mm:
						try:
							event_weekday = self.weekdays.index(mm.group(1))
						except:
							event_weekday = None
						event_weekday2 = mm.group(2)
					mm = re.search(r'<td class="s_termin_raum">([^<,]+),?\s?([^<]+)?</td>', e.group(0), flags=re.M|re.S)
					if mm:
						if mm.group(2) == None:
							location, created = Location.objects.get_or_create(room=mm.group(1))
						else:
							location, created = Location.objects.get_or_create(room=mm.group(2), building=mm.group(1))

					event_instructors = set()
					mm = re.search(r'<td class="s_termin_dozent">(.+?)</td>', e.group(0), flags=re.M|re.S)
					if mm:
						mms = re.finditer(r'<a href="studium/stundenplan/ws2013/w13dozent.html#[^>]+>([^,]+), ([^<]+)</a>', mm.group(1), flags=re.M|re.S)
						for mmm in mms:
							event_instructor, created = Instructor.objects.get_or_create(firstname=mmm.group(2), lastname=mmm.group(1))
							event_instructors.add(event_instructor)

					for modul in moduls:
						(event, created) = Event.objects.get_or_create(name=eventname, modul=modul, semester=semester, eventtype=eventtype, begin=event_begin, end=event_end, location=location, weekday=event_weekday, weeknumber=event_weekday2)

						if created:
							event_instructors.union(instructors)
							for instructor in event_instructors:
								event.instructors.add(instructor)
							event.save()