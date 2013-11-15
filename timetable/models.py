from django.db import models

# Create your models here.
class Modul(models.Model):
	number = models.CharField(max_length=256)
	name = models.CharField(max_length=1024)

	def __unicode__(self):
		return self.name