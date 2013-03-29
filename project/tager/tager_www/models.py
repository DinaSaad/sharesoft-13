from django.db import models
from django.contrib.auth.models import User


class UserProfile():


class Channel():


#This table shows the existing subchannels, name represents the name of the subchannel, and the channel_id is a foreign key that references the id of each channel from the channels model
class SubChannel(models.Model):
	
	name = models.CharField(max_length=64)#Holds the name of the subchannel
	channel_id   = models.ForeignKey(Channel) #Foreign key id that references the id of the channel model



class Post():


class Comments():



class Subscribtion():



class Notification():


class InterestedIn():




#This table shows the attributes that describes the subchannel, name represents Name of the attribute, subchannel_id is a Foreign key that references the id of the subchannels from the subchannels models, weight is the weight given to the attribute in order to help when measuring the quality index of the post
class Attributes(models.Models):
	name = models.CharField(max_length=64)
	subchannel_id = models.ForeignKey(SubChannels)
	weight = models.DecimalField()


#This table holds different values for the attribute (i.e for each attribute there will be different values), attribute_id is a Foreignkey that references the id ofthe attribute from the attributes model,value is the name of the different values that would be given for the attributes, and Post_id is a Foreign key that references the id of the post from the posts model#
class Values(models.Models):
	attribute_id = models.ForeignKey(Attributes)
	value = models.CharField(max_length=64)
	Post_id = models.ForeignKey(Post)
	



