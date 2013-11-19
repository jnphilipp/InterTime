# -*- coding: utf-8 -*-

from timetable.models import Deparment, Event, EventType, Instructor, Modul, Semester
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
		text =parser.unescape(html)
		return text

class IFIWS13(BaseParser):
	def fetch(self):
		html = super(IFIWS13, self).fetch('http://www.informatik.uni-leipzig.de/ifi/studium/stundenplan/ws2013/w13stdgang.html')
		deparment, created = Deparment.objects.get_or_create(name='Institut für Informatik')
		semester, created = Semester.objects.get_or_create(name='Wintersemester')

		#matchs = re.finditer(r'<table.+?s_modul_head.+?<a.+?>(\d[^<>]+?)</a>.+?<b>(.+?)</b>.+?</table>', html, flags=re.M|re.S)
		matchs = re.finditer(r'<!--###s_modul### begin -->.+?name="(\d.+?)">.+?<td align="center"><b>(.+?)</b>.+?<b><i><a href="studium/stundenplan/ws2013/w13dozent.html#.+?>(.+?),(.+?)</a></i></b>.+?href="studium/stundenplan/ws2013/w13stdgang.html#.+?">(.+?)\.(.+?)</a></td><td></td><td nowrap="nowrap">(.+?). Sem.</td>.+?("s_termin_typ">.+?)<!--###s_modul### end -->', html, flags=re.M|re.S)
		for match in matchs:
			modul, created = Modul.objects.get_or_create(number=match.group(1), name=match.group(2), deparment=deparment)
			modul.save()
			#Instructor(firstname=match.group(3), lastname=match.group(4)).save()
			#print "Modulnummer: "+match.group(1)+", Modulname: "+match.group(2)
			#print "Modulverantwortlicher: Vorname: "+match.group(3)+", Nachname: "+match.group(4)
			#print "Studiengang: "+match.group(5)+", Abschluss: "+match.group(6)+", Semester: "+match.group(7)
			lst = []
			lst = match.group(8).split('"s_termin_typ">')
			for index in lst: 
				m = re.search(r'(.+?)</td>.+?"s_termin_von">(\d{1,2}:\d\d)</td>.+?"s_termin_bis">(\d{1,2}:\d\d)</td>.+?"s_termin_zeit">(.+?)</td>.+?"s_termin_raum">(.+?)</td>.+?"s_termin_dozent"><a href="studium/stundenplan/ws2013/w13dozent.html#.+?>(.+?)</a>', index, flags=re.M|re.S)
				if m:
					eventtype, created = EventType.objects.get_or_create(name=m.group(1))
					Event(modul=modul, semester=semester, eventtype=eventtype, begin=m.group(2), end=m.group(3)).save()
					#print "Veranstaltungsart: "+m.group(1)+" von "+m.group(2)+" bis "+m.group(3)+", Wochentag: "+m.group(4)+", Raum: "+m.group(5)+", Dozent: "+m.group(6)
			#print 
