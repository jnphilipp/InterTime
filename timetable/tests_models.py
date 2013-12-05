# -*- coding: utf-8 -*-

from django.test import TestCase
from timetable.models import Department, Modul, ModulType, Semester

class ModelsTestCase(TestCase):
	def setUp(self):
		ModulType.objects.create(name='Kernmodul')
		ModulType.objects.create(name='Vertiefungsmodul')
		Department.objects.create(name='Institut für Informatik')
		Department.objects.create(name='Institut für Mathematik')

	def test_modultype_exist(self):
		self.assertEqual(ModulType.objects.all().count(), 2)

	def test_department_exist(self):
		self.assertEqual(Department.objects.all().count(), 2)

	def test_semester_exist(self):
		self.assertEqual(Semester.objects.all().count(), 2)