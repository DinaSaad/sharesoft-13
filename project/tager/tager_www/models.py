from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
	status = models.CharField(max_length=400)
	def ___unicode___(self):
		return unicode(self.id)
	
	#The Method Takes 2 arguments(User who clicked intrested,Post Which the user has clicked the button in) 
	#The method get the Post Object using the Post_id , then checks if the post exists , 
	#then then check if the user exists , 
	#then input the values in teh table [IntrestedIn] )
	def Interested(self, post_id_in):
		p=Post.objects.get(pk=post_id_in.id)
		#User CHeck Conditions should be added
		if Post.objects.filter(pk=post_id_in).exists():
			if  UserProfile.filter(user_id=self.user_id).exists():
					user1=InterestedIn(user_id_buyer=self.user_id,user_id_in_seller=p.seller_id,post_id=post_id_in)
					user1.save()



#class Channel():


#class Subchannel():



#class Attribute():

class Post(models.Model):
	user_id = models.ForeignKey(UserProfile)
	def ___unicode___(self):
		return unicode(self.id)


#class Comments():



#class Subscribtion():



#class Notification():


class InterestedIn(models.Model):
	user_id = models.ForeignKey(UserProfile)
	post_id = models.ForeignKey(Post)

	#The Method Taked User_id[User Clicking the intrested button] and Post_id[the post where the intrested button has been clciked ]

	
	#post checks
	#!user_id & post not in intrested in
	



