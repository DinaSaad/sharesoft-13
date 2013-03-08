from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class user_guest(models.Model):
  user = models.OneToOneField(User)
  name = models.CharField(max_length=40)

  def __unicode__(self):
	return self.name

def create_user(sender,instance, **kwargs):
    Guest.new = user_guest.objects.get_or_create(user=instance)

post_save.connect(create_user,User)
      