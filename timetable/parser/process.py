from timetable.models import Parser, Semester
from timetable.parser.htmlparsers import IFITimetable, HSS
from timetable.parser.pdfparsers import BAInfParser, MAInfParser

import datetime
import re

def process_source(source):
	try:
		if source.parser == Parser.objects.get(name='ifitimetable'):
			process_source_ifitimetable(source)
		elif source.parser == Parser.objects.get(name='ifipdfs'):
			process_source_ifipdfs(source)
		elif source.parser == Parser.objects.get(name='hss'):
			process_source_hss(source)
	except Parser.DoesNotExist, e:
		print 'Parser does not exist: %s' % e

def process_source_ifitimetable(source):
	try:
		ws = Semester.objects.get(name='Wintersemester')
		ss = Semester.objects.get(name='Sommersemester')
		if source.regex:
			urls = regex_url(source.source)
			for url in urls:
				if '/ss' in url:
					semester = ss
				elif '/ws' in url:
					semester = ws
				ifi = IFITimetable()
				ifi.fetch(url, semester)
		else:
			if '/ss' in source.source:
				semester = ss
			elif '/ws' in url:
				semester = ws
			ifi = IFITimetable()
			ifi.fetch(source.source, semester)
	except Semester.DoesNotExist, e:
		print 'Semester does not exist: %s' % e

def process_source_ifipdfs(source):
	if source.regex:
		urls = regex_url(source.source)
		for url in urls:
			if 'ba' in url:
				ba = BAInfParser()
				ba.fetch(url)
			elif 'ma' in url:
				ma = MAInfParser()
				ma.fetch(url)
	else:
		if 'ba' in source.source:
			ba = BAInfParser()
			ba.fetch(source.source)
		elif 'ma' in source.source:
			ma = MAInfParser()
			ma.fetch(source.source)

def process_source_hss(source):
	if source.regex:
		urls = regex_url(source.source)
		for url in urls:
			hss = HSS()
			hss.fetch(url)
	else:
		hss = HSS()
		hss.fetch(source.source)

def regex_url(url):
	match = re.findall(r'\[([^\]]+)\]', url, flags=re.M)
	urls = []

	if match:
		for i in range(0, len(match[0].split('|'))):
			urls.append(url)

		for i in range(len(urls)):
			for m in match:
				urls[i] = re.sub(re.escape('[' + m + ']'), m.split('|')[i], urls[i])

	year = datetime.datetime.now().year
	prevyear = (datetime.datetime.now().year - 1)
	urls2 = []
	for url in urls:
		u = re.sub(r'\(yyyy\)', str(year), url)
		urls2.append(re.sub(r'\(yy\)', str(year % 100), u))
		u = re.sub(r'\(yyyy\)', str(prevyear), url)
		urls2.append(re.sub(r'\(yy\)', str(prevyear % 100), u))

	return set(urls2)