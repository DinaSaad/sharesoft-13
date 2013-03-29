from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile():

#this is Channel class where all channel records and information are kept
class Channel():
	name = models.CharField(max_length=100, unique = True) #name of the channel
	description = models.CharField(max_length=500) #description of the channel
	def __unicode__(self):
		return self.name

class Subchannel():

class Attribute():

class Post():

class Comments():

#this is subscription class that keeps records for all possible combination of subscriptions a user can make.
class Subscribtion():
	channel_id = models.ForeignKey(Channel, null = True) #reference to Channel model ex.(cars channel)
	sub_channel_id = models.ForeignKey(SubChannel, null = True) #reference to SubChannel model ex.(sport cars)
	parameter = models.CharField(max_length=100, null = True) #parameter that is predefined ex.(color)
	choice = models.CharField(max_length=100, null = True) #choice that users can make ex.(red)
	#previous example mean that a user can subscribe to red sport cars
	#this def add user subscription input to UserSubscription model
	def subscribe(self, user_id_received, channel_id_received, sub_channel_id_received):
		user_subscription = UserSubscription(user_id = user_id_received, channel_id = channel_id_received, sub_channel_id = sub_channel_id_received, subscription = self)
		user_subscription.save()
	class Meta:
		unique_together = ("channel_id","sub_channel_id","parameter","choice") #to make sure no duplicates were entered

class Notification():

class InterestedIn():
	
#this class saves the data of the subscriptions that the user has done
class UserSubscription(models.Model):
	user_id = models.ForeignKey(User) #a reference to the user
	channel_id = models.ForeignKey(Channel,null = True) #a reference to channel subscribed in
	sub_channel_id = models.ForeignKey(SubChannel,null = True) #a reference to the sub channel the user is subscribed in
	subscription = models.ForeignKey(Subscription,null = True) # a reference to the subscription pre defined in Subscription model
	class Meta:
		unique_together = ("user_id", "channel_id", "sub_channel_id", "subscription") #to make sure no duplicates were entered
