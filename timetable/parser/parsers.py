# -*- coding: utf-8 -*-

from timetable.models import Deparment, Event, EventType, FieldOfStudy, Instructor, Location, Modul, ModulFieldOfStudy, Semester
import HTMLParser
import re
from urllib2 import urlopen

class BaseParser(object):
	def fetch(self, url):
		r = urlopen(url)
		encoding = r.headers['content-type'].split('charset=')[-1]
		html = unicode(r.read(), encoding)
		r.close

		parser = HTMLParser.HTMLParser()
		text = parser.unescape(html)
		return text

class IFIWS13(BaseParser):#Module ohne Modulnummer werden nicht aufgenommen
	def fetch(self):
		html = super(IFIWS13, self).fetch('http://www.informatik.uni-leipzig.de/ifi/studium/stundenplan/ws2013/w13stdgang.html')
		deparment, created = Deparment.objects.get_or_create(name='Institut für Informatik')
		semester, created = Semester.objects.get_or_create(name='Wintersemester')

		matchs = re.finditer(r'<!--###s_modul### begin -->.+?name="(\d.+?)">.+?<td align="center"><b>(.+?)</b>.+?<b><i><a href="studium/stundenplan/ws2013/w13dozent.html#.+?>(.+?),(.+?)</a></i></b>.+?href="studium/stundenplan/ws2013/w13stdgang.html#.+?">(.+?)\.(.+?)</a></td><td></td><td nowrap="nowrap">(.+?). Sem.</td>.+?("s_termin_typ">.+?)<!--###s_modul### end -->', html, flags=re.M|re.S)
		for match in matchs:

			#print "Modulverantwortlicher: Vorname: "+match.group(3)+", Nachname: "+match.group(4)

			#print "Modulnummer: "+match.group(1)+", Modulname: "+match.group(2)
			modul, created = Modul.objects.get_or_create(number=match.group(1), name=match.group(2), deparment=deparment)
			modul.save()

			# Abkürzungen eleminieren
			a = match.group(5)
			if "LA" in a:
				a = "Lehramt"
			if "Inf" in a:
				a = "Informatik"

			#print "Studiengang: "+a+", Abschluss: "+match.group(6)+", Semester: "+match.group(7)
			field, created = FieldOfStudy.objects.get_or_create(name=match.group(5), deparment=deparment)
			modulfield, created = ModulFieldOfStudy.objects.get_or_create(field_of_study=field, semester_numbers=match.group(7))
			modulfield.save()
			modul.fields.add(modulfield)

			lst = []
			lst = match.group(8).split('"s_termin_typ">')
			for index in lst: 
				m = re.search(r'(.+?)</td>.+?"s_termin_von">(\d{1,2}:\d\d)</td>.+?"s_termin_bis">(\d{1,2}:\d\d)</td>.+?"s_termin_zeit">(.+?) (.+?)</td>.+?"s_termin_raum">(SG|Hs|.+?,)(.+?)</td>.+?"s_termin_dozent"><a href="studium/stundenplan/ws2013/w13dozent.html#.+?>(.+?),(.+?)</a>', index, flags=re.M|re.S)
				if m:
					#print "Veranstaltungsart: "+m.group(1)
					eventtype, created = EventType.objects.get_or_create(name=m.group(1))

					# Abkürzungen eleminieren
					g = m.group(6)
					if "SG" in m.group(6):
						g = "Seminargebaeude"
					if "Hs" in m.group(6):
						g = "Hoersaalgebaeude"						

					# Komma hinter Gebäudennamen entfernen
					if "," in g:
						g = g[:-1]

					# Prüfung ob Raumnummer vorhanden
					r = m.group(7)
					number =["0","1","2","3","4","5","6","7","8","9"]
					flag = -1
					for index2 in number:
						if (index2 in r):
							flag = 1
							break
						else:
							flag = 0

					if flag == 0:
						g = g+", "+r
						r = ""

					#print "Gebaeude: "+g+", Raum: "+r
					location, created = Location.objects.get_or_create(building=g, room=r)

					#print "Dozent: "+m.group(8)+", "+m.group(9)
					instructor, created = Instructor.objects.get_or_create(firstname=m.group(9), lastname=m.group(8))

					# Umwandlung Wochentag in Integer
					day = m.group(4)
					weekdays =["montags","dienstags","mittwochs","donnerstags","freitags","samstags","sonntags"]
					i = 0
					for index3 in weekdays:
						i+=1
						if day in index3:
							break

					#print i
					#print  "von "+m.group(2)+" bis "+m.group(3)+", Wochentag: "+day+" ,Zusatz: "+m.group(5) 
					event = Event(modul=modul, semester=semester, eventtype=eventtype, begin=m.group(2), end=m.group(3) ,location=location, weekday=i, weeknumber=m.group(5))
					event.save()
					event.instructors.add(instructor)
			print "..."
		print Parser_IFIWS13_done
