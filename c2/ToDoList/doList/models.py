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
    list_text = models.CharField(max_length=200)
    task_done = models.BooleanField(default= 'false')

    def __unicode__(self):
        return self.list_text

#class Registered_users (models.Model):
 #   user = models.ForeignKey(user)
  #  Tolist = models.ForeignKey(Tolist)
   # regs_users = models.ForeignKey(user, related_name= " registeration")