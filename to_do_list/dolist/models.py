from django.db import models

# Create your models here.

class user(models.Model):
 name = models.CharField(max_length=100)
 username = models.CharField(max_length=100)
 password = models.CharField(max_length=50)

 def __unicode__(self):
		return self.name

class list (models.Model):
 user = models.ManyToManyField(user)
 list_text = models.CharField(max_length=200)
 task_done = models.BooleanField(default= 'false')

def __unicode__(self):
		return self.list_text