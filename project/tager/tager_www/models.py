from django.db import models
#from django.contrib.auth.models import User


class UserProfile():

    
    def canRate(self,post_id):
        print post_id
        p = Post.objects.get(id = post_id)
        #user = UserProfile.objects.filter(pk= user_id)
        return p.is_sold and p.buyer_id == self.id


#class Channel():


#class Attribute():


class Post():
   


#class Comments():



#class Subscribtion():



#class Notification():


#class InterestedIn():
    



