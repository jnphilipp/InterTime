# -*- coding: utf-8 -*-

from timetable.models import Department, Event, EventType, FieldOfStudy, Instructor, Location, Modul, ModulFieldOfStudy, Semester, Sportkurs, SportkursEvent
from urllib2 import urlopen
import HTMLParser
import re

class BaseParser(object):
	def fetch(self, url):
		r = urlopen(url)
		encoding = r.headers['content-type'].split('charset=')[-1] if 'charset=' in r.headers['content-type'] else 'iso-8859-1'
		html = unicode(r.read(), encoding)
		r.close

		parser = HTMLParser.HTMLParser()
		text = parser.unescape(html)
		return text

class IFITimetable(BaseParser):
	weekdays =["montags","dienstags","mittwochs","donnerstags","freitags","samstags","sonntags"]

	def fetch(self, url, semester):
		try:
			html = super(IFITimetable, self).fetch(url)
		except:
			return
		department, created = Department.objects.get_or_create(name='Institut für Informatik')

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

				ms = re.finditer(r'<a href="stundenplaene/(ws|ss)\d{4}/(w|s)\d\ddozent.html#.+?>(.+?),(.+?)</a>', header.group(1), flags=re.M|re.S)
				for m in ms:
					instructor, created = Instructor.objects.get_or_create(firstname=m.group(3), lastname=m.group(4))
					instructors.add(instructor)

				m = re.search(r'href="stundenplaene/(ws|ss)\d{4}/(w|s)\d\dstdgang.html#.+?">(.+?)</a>', header.group(1), flags=re.M|re.S)
				if m:
					field, created = FieldOfStudy.objects.get_or_create(name=m.group(3), department=department)

				m = re.search(r'<td nowrap="nowrap">(\d+?). Sem.</td>', header.group(1), flags=re.M|re.S)
				if m:
					modulfield, created = ModulFieldOfStudy.objects.get_or_create(field_of_study=field, semester_numbers=m.group(1))
					for modul in moduls:
						if not modul.fields.filter(id=modulfield.id):
							modul.fields.add(modulfield)

			ms = re.finditer(r'<table class="full s_veranstaltung">.*?(?=<table class="full s_veranstaltung">|</table>\s+</table>)', match.group(1), flags=re.M|re.S)
			for m in ms:
				mm = re.search(r's_termin_titel[^>]*><b>([^<]*)<', m.group(0), flags=re.M|re.S)
				if mm:
					eventname = mm.group(1)

				events = re.finditer(r'<table class="full">.*?(?=</table>|</tr>)', m.group(0), flags=re.M|re.S)
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
					mm = re.search(r'<td class="s_termin_zeit">([^\s<]+)(\s+\([^<\)]+\))?</td>', e.group(0), flags=re.M|re.S)
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
						mms = re.finditer(r'<a href="stundenplaene/(ws|ss)\d{4}/(w|s)\d\ddozent.html#[^>]+>([^,]+), ([^<]+)</a>', mm.group(1), flags=re.M|re.S)
						for mmm in mms:
							event_instructor, created = Instructor.objects.get_or_create(firstname=mmm.group(4), lastname=mmm.group(3))
							event_instructors.add(event_instructor)

					for modul in moduls:
						(event, created) = Event.objects.get_or_create(name=eventname, modul=modul, semester=semester, eventtype=eventtype, begin=event_begin, end=event_end, location=location, weekday=event_weekday, weeknumber=event_weekday2)

						if created:
							event_instructors.union(instructors)
							for instructor in event_instructors:
								event.instructors.add(instructor)
							event.save()


#Hochschulsport
class HSS(BaseParser):
	def fetch(self, url):
		abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		weekdays =["mo","di","mi","do","fr","sa","so"]

		i = 0
		html = super(HSS, self).fetch(url)
		for i in abc:
			inhalt = re.finditer(r'<!-- BEGINN_INHALT_ZFH -->(.+?)(?=<!-- ENDE_INHALT_ZFH -->)', html, flags=re.M|re.S)
			for index in inhalt:
				veranstaltungen = re.finditer(r'href="(_'+i+'.+?.html)', index.group(1), flags=re.M|re.S) # hier nur für alle A-Kurse

				for index2 in veranstaltungen:
					html2 = super(HSS, self).fetch('http://hochschulsport.uni-leipzig.de/angebote/aktueller_zeitraum/'+index2.group(1))

					seiten = re.finditer(r'<!-- BEGINN_INHALT_ZFH -->(.+?)(?=<!-- ENDE_INHALT_ZFH -->)', html2, flags=re.M|re.S)
					for index3 in seiten:
						informationen = re.search(r'bs_head">(.+?)<.+?bs_verantw">verantwortlich: (.+?)<.+?bs_kursbeschreibung.+?<p> (.+?)</p>(.*)', index3.group(1), flags=re.M|re.S)
						if informationen:
							firstname, lastname = informationen.group(2).rsplit(' ', 1)#Verantwortlicher
							instructor, created = Instructor.objects.get_or_create(firstname=firstname, lastname=lastname)

							kurs, created = Sportkurs.objects.get_or_create(name=informationen.group(1))
							if created or not kurs.description:
								kurs.description = re.sub(r'<[^>]+>', '', informationen.group(3))
								kurs.instructor = instructor
								kurs.save()

							events = re.finditer(r'bs_sdet(.+?)(?=bs_sbuch)', informationen.group(4), flags=re.M|re.S)
							for index4 in events:
								event = re.search(r'\'>(.+?)<.+?bs_stag\'>(.+?)</td.+?bs_szeit\'>(.+?)-(.+?)<.+?bs_sort\'>.+?\'.+?\'>(.+?)<.+?bs_szr.+?\'.+?\'>(.+?)<.+?bs_skl\'>(.+?)<', index4.group(1), flags=re.M|re.S)
								if event:
									firstname, lastname = event.group(7).rsplit(' ', 1)#Lehrer/Leiter
									einstructor, created = Instructor.objects.get_or_create(firstname=firstname, lastname=lastname)
									location, created = Location.objects.get_or_create(room=event.group(5))

									wd = event.group(2)
									if '<br />' in event.group(2):
										wd = event.group(2).split('<br />')[0]

									weekday = weekdays.index(str.lower(str(wd)))
									spevent, created = SportkursEvent.objects.get_or_create(kurs=kurs, details=event.group(1), weekday=weekday, begin=event.group(3), end=event.group(4), location=location)
									#print event.group(6) #Zeitraum