from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):   
    user = models.ForeignKey(User)    
    date_Of_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)           
    is_verfied = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='img',blank=True)
    activation_key = models.BooleanField(default=False)
    status = models.CharField(max_length=400) 
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices)
    users = models.ManyToManyField("self") # many users can add many users to their networks (profile)
    
    def __unicode__(self):               # returns name in string 
       return self.user.username

class Channel():


class Subchannel():



class Attribute():


class Post():


class Comments():



class Subscribtion():



class Notification():


class InterestedIn():
	



