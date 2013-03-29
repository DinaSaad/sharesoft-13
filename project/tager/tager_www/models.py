from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):


    #The Method Takes 2 arguments(User who clicked intrested,Post Which the user has clicked the button in) 
    #then then check if the user is verified ,
    #then input the values in  table [IntrestedIn] and Increment Intrested Counter
    def Interested(self, post_in):
        if self.canPost:
            if  Post.objects.filter(pk=post_in.post_id).exists():
                user1=InterestedIn(user_id_buyer_id=self.user_id,user_id_seller_id=post_in.post_id,post_id_id=post_in.post_id)
                user1.save()
                post_in.intersed_count=post_in.intersed_count+1
                post_in.save()
    



