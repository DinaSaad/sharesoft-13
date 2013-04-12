from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser

#since userprofile has different than abstractbaseuser attriubtes thats why will define our own custom manager that extends BaseUserManager.
class MyUserManager(BaseUserManager):
    # this will create user when name , email, password is entered 
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=MyUserManager.normalize_email(email),
            
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
     #this creates the admin user 
    def create_superuser(self, email, name , password):
        user = self.create_user(email,
            password=password, name=name
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

     #UserProfile class extends abdstractbaseuser which has core implementation of user model build in    django 
     #this class addes some fields to abstractbaseuser which is inherited 

class UserProfile (AbstractBaseUser):
    name = models.CharField(max_length=40)     
    email = models.EmailField(max_length=254, unique=True)
    facebook_uid = models.IntegerField(unique=True, null=True)
    accesstoken = models.CharField(max_length=50 , null=True , unique=True)
    date_Of_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)           
    is_verfied = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='img',blank=True)
    activation_key = models.BooleanField(default=False)
    status = models.CharField(max_length=400 , null=True) 
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
     )
    gender = models.CharField(max_length=1, choices=gender_choices , null=True)
    
    # this tells UserProfile to use the custom manager made 
    objects = MyUserManager()  
    # this is the unique identifier , it can be any unique field
    USERNAME_FIELD = 'email'   
    # the requird fields are the fields which are mandotory , you dont put the USERNAME_fields in it 
    REQUIRED_FIELDS = ['name']  
    
    #these method are in the abstractbaseuser and These methods allow the admin to control access of the User to admin content: 
    is_admin = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')    


    is_active = models.BooleanField('active', default=True,    # returns true if the user is still active 
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')

    def get_full_name(self):
        # return name . Could also be User.first_name User.last_name if you have these fields
        return self.name
 
    def get_short_name(self):
        # return name. Could also be User.first_name if you have this field
        return self.name
 
    def __unicode__(self):
        return self.email
     
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True

    # genrates setters and getters
    @property   
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin

    def canRate(self,post_id):
        print post_id
        p = Post.objects.get(id = post_id)
        #user = UserProfile.objects.filter(pk= user_id)
        return p.is_sold and p.buyer_id == self.id

    #This method returns to the Seller (User) the list of buyers (User) interested in his (specific) post
    def getInterestedIn(self, post):       
        print self.id
        print post.id  
        # p = Post.objects.get(id = post)
        interested = InterestedIn.objects.filter(user_id_seller = self.id, post = post.id)
        x = []
        for i in interested:
            x.append(i.user_id_buyer.id)
        return x
        
    def canPost(self):
        return self.is_verfied

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



#this is Channel class where all channel records and information are kept
#name is the name of the channel
#description is the description of the channel
class Channel():
    name = models.CharField(max_length=100, unique = True)
    description = models.CharField(max_length=500) 
    def __unicode__(self):
        return self.name

#class Attribute():


#This table shows the existing subchannels, name represents the name of the subchannel, and the channel_id is a foreign key that references the id of each channel from the channels model
class Subchannel(models.Model):
	
	name = models.CharField(max_length=64)#Holds the name of the subchannel
	channel_id   = models.ForeignKey(Channel) #Foreign key id that references the id of the channel model




class Post():
	

''' C1_beshoy Cal Quality index this method takes a post and then calculate its quality 
index based on the filled attributes and thier wight'''
    def cal_quality_index(self):
        q_index=0
        if self.title is not None && self.description is not None
         && self.priceis not None && picture is not None :
         q_index=q_index+20
         attr_list_tmp=Attribute.objects.filter(sub_channel_id=self.sub_channel_id_id)
         values_list_tmp=Values.objects.filter(Post_id=self.post_id_id)
         for Values in values_list_tmp:
            if Values.name_of_value is not None:
                attr_tmp=Attribute.objects.get(Attribute_id=Values.attribute_id_id)
                q_index=q_index+int(attr_tmp.weight)
        self.quality_index=q_indexUI



#class Comments():



#this is subscription class that keeps records for all possible combination of subscriptions a user can make where
#channel references to Channel model ex.(cars channel)
#sub_channelreference to SubChannel model ex.(sport cars)
#parameter is predefined ex.(color)
#choice that users can make ex.(red)
#previous example mean that a user can subscribe to red sport cars
#and it contains a def subscribe where a user can add subscription input to UserSubscription model
class Subscribtion():
    channel = models.ForeignKey(Channel, null = True) 
    sub_channel = models.ForeignKey(SubChannel, null = True)
    attribute = models.ForeignKey(Attribute, null = True)
    value = models.CharField(Values, null = True)
    def subscribe(self, user_received, channel_received, sub_channel_received):
        user_subscription = UserSubscription(user = user_received, channel = channel_received, sub_channel = sub_channel_received, subscription = self)
        user_subscription.save()
    class Meta:
        unique_together = ("channel","sub_channel","parameter","choice") #to make sure no duplicates were entered





# this model is the result of the Many-to-Many relationship between the model Users and Post
# this model takes in a the seller's id, buyer's id, and the post id (related to the seller)
# the model has a primary key combination of all 3 attributes

class InterestedIn(models.Model):
    user_id_buyer = models.ForeignKey(UserProfile, related_name = 'buyer')
    user_id_seller = models.ForeignKey(UserProfile, related_name= 'seller')
    post = models.ForeignKey(Post)

    class Meta:                    #gives the model a primary key of these attributes
        unique_together = ("user_id_buyer", "user_id_seller", "post")     
    
    def __unicode__(self):         #converts the INT to Strings to be displayed
        return unicode(self.post_id) 





#the following method takes the post as input and returns the buyer_id 
#to be used in other methods like canRate that needs a specified buer.
def getBuyer():
	return self.buyer_id
	

#class Notification():

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
	



#class InterestedIn():
    

#this class saves the data of the subscriptions that the user has done
#user is a reference to the user
#channel is a reference to channel the user is subscribed in
#sub_channel is a reference to the sub channel the user is subscribed in
#subscription is a reference to the subscription pre defined in Subscription model
class UserSubscription(models.Model):
    user = models.ForeignKey(User)
    channel = models.ForeignKey(Channel,null = True)
    sub_channel = models.ForeignKey(SubChannel,null = True) 
    subscription = models.ForeignKey(Subscription,null = True) 
    class Meta:
        unique_together = ("user", "channel", "sub_channel", "subscription") #to make sure no duplicates were entered
