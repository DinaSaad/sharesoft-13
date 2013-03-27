from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile():

class Channel():
	name = models.CharField(max_length=100, unique = True)
	description = models.CharField(max_length=500)
	def __unicode__(self):
		return self.name

class Subchannel():

class Attribute():

class Post():

class Comments():

class Subscribtion():
	channel_id = models.ForeignKey(Channel, null = True)
	sub_channel_id = models.ForeignKey(SubChannel, null = True)
	parameter = models.CharField(max_length=100, null = True)
	choice = models.CharField(max_length=100, null = True)
	def subscribe(self, user_id_received, channel_id_received, sub_channel_id_received):
		user_subscription = UserSubscriptions(user_id = user_id_received, channel_id = channel_id_received, sub_channel_id = sub_channel_id_received, subscription = self)
		user_subscription.save()
	class Meta:
		unique_together = ("channel_id","sub_channel_id","parameter","choice")

class Notification():

class InterestedIn():
	
class UserSubscriptions(models.Model):
	user_id = models.ForeignKey(UserProfile)
	channel_id = models.ForeignKey(Channel,null = True)
	sub_channel_id = models.ForeignKey(SubChannel,null = True)
	subscription = models.ForeignKey(Subscription,null = True)
	class Meta:
		unique_together = ("user_id", "channel_id", "sub_channel_id", "subscription")
