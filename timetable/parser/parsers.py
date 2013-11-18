# -*- coding: utf-8 -*-

from timetable.models import Deparment, Modul
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

		matchs = re.finditer(r'<table.+?s_modul_head.+?<a.+?>(\d[^<>]+?)</a>.+?<b>(.+?)</b>.+?</table>', html, flags=re.M|re.S)
		for match in matchs:
			Modul(number=match.group(1), name=match.group(2), deparment=deparment).save()