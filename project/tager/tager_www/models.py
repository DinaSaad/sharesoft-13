from django.db import models
from django.contrib.auth.models import User


class UserProfile():


class Channel():


#This table shows the existing subchannels
class SubChannels(models.Model):
	
	name = models.CharField(max_length=64)#Holds the name of the subchannel
	sub_channel_id = models.IntegerField(default=0)#Holds the id of the subchannel
	channel_id   = models.ForeignKey(Channel) #Foreign key id that references the id of the channel model



class Post():


class Comments():



class Subscribtion():



class Notification():


class InterestedIn():
	def InterestedIn(user_id_in, post_id_in):
		if UserProfile.userCanPost(user_id):
			if  Post.filter(post_id=post_id_in).exists()
				if not User.filter(user_id=user_id_in).exists()
					p=Post.get(post_id=post_id_in)
					user1=InterestedIn(user_id_buyer=user_id_in,user_id_seller=p.seller_id,post_id=post_id_in)
					user1.save()

		#User CHecks
		#post checks
		#!user_id & post not in intrested in







#This table shows the attributes that describes the subchannel
class Attributes(models.Models):
	name = models.CharField(max_length=64)#Name of the aatribute
	attribute_id = models.IntegerField()#Holds the id of the attribute
	sub_channel_id = models.ForeignKey(SubChannels)#Foreign key that references the id of the subchannels from the subchannels models
	weight = models.DecimalField()#A weight given to the attribute in order to help when measuring the quality index of the post


#This table holds different values for the attribute (i.e for each attribute there will be different values)
class Values(models.Models):
	attribute_id = models.ForeignKey(Attributes)#Foreign key that references the id of the attribute from the attributes model
	name_of_value = models.CharField(max_length=64)#name of the different values that would be given for the attributes 
	Post_id = models.ForeignKey(Post)#Foreign key that references the id of the post from the posts model
	



