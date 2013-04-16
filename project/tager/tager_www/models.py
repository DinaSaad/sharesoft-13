from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser

from django.utils.timezone import utc
from datetime import datetime, timedelta

EXPIRATION_DAYS = 10

from django.db.models import Sum , Avg 




#mai 
#this is the custome manager made , it inheirts the built in baseUSermanager 
#it must have 2 methods which is create user and create super users 
class MyUserManager(BaseUserManager):

    # this method takes email , name , password and extra fields (which can be any fileds in the USerPRofile model) as paramters
    #it checks if the user provided the email or not 
    #than it returns the saved user with the paramters entered 
    #sets is_staff /is_superuser to false cuz hes not a super user
    #and is_active is set to true which means this user has an account

    def create_user(self, email, name, password=None , **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
 

        user = self.model(name=name , email=email,**extra_fields )
        email=MyUserManager.normalize_email(email),
        is_staff=False 
        is_superuser=False 
        is_active = True
        
                
 
        user.set_password(password)
        user.save(using=self._db)
        return user


     #this method also takes email name password and extra fields ) to create superusers which are the admins 
     #returns the saved user with the attributes entered 
     #sets is_admin/is_staff to true cuz they r admin

      
    def create_superuser(self, email, name , password , **extra_fields):
        user = self.create_user(email,
            password=password, name=name , **extra_fields
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


     


#Mai c2 : provide the company with user 
#this class inherits AbstractBaseUser (password, login_now) and adds to these 2 fields the fields that i wrote 
#when AbstractBaseUSer is inherited u have to follow 3 min requirments , 1. the class has to have a numeric primary key 
#2.the class has to have a unique identifer which in this case is email and its written in USERNAME_FIELD which is the fields that uniquly identify the user 
#there is also a field called REQIURED fields which is a list of all the fields except the USER_field that are requied for creating the user 
#3.the class should have 2 methods get_full_name and get_short_name which doesnt take paramters and returns an identifyer of the user in my case its email but it can be username , and both can be the same 
#for this class a custom manager is made beause i have different attributes than the USer model built in . this manager is called from the class .
class UserProfile(AbstractBaseUser):
    name = models.CharField(max_length=40)     
    email = models.EmailField(max_length=254, unique=True)
    facebook_uid = models.IntegerField(unique=True, null=True)
    accesstoken = models.CharField(max_length=50 , null=True , unique=True)
    date_Of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20 , null=True)
    is_admin = models.BooleanField(default=False)           
    is_verfied = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='img',blank=True)
    activation_key = models.CharField(max_length=40 , null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=400 , null=True) 
    rating = models.FloatField(default=0.0)
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
     )
    gender = models.CharField(max_length=1, choices=gender_choices , null=True)
    
    
    objects = MyUserManager()  
    
    USERNAME_FIELD = 'email'   
    
    REQUIRED_FIELDS = ['name']  

    
    #these attrubutes are in the abstractbaseuser and These methods allow the admin to control access of the User to admin content: 
    is_admin = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')    


    is_active = models.BooleanField('active', default=True,    # returns true if the user is still active 
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')

    def get_full_name(self):
        
        return self.name
 
    def get_short_name(self):
        
        return self.name
 
    def __unicode__(self):
        return self.email + str(self.is_verfied) + str(self.activation_key)

     # this methods taked in a permission and the objects and returns true or false regarding wherther the objec entered has permission or not (user)
    def has_perm(self, perm, obj=None):
        
        return True
 
	# Handle whether the user has permissions to view the app `app_label`?" 
    def has_module_perms(self, app_label):
        
        return True

    # genrates setters and getters
    # Handle whether the user is a member of staff?"
    @property   
    def is_staff(self):
        
        return self.is_admin


    #mai :registertaion
    #this method takes self and just checks if the todays date from the time of the creation of the user is greater then
    #the expired date set then the key is expired so it retunrs true 
    #else returns false 

    def is_expired(self):
        if (datetime.now() - self.created).days >= EXPIRATION_DAYS:
            return True
        return False

#C2-mahmoud ahmed- as a user i should be able to rate seller whom i bought from before- canRate method 
#is a method that takes in an object user as in "self" and a post id and what it does is it gets the Post
#object and insert it in a variable p, then takes the post object and the buyer and checks if he has rated 
#this post before.. if he did then it would return false as he can't rate again if not. then it checks if the
#product is sold or not and if it is sold and the buyer set to this post is the same as the buyer in sessio
#rateSeller button appears if he isn't then the button won't appear.

    def can_rate(self,post_id):
        print post_id
        p = Post.objects.get(id = post_id)
        r = Rating.objects.filter(post= p ,buyer = self).count() 
        print r
        if r == 1:
            return False
        # #user = UserProfile.objects.filter(pk= user_id)
        return p.is_sold and p.buyer_id == self.id

    def get_posts(self):
        user_posts = Post.objects.filter(user_id_id = self.id)
        return user_posts

    def add_buyer(self,post,phone_num):
        p = post        
        if p.user_id == self.id:
            post_buyer = UserProfile.objects.get(phone_number = phone_num)
            #post_buyer_id = post_buyer.id
            p.buyer = post_buyer
            p.is_sold = True
            p.save()
            return True
        else:
            return False

    def show_add_buyer_button(self,post_id):
        p = Post.objects.get(id = post_id)
        return user.id == post.user_id_id

    #This method returns to the Seller (User) the list of buyers (User) interested in his (specific) post
    def get_interested_in(self, post):       
        interested = InterestedIn.objects.filter(user_id_seller = self.id, post = post.id)
        x = []
        for i in interested:
            x.append(i.user_id_buyer.id)
        return x
        
    def can_post(self):
        return self.is_verfied

    #The Method Takes 2 arguments(User who clicked intrested,Post Which the user has clicked the button in) 
    #then then check if the user is verified ,
    #then input the values in  table [IntrestedIn] and Increment Intrested Counter
    def interested_in(self, post_in):
        if self.canPost:
            if  Post.objects.filter(pk=post_in.post_id).exists():
                user1=InterestedIn(user_id_buyer_id=self.user_id,user_id_seller_id=post_in.post_id,post_id_id=post_in.post_id)
                user1.save()
                post_in.intersed_count=post_in.intersed_count+1
                post_in.save()

    def calculate_rating(self,rate,post,buyer): #self is the post_owner
        owner_id = self.id
        #print owner_id
        post_id = post.id
        #print owner_id
        buyer_id = buyer.id
        #print buyer_id

        rate = Rating(post_owner_id=owner_id,buyer_id=buyer_id,post_id=post_id,rating= rate)
        rate.save()
        user_rating = Rating.objects.filter(post_owner = self).aggregate(Avg('rating')).values()[0]
       # print user_rating
        self.rating = user_rating
        self.save() 
        return user_rating




#this is Channel class where all channel records and information are kept
#name is the name of the channel
#description is the description of the channel
class Channel(models.Model):
    name = models.CharField(max_length=100, unique = True)
    description = models.CharField(max_length=500) 
    
    def __unicode__(self):
        return self.name

#This table shows the existing subchannels, name represents the name of the subchannel, and the channel_id is a foreign key that references the id of each channel from the channels model
class SubChannel(models.Model):
    name = models.CharField(max_length=64)#Holds the name of the subchannel
    channel = models.ForeignKey(Channel) #Foreign key id that references the id of the channel model


#Class Post documentation
#The model Post define the table of posts in the data base. 
#There are 17 attributes. There is a one to many relationship 
#between the post table and the subchannel table. meaning each post belongs to one subchannel.
#and each sub channel can have have many posts. Also there is a one to many relationship between the posts table 
#and the userprofile table. meaning each post can have only one author ("user") and each user could have many posts.  
#Also there is a one to many relationship between the post and the user table through the foreign key buyer_id.
#Meaning that each buyer will have many purchased posts but each post will have only one buyer.

class Post(models.Model):
    state = models.CharField(max_length=200, default= "new")
    expired = models.BooleanField(default= False)
    no_of_reports = models.IntegerField(null=True)
    title = models.CharField(max_length=200)
    is_hidden = models.BooleanField(default=False)
    quality_index = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    description = models.CharField(max_length=500, null=True)
    price = models.IntegerField(null=True)
    edit_date = models.DateField(null=True)
    pub_date = models.DateField(null=True)
    comments_count = models.IntegerField(default=0)
    intersed_count = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='media', blank=True)
    picture1 = models.ImageField(upload_to='media', blank=True)
    picture2 = models.ImageField(upload_to='media', blank=True)
    picture3 = models.ImageField(upload_to='media', blank=True)
    picture4 = models.ImageField(upload_to='media', blank=True)
    picture5 = models.ImageField(upload_to='media', blank=True)
    subchannel = models.ForeignKey(SubChannel)
    seller = models.ForeignKey(UserProfile, related_name = 'seller_post')
    buyer = models.ForeignKey(UserProfile, related_name = 'buyer_post', blank=True, null=True)
    is_sold = models.BooleanField()#class Comments():

    def get_buyer():
        return self.buyer.id
        
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


# This model defines the table of reports
# this table contains 3 attributes, the related post ID, the type of report chosen by the user, and the user reporting the post
# as the user reports a post after choosing a reason pre-defined in the system, a record is inserted in the table
# this table is used to retrieve the reports related to a certain post
class Report(models.Model):
    reported_post = models.ForeignKey(Post, related_name = 'reported_Post')
    report_type = models.CharField(max_length = '100')
    reporting_user = models.ForeignKey(UserProfile, related_name = 'reporting_user_id')
        
    def __unicode__(self):
        return (self.report_type)


class Rating(models.Model):
    post_owner = models.ForeignKey('UserProfile', related_name="post_owner")
    buyer = models.ForeignKey('UserProfile',related_name="post_buyer")
    post = models.ForeignKey('Post')
    rating = models.FloatField()

    class Meta:
        unique_together = ("post","buyer")

#This table shows the attributes that describes the subchannel, name represents Name of the attribute, subchannel_id is a Foreign key that references the id of the subchannels from the subchannels models, weight is the weight given to the attribute in order to help when measuring the quality index of the post
class Attribute(models.Model):
    name = models.CharField(max_length=64)
    subchannel = models.ForeignKey(SubChannel)
    weight = models.FloatField()

class Value(models.Model):
    attribute_id = models.ForeignKey(Attribute)
    value = models.CharField(max_length=64)
    post = models.ForeignKey(Post)


#this is subscription class that keeps records for all possible combination of subscriptions a user can make where
#channel references to Channel model ex.(cars channel)
#sub_channelreference to SubChannel model ex.(sport cars)
#parameter is predefined ex.(color)
#choice that users can make ex.(red)
#previous example mean that a user can subscribe to red sport cars
#and it contains a def subscribe where a user can add subscription input to UserSubscription model
class Subscription(models.Model):
    channel = models.ForeignKey(Channel, null = True)
    sub_channel = models.ForeignKey(SubChannel, null = True)
    parameter = models.ForeignKey(Attribute, null = True)
    choice = models.ForeignKey(Value, null = True)
    
    class Meta:
        unique_together = ("channel","sub_channel","parameter","choice")
    def subscribe_by_channel(self, user_in):
        UserSubchannelSubscription.objects.filter(user = user_in, parent_channel = self.channel).delete()
        channel_to_subscribe = self.channel
        subscription = UserChannelSubscription(user = user_in, channel = channel_to_subscribe)
        subscription.save()
        
    def subscribe_by_subchannel(self, user_in):
        self_parent_channel = self.sub_channel.channel_id
        UserChannelSubscription.objects.filter(user = user_in, channel = self_parent_channel).delete()
        sub_channel_to_subscribe = self.sub_channel
        subscription = UserSubchannelSubscription(user = user_in, parent_channel = self_parent_channel, sub_channel = sub_channel_to_subscribe)
        subscription.save()
        subchannels_with_same_channel = Subchannel.objects.filter(channel_id=self_parent_channel).count()
        subchannels_subscribed_with_same_channel = UserSubchannelSubscription.objects.filter(parent_channel=self_parent_channel, user=user_in).count()
        if subchannels_with_same_channel==subchannels_subscribed_with_same_channel:
            UserSubchannelSubscription.filter(parent_channel=self.sub_channel.channel).delete()
            self.subscribe_Bychannel(user_in)
    def subscribe_by_parameter(self, user_in):
        self_parent_channel = self.sub_channel.channel_id
        sub_channel_to_subscribe = self.sub_channel
        self_parent_channel = self.channel
        subscription = UserParameterSubscription(user = user_in, parent_channel = self_parent_channel, sub_channel = sub_channel_to_subscribe, parameter = self.parameter, choice = self.choice)
        subscription.save()
        
    def __unicode__(self):
        return self.id

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
    

#class Notification():

#This table holds different values for the attribute (i.e for each attribute there will be different values), attribute_id is a Foreignkey that references the id ofthe attribute from the attributes model,value is the name of the different values that would be given for the attributes, and Post_id is a Foreign key that references the id of the post from the posts model#    
class UserChannelSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    channel = models.ForeignKey(Channel)

    class Meta:
        unique_together = ("user", "channel")
    def __unicode__(self):
        return unicode(self.user)


class UserSubchannelSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    parent_channel = models.ForeignKey(Channel)
    sub_channel = models.ForeignKey(SubChannel)

    class Meta:
        unique_together = ("user", "parent_channel", "sub_channel")
    def __unicode__(self):
        return unicode(self.user)

class UserParameterSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    parent_channel = models.ForeignKey(Channel)
    sub_channel = models.ForeignKey(SubChannel)
    parameter = models.ForeignKey(Attribute)
    choice = models.ForeignKey(Value)

    class Meta:
        unique_together = ("user", "parent_channel", "sub_channel", "parameter", "choice")
    def __unicode__(self):
        return unicode(self.user)