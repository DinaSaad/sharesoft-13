from django.db import models

# Create your models here.
class user(models.Model):
	name = models.CharField(max_length=100)
	user_mail = models.CharField(max_length=100)
	password = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name
	
class Tolist (models.Model):
	user = models.ForeignKey(user, related_name ='users')
	list_name = models.CharField(max_length = 50)
	def editlist(self,name):
		self.list_name=name
	def addTask(self,text):
		newTask=Tolist_item(self,text,'false')
		newTask.save()
	def deleteTask(self,text):
		Tolist_item.objects.all().filter(list_text=text).delete()
	

	def __unicode__(self):
		return self.list_text

class Tolist_item (models.Model):
	tolist = models.ForeignKey(Tolist)
	list_text = models.CharField(max_length=200)
	task_done = models.BooleanField(default= 'false')
