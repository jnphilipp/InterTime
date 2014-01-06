# -*- coding: utf-8 -*-
#!/usr/bin/python
import os, sys, re

from urllib2 import urlopen
from timetable.models import Department, Event, EventType, FieldOfStudy, Instructor, Location, Modul, ModulFieldOfStudy, Semester, ModulType


class PdfparserBA():


	def fetch(self):

		department, created = Department.objects.get_or_create(name='Institut für Informatik')


		r = urlopen('http://www.informatik.uni-leipzig.de/ifi/studium/studiengnge/ba-inf/ba-inf-module.html')
		with open('/tmp/ba-inf.pdf', 'w') as f:
			f.write(r.read())
		os.system('/usr/local/bin/pdf2txt.py -o /tmp/a.out /tmp/ba-inf.pdf');

		fobj = open("/tmp/a.out", "r")

		counter=0
		counter2 =0
		founddate=0

		index=1
		flag=0
		flagInhalt=0

		liste = []
		liste2 = []
		titles =[]
		numbers=[]

		letzteZeile='leer' 
		fobj_out = open("test.txt","w")
		fobj_out.write( "hhall")

		title=''
		lp='0'
		inhalt=''
		modultype=''

		for line in fobj: 
			liste.insert(counter, line)
			counter+=1
	

			#modulnummer
			if counter==1:
				number=line
				fobj_out.write( str(counter2)+line)
				#print line

			#modulform
		#	if counter==4: print line	


			#Leistungspunkte
			if '5 LP = 150 Arbeitsstunden (Workload)' in line:index+=1; lp='5'
			if '10 LP = 300 Arbeitsstunden (Workload)' in line:index+=1; lp='10'

			#modultitel bachelor
			if '. Semester'in line: 
				fobj_out.write( letzteZeile);title=letzteZeile
				#print letzteZeile

			#inhalt
			if line.strip() == 'Teilnahmevoraus-': flagInhalt=0
			if flagInhalt==1: inhalt += line
			if line.strip() =='Inhalt': flagInhalt=1


			#???if counter==20: print line	#institut

			letzteZeile=line

			#str = line
			match = re.search(r'\d\d?\.\s\w+\s\d{4}', line)
			# If-statement after search() tests if it succeeded
			#if match:                      
				#print 'found', match.group() ## 'found word:cat'
				#founddate+=1
				#print founddate

			if 'Vertiefungsmodul'==line.strip(): modultype='Vertiefungsmodul'
			if 'Ergänzungsfach'==line.strip(): modultype='Ergänzungsfach'
			if 'Kernmodul'==line.strip(): modultype='Kernmodul'
			if 'Seminarmodul'==line.strip(): modultype='Seminarmodul'
			if 'Ergänzungsfach Medizinische Informatik'==line.strip(): modultype='Ergänzungsfach Medizinische Informatik'


			#neuer eintrag
			if 'Modulnummer' in line:
				flag+=1

				#if index != flag: print title+ str(index) + ' '+str(flag)
				#print lp
		
				#print inhalt

				counter=0
				liste2=liste
				liste[:]=[]
				#print title
				if counter2>0:
					titles.append(title.strip()	)
					numbers.append(number.strip())
					#print titles[counter2-1]+numbers[counter2-1]
				counter2+=1


				type, created = ModulType.objects.get_or_create(name=modultype)

				modul, created = Modul.objects.get_or_create(number=number)	
				#if created:
				modul.name = title.strip()
				modul.lp=int(lp)
				modul.modultype=type
				modul.description=inhalt
				modul.department = department
				#modul.fields='no clue what that is'
				modul.save()






				title=''
				number=''
				lp='0'
				inhalt=''
				modultype=''



		#letztes Modul noch hinzufuegen
		#
		#


		#print titles[0]+' xx '+numbers[0]
		#print len(titles)

		#m = Modul(number=nummer, name=..., )
		#m.save()

		#print len(numbers)
		#print index

		fobj.close()
		fobj_out.close()
