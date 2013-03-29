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


#this is Channel class where all channel records and information are kept
#name is the name of the channel
#description is the description of the channel
class Channel():
    name = models.CharField(max_length=100, unique = True)
    description = models.CharField(max_length=500) 
    def __unicode__(self):
        return self.name

#class Attribute():


class Post():
   


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




<<<<<<< HEAD
class InterestedIn():

#the following method takes the post as input and returns the buyer_id 
#to be used in other methods like canRate that needs a specified buer.
def getBuyer():
	return self.buyer_id
	
=======
#class Notification():
>>>>>>> b9adbd9590a2912b2c9044a67446e945f32c356d


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
