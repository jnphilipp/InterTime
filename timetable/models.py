from django.contrib.auth.models import User
from django.db import models

class Source(models.Model):
	url = models.CharField(max_length=1024, blank=True, null=True)
	regex = models.CharField(max_length=1024, blank=True, null=True)

	def __unicode__(self):
		if self.url:
			return self.url 
		elif self.regex:
			return self.regex
		else:
			return self.id

class ModulType(models.Model):
	name = models.CharField(max_length=1024, unique=True)

	def __unicode__(self):
		return self.name

class Department(models.Model):
	name = models.CharField(max_length=256, unique=True)

	def __unicode__(self):
		return self.name

class FieldOfStudy(models.Model):
	name = models.CharField(max_length=256, unique=True)
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return self.name

class ModulFieldOfStudy(models.Model):
	field_of_study = models.ForeignKey(FieldOfStudy)
	semester_numbers = models.CommaSeparatedIntegerField(max_length=256, null=True)

	def __unicode__(self):
		return unicode(self.field_of_study)

class Modul(models.Model):
	number = models.CharField(max_length=256, unique=True, null=True)
	name = models.CharField(max_length=1024)
	lp = models.IntegerField(blank=True, null=True)
	modultype = models.ForeignKey(ModulType, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	department = models.ForeignKey(Department, blank=True, null=True)
	fields = models.ManyToManyField(ModulFieldOfStudy, null=True)

	def __unicode__(self):
		return self.name

class Instructor(models.Model):
	firstname = models.CharField(max_length=256)
	lastname = models.CharField(max_length=256)
	title = models.CharField(max_length=256, blank=True, null=True)

	def __unicode__(self):
		return self.title + u' ' + self.firstname + u' ' + self.lastname if self.title else self.firstname + u' ' + self.lastname

class Semester(models.Model):
	name = models.CharField(max_length=256, unique=True)

	def __unicode__(self):
		return self.name

class Location(models.Model):
	building = models.CharField(max_length=256)
	room = models.CharField(max_length=256)

	def __unicode__(self):
		return self.building + u', ' + self.room if self.building else self.room

	class Meta:
		unique_together = ('building', 'room')

class EventType(models.Model):
	name = models.CharField(max_length=256, unique=True)

	def __unicode__(self):
		return self.name

class Event(models.Model):
	name = models.CharField(max_length=256)
	modul = models.ForeignKey(Modul)
	semester = models.ForeignKey(Semester)
	eventtype = models.ForeignKey(EventType)
	begin = models.TimeField(blank=True, null=True)
	end = models.TimeField(blank=True, null=True)
	weekday = models.IntegerField(blank=True, null=True)
	weeknumber = models.CharField(max_length=256, blank=True, null=True)
	instructors = models.ManyToManyField(Instructor)
	location = models.ForeignKey(Location, null=True)

	def get_instructors(self):
		return u", ".join([unicode(instructor) for instructor in self.instructors.all()])

	def __unicode__(self):
		return self.name

class Student(models.Model):
	user = models.OneToOneField(User)
	field_of_studies = models.ManyToManyField(FieldOfStudy)
	current_semester = models.IntegerField()

class Selection(models.Model):
	student = models.ForeignKey(Student)
	events = models.ManyToManyField(Event)

class Sportkurs(models.Model):
	name = models.CharField(max_length=256, unique=True)
	description = models.CharField(max_length=2048, blank=True)
	instructor = models.ForeignKey(Instructor, blank=True, null=True)

	def __unicode__(self):
		return self.name

class SportkursEvent(models.Model):
	kurs = models.ForeignKey(Sportkurs)
	details = models.CharField(max_length=2048, blank=True)
	weekday = models.IntegerField(blank=True, null=True)
	begin = models.TimeField(blank=True, null=True)
	end = models.TimeField(blank=True, null=True)
	begin_day = models.DateField(blank=True, null=True)
	end_day = models.DateField(blank=True, null=True)
	location = models.ForeignKey(Location, blank=True, null=True)
	instructor = models.ForeignKey(Instructor, blank=True, null=True)