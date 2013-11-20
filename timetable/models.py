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

class Deparment(models.Model):
	name = models.CharField(max_length=256, unique=True)

	def __unicode__(self):
		return self.name

class Modul(models.Model):
	number = models.CharField(max_length=256, unique=True)
	name = models.CharField(max_length=1024)
	lp = models.IntegerField(blank=True, null=True)
	modultype = models.ForeignKey(ModulType, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	deparment = models.ForeignKey(Deparment, blank=True, null=True)

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
		return self.building + u', ' + self.room

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
	instructors = models.ManyToManyField(Instructor)
	location = models.ForeignKey(Location, null=True)
	semester_numbers = models.CommaSeparatedIntegerField(max_length=256, null=True)

	def get_instructors(self):
		return u", ".join([unicode(instructor) for instructor in self.instructors.all()])

	def __unicode__(self):
		return self.name