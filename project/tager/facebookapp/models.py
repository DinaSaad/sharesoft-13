from django.db import models

class UserProfile(User):
    facebook_uid = models.integer()
    #first_name = models.CharField(max_length=20)
    #last_name= models.CharField(max_length=20)
    #email = models.CharField(max_length=50)
    accesstoken = models.CharField(max_length=50)
