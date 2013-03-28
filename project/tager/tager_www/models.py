from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    User = models.ForeignKey(User)
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
    # def __unicode__(self): # returns name in string
      # return self.user_name
    #This method checks whether the user can is eligible to post or not. 
    #This is done by checking whether the user is verified or not
    def canPost(self):
        return self.is_verfied

class Channel(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    def __unicode__(self):
        return self.name


class SubChannel(models.Model):

    name = models.CharField(max_length=64)#Holds the name of the subchannel
    sub_channel_id = models.IntegerField(default=0)#Holds the id of the subchannel
    channel_id = models.ForeignKey(Channel) #Foreign key id that references the id of the channel model


class Attribute(models.Model):

    name = models.CharField(max_length=64)#Name of the aatribute
    sub_channel_id = models.ForeignKey(SubChannel)#Foreign key that references the id of the subchannels from the subchannels models
    weight = models.DecimalField(max_digits=5, decimal_places=2)#A weight given to the attribute in order to help when measuring the quality index of the post

#Class Post documentation
#The model Post define the table of posts in the data base. 
#There are 17 attributes. There is a one to many relationship 
#between the post table and the subchannel table. meaning each post belongs to one subchannel.
#and each sub channel can have have many posts. Also there is a one to many relationship between the posts table 
#and the userprofile table. meaning each post can have only one author ("user") and each user could have many posts.  
#Also there is a one to many relationship between the post and the user table through the foreign key buyer_id.
#Meaning that each buyer will have many purchased posts but each post will have only one buyer.



class Post(models.Model):

    state = models.CharField(max_length="200")
    expired = models.BooleanField()
    no_of_reports = models.IntegerField()
    title = models.CharField(max_length="200")
    is_hidden = models.BooleanField()
    quality_index = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.CharField(max_length="500")
    price = models.IntegerField()
    edit_date = models.DateField()
    pub_Date = models.DateField()
    comments_count = models.IntegerField()
    intersed_count = models.IntegerField()
    picture = models.ImageField(upload_to='None', blank=True)
    sub_channel_id = models.ForeignKey(SubChannel)
    user_id = models.ForeignKey(UserProfile)
    buyer_id = models.ForeignKey(User)
    is_sold = models.BooleanField()

        


class Values(models.Model):

    attribute_id = models.ForeignKey(Attribute)#Foreign key that references the id of the attribute from the attributes model
    name_of_value = models.CharField(max_length=64)#name of the different values that would be given for the attributes
    Post_id = models.ForeignKey(Post)#Foreign key that references the id of the post from the posts model

#class Comments(models.Model):



#class Subscribtion(models.Model):



#class Notification():


#class InterestedIn():
    



