from django.db import models
from django.contrib.auth.models import User


# this class has the user information for creation 
# it extends User model built in django which include username, email , password ,firstname , lastname 
class UserProfile(User):       
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
    users = models.ManyToManyField("self") # many users can add many users to their networks (profile)
    
    def __unicode__(self):               # returns name in string 
      return self.user_name


    def canRate(self,post_id):
       post = Post.objects.filter(pk= post_id)
        #user = UserProfile.objects.filter(pk= user_id)
       if post.is_sold = true && post.buyer_id = self.id
           return True
        else:
           return False

      
    


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
    attribute_id = models.IntegerField()#Holds the id of the attribute
    sub_channel_id = models.ForeignKey(SubChannel)#Foreign key that references the id of the subchannels from the subchannels models
    weight = models.DecimalField(max_digits=5, decimal_places=2)#A weight given to the attribute in order to help when measuring the quality index of the post



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


    def __unicode__(self):
        return unicode(self.post_id)

   # def canRate(self,user):
    #    post = Post.objects.filter(pk= post_id)
        #user = UserProfile.objects.filter(pk= user_id)
     #   if post.is_sold = true && post.buyer_id = user.id
      #      return True
       # else:
        #    return False

    

class Values(models.Model):

    attribute_id = models.ForeignKey(Attribute)#Foreign key that references the id of the attribute from the attributes model
    name_of_value = models.CharField(max_length=64)#name of the different values that would be given for the attributes
    Post_id = models.ForeignKey(Post)#Foreign key that references the id of the post from the posts model


class Comments():



class Subscribtion():



class Notification():


class Interested_In(models.Model):
    user_id_buyer = models.ForeignKey(User, related_name = 'buyer')
    user_id_seller = models.ForeignKey(User, related_name= 'seller')
    post_id = models.ForeignKey(Post)
    class Meta:
        unique_together = ("user_id_buyer", "user_id_seller", "post_id")   




