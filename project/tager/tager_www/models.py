from django.db import models
#from django.contrib.auth.models import User


class UserProfile(models.Model):

    name = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.id)
    
    def canRate(self,post_id):
       
        p = Post.objects.get(id = post_id)
        #user = UserProfile.objects.filter(pk= user_id)
        return p.is_sold and int(p.buyer_id) == self.id


#class Channel():


#class Attribute():


class Post(models.Model):
    #seller_id = models.ForeignKey('UserProfile')
    post_name = models.CharField(max_length=10)
    buyer_id = models.ForeignKey('UserProfile')
    is_sold = models.BooleanField(default= False)


#class Comments():



#class Subscribtion():



#class Notification():


#class InterestedIn():
    



