from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser
from django.utils.timezone import utc
import datetime
from datetime import timedelta






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
    facebook_uid = models.CharField(max_length=200, null=True)
    accesstoken = models.CharField(max_length=50 , null=True , unique=True)
    date_Of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20 , null=True)
    phone_number2 = models.CharField(max_length=20 , null=True)
    is_admin = models.BooleanField(default=False)           
    is_verfied = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    private_birth = models.BooleanField(default=False)
    private_number = models.BooleanField(default=False)
    private_work = models.BooleanField(default=False)
    works_at = models.CharField(max_length=100, null=True)
    works_at2 = models.CharField(max_length=100, null=True)
    # photo = models.ImageField(upload_to='img',blank=True)
    photo = models.ImageField(upload_to='img',blank=True,default="mpf.png")
    activation_key = models.CharField(max_length=40 , null=True)
    sms_code = models.CharField(max_length=5 , null=True)
    status = models.CharField(max_length=400 , null=True) 
    rating = models.FloatField(default=0.0)
    phone_is_verified=models.BooleanField(default=False)    
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
     )
    gender = models.CharField(max_length=1, choices=gender_choices , null=True)
    
    friends = models.ManyToManyField ("self")
    
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
        return self.email
        # return self.email + str(self.is_verfied) + str(self.activation_key)
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

    def cache(user,url):
        """Store image locally if we have a URL"""
        result = urllib.urlretrieve(url)
        self.photo.save(
                os.path.basename(url),
                File(open(result[0], 'rb'))
                )
        self.save()


   

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
        if p.seller_id == self.id:
            try:
                post_buyer = UserProfile.objects.get(phone_number = phone_num)
            except UserProfile.DoesNotExist:
                return False
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

   #C1-Tharwat) This method takes in 2 parameters, the user id and the post.
    #It creates a list in which it filters through the posts table based on the user and post id.
    #It returns to the Seller (User) the list of buyers (User) interested in his (specific) post
    #This method returns to the Seller (User) the list of buyers (User) interested in his (specific) post
    def get_interested_in(self, post):       
        interested = InterestedIn.objects.filter(user_id_seller = self, post = post)
        buyer_names = []
        for i in interested:
            buyer_names.append(i.user_id_buyer.name)
        return buyer_names

    #C1-Tharwat) This method is used to report a post for a reason choosen from a pre-defined list
    #It takes 2 parameters, the post being reported and the reason of report
    #It then inserts the record into the Report table
    def report_the_post(self, post, report_reason):
        reported_post = Post.objects.get(id = post.id)
        if post.seller.id == self.id:
            print 'Cant report urself'
        elif Report.objects.filter(reported_post = post, reporting_user = self.id).exists():
            print 'already reported'
        elif reported_post.report_count() >= 20:
            reported_post.is_hidden = True
            reported_post.save()
        else:   
            report = Report(reported_post = post, report_type = report_reason, reporting_user = self)
            report.save()
            reported_post.no_of_reports = reported_post.no_of_reports + 1
            reported_post.save()      
        
    
    #c1_abdelrahman the method takes self as an argument. 
    # It checks whether the user has the prevalage to post or not.
    #the return type is whether true or false. 
    # if the user is not verfied the method returns false 
    # else if the user is premium the method return true without checking any further condition. 
    # but if the user is not premium but verfied then the method check the user's number of active posts if it is below three the method return true else it returns false.
    def can_post(self):
        no_of_user_active_posts =  Post.objects.filter(seller = self).exclude(state='sold').exclude(state='Archived').count()
        print no_of_user_active_posts
        if not self.is_verfied:
            return False
        else:
            if self.is_premium:
                return True
            else:
                if no_of_user_active_posts < 3:
                    return True
                else: 
                    return False

    #c1 abdelrahman the method takes self, and post id as an arguments it checks whether this combination is in the table if it is in the query set. 
    # it returns false meaning that the user can not add this post to the wish list, else it returns true.
    def add_to_wish_list(self, post_id):
        if WishList.objects.filter(post=post_id , user = self).exists():
            return "false"
        else:
            return "true"

    #The Method Takes 2 arguments(User who clicked intrested,Post Which the user has clicked the button in) 
    #then then check if the user is verified ,
    #then input the values in  table [IntrestedIn] and Increment Intrested Counter
    def interested_in(self, post_in):
        if self.is_verfied:
            if  Post.objects.filter(pk=post_in.id).exists():
                user1=InterestedIn(user_id_buyer =self,user_id_seller =post_in.seller,post=post_in)
                user1.save()
                post_in.intersed_count=post_in.intersed_count+1
                post_in.save()

#C2-mahmoud ahmed- as a user i can rate sellers whom i bought from. the method takes the rate and the post
#and the buyer as inputs and then it inserts these inputs into the rating table and save the record after
#that the post_owner rating is calculated and the average is brought and saved instead of the old rating.
#and then the average rating is returned.

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

#c2-mahmoud ahmed-as a user i should be able to see the people i interacted with through buying 
#and selling activities - what get_interacting_people does is that it first gets the posts where
#the current user is found as the buyer of a post in the Posts table then it loops the list that is 
#returned from the filter and it gets the ids of the sellers which the user bought the post from
#and then get them as objects and add them to the list. and then the same procedure is repeated 
#for the posts where he was the post owner and the post is sold so it gets the buyers and then add
#them to the interacting peoples list. and at the end it returns the list. duplicate records was handeled

    def get_interacting_people(self):
        interacting_people = []
        refined_interacting_people = []
        
        posts_bought = Post.objects.filter(buyer_id = self.id)
        for post in posts_bought:
            seller_identifciation = post.seller.id
            seller_obj = UserProfile.objects.get(id=seller_identifciation)
            if seller_obj not in interacting_people:
                interacting_people.append(seller_obj)
                
        
        post_sold_to = Post.objects.filter(seller_id = self.id, is_sold = True)
        
        for post in post_sold_to:
            buyer_identification = post.buyer.id
            buyer_obj = UserProfile.objects.get(id=buyer_identification)
            if buyer_obj not in interacting_people:
                interacting_people.append(buyer_obj)
                    

        # for p in interacting_people:
        #     if new not in refined_interacting_people:
        #         refined_interacting_people.append(p)
        
        print interacting_people
        print refined_interacting_people

        return interacting_people

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

    def __unicode__(self):
        return self.name



#Class Post documentation
#The model Post define the table of posts in the data base. 
#There are 17 attributes. There is a one to many relationship 
#between the post table and the subchannel table. meaning each post belongs to one subchannel.
#and each sub channel can have have many posts. Also there is a one to many relationship between the posts table 
#and the userprofile table. meaning each post can have only one author ("user") and each user could have many posts.  
#Also there is a one to many relationship between the post and the user table through the foreign key buyer_id.
#Meaning that each buyer will have many purchased posts but each post will have only one buyer.

class Post(models.Model):

    state = models.CharField(max_length=200, default= "New")
    expired = models.BooleanField(default= False)
    no_of_reports = models.IntegerField(null=True)
    title = models.CharField(max_length=100)
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
    is_sold = models.BooleanField()
    location = models.CharField(max_length = "100")


    
    #C1-Tharwat) returns to total number of reports on the current post
    def reportCount(self):
        return self.no_of_reports

    #C1-Tharwat) this method allows the admin to manually delete (Hide) a post
    def adminDeleteReportedPost(post):
        p = Post.objects.get(pk = post.id)
        p.is_hidden = True
        p.save()


    #(C1-Tharwat)This method automatically determines the state of the post. Whether it is (New, Old, or Archived)
    #The method takes in one parameter which is the post itself
    #the method compares the date of which the post was published in and the current date
    #It then uses an algorithim to determine the difference in number of days between the current date and the published date
    #Based on the amount returned, if the amount is less than 30 days, the state = "NEW", if between 30 and 60, the state = "OLD", if greater than 60, the state = "ARCHIVED"
    def postState(self):
        current_time = datetime.datetime.now()
        p = Post.objects.get(id = self.id)
        #used if the current year is greater than the year of the published post
        if current_time.year > self.pub_date.year:
            #this is in case for exmaple the published month of the post is December and the current month is January
            #Although the years are diff yet the diff in days may not be greater than 30
            #Ex: published date: 2012, 12, 28 ----- current date: 2013, 1, 10
            if current_time.month == 1 and self.pub_date.month ==12 and (current_time.day + (31 - self.pub_Date.day)) > 30:
                p.state = 'Old'
                p.save()
            #this is in case for exmaple the published month of the post is November and the current month is January
            #Although the years are diff yet the diff in days may not be greater than 30 and less than 60
            #Ex: published date: 2012, 11, 1 ----- current date: 2013, 1, 28
            elif current_time.month == 1 and self.pub_date.month ==11 and (current_time.day + (31 - self.pub_Date.day)) < 60:
                p.state = 'Old'
                p.save()
            else:
                p.state = 'Archived'
                p.save()
        #Used when the current year and Published year of the post are the same
        if current_time.year == self.pub_date.year:

            day_diff_diff_month = current_time.day + (31 - self.pub_date.day)
            day_diff_same_month = current_time.day - self.pub_date.day
            month_diff = current_time.month - self.pub_date.month
            
            if month_diff >= 1:
                month_diff = month_diff - 1
                total_diff = (month_diff*31) + day_diff_diff_month
            else:
                total_diff = day_diff_same_month
              
            if total_diff > 30 and total_diff < 60:
                p.state = 'Old'
                p.save()
            if total_diff > 60:
                p.state = 'Archived'
                p.save()

    def get_buyer():
        return self.buyer.id
 
        
# ''' C1_beshoy Cal Quality index this method takes a post and then calculate its quality 
# index based on the filled attributes and thier wight'''

    def cal_quality(self):
        q_index=0
        attr_list=Attribute.objects.filter(sub_channel_id=self.sub_channel_id_id)
        values_list_tmp=Values.objects.filter(Post_id=self.post_id_id)
        for Values in values_list_tmp:
            if Values.name_of_value is not None:
                attr_tmp=Attribute.objects.get(Attribute_id=Values.attribute_id_id)
                q_index=q_index+int(attr_tmp.weight)
        self.quality_index=q_indexUI    


    #C1-Tharwat) returns to total number of reports on the current post
    def report_count(self):
        return self.no_of_reports

    #(C1-Tharwat)This method automatically determines the state of the post. Whether it is (New, Old, or Archived)
    #The method takes in one parameter which is the post itself
    #the method compares the date of which the post was published in and the current date
    #It then uses an algorithim to determine the difference in number of days between the current date and the published date
    #Based on the amount returned, if the amount is less than 30 days, the state = "NEW", if between 30 and 60, the state = "OLD", if greater than 60, the state = "ARCHIVED"
    def post_state(self):
        current_time = datetime.datetime.now()
        post = Post.objects.get(id = self.id)
        #used if the current year is greater than the year of the published post
        if current_time.year > self.pub_date.year:
            #this is in case for exmaple the published month of the post is December and the current month is January
            #Although the years are diff yet the diff in days may not be greater than 30
            #Ex: published date: 2012, 12, 28 ----- current date: 2013, 1, 10

            if current_time.month == 1 and self.pub_date.month ==12 and (current_time.day + (31 - self.pub_date.day)) > 30:

                post.state = 'Old'
                post.save()
            #this is in case for exmaple the published month of the post is November and the current month is January
            #Although the years are diff yet the diff in days may not be greater than 30 and less than 60
            #Ex: published date: 2012, 11, 1 ----- current date: 2013, 1, 28

            elif current_time.month == 1 and self.pub_date.month ==11 and (current_time.day + (31 - self.pub_date.day)) < 60:

                post.state = 'Old'
                post.save()
            else:
                post.state = 'Archived'
                post.save()
        #Used when the current year and Published year of the post are the same
        if current_time.year == self.pub_date.year:

            day_diff_diff_month = current_time.day + (31 - self.pub_date.day)
            day_diff_same_month = current_time.day - self.pub_date.day
            month_diff = current_time.month - self.pub_date.month

            

            if month_diff >= 1:
                month_diff = month_diff - 1
                total_diff = (month_diff*31) + day_diff_diff_month
            else:
                total_diff = day_diff_same_month
            
            if total_diff > 30 and total_diff < 60:
                post.state = 'Old'
                post.save()
            if total_diff > 60:
                post.state = 'Archived'
                post.save()
    
    def __unicode__(self):
        return self.title

#c2-mohamed
#this class holds all notifications to all users
class Notification(models.Model):
    user = models.ForeignKey(UserProfile)
    content = models.CharField(max_length=100)
    read = models.BooleanField(default=False)
    url = models.CharField(max_length=50)
    image_url = models.CharField(max_length=50)
    not_date = models.DateTimeField(default=datetime.datetime.now())
    def __unicode__(self):
        return unicode(self.user.name) + "   " + unicode(self.content)

# This model defines the table of reports
# this table contains 3 attributes, the related post ID, the type of report chosen by the user, and the user reporting the post
# as the user reports a post after choosing a reason pre-defined in the system, a record is inserted in the table
# this table is used to retrieve the reports related to a certain post
class Report(models.Model):
    reported_post = models.ForeignKey(Post, related_name = 'reported_Post')
    report_type = models.CharField(max_length = 100)
    reporting_user = models.ForeignKey(UserProfile, related_name = 'reporting_user_id')
        
    def __unicode__(self):
        return (self.report_type)

class ReportReasons(models.Model):
    reported_reason = models.CharField(max_length = 50) 

    def __unicode__(self):
        return (self.reported_reason)

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
    def __unicode__(self):
        return self.name
#this table contains all attributes (attribute_id) refrencing class attribute with all their posiible values(value)
class AttributeChoice(models.Model):
    attribute_id = models.ForeignKey(Attribute)
    value = models.CharField(max_length=64)
    def __unicode__(self):
        return self.value

class Value(models.Model):
    attribute = models.ForeignKey(Attribute)
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
    choice = models.ForeignKey(AttributeChoice, null = True)
    class Meta: #to make sure a subscription doesn't exist twice
        unique_together = ("channel","sub_channel","parameter","choice")
    def subscribe_Bychannel(self, user_in): #this def subscribe users who wants to subscribe by channel
        try:
            UserSubchannelSubscription.objects.filter(user = user_in, parent_channel = self.channel).delete()
        except:
            pass
        channel_to_subscribe = self.channel
        subscription = UserChannelSubscription(user = user_in, channel = channel_to_subscribe)
        try:
            subscription.save()
        except:
            pass
        
    def subscribe_Bysubchannel(self, user_in): #this def subscribe users who wants to subscribe by subchannel
        self_parent_channel = self.sub_channel.channel
        UserChannelSubscription.objects.filter(user = user_in, channel = self_parent_channel).delete()
        sub_channel_to_subscribe = self.sub_channel
        subscription = UserSubchannelSubscription(user = user_in, parent_channel = self_parent_channel, sub_channel = sub_channel_to_subscribe)
        try:
            subscription.save()
        except:
            pass
        subchannels_with_same_channel = SubChannel.objects.filter(channel_id=self_parent_channel).count()
        subchannels_subscribed_with_same_channel = UserSubchannelSubscription.objects.filter(parent_channel=self_parent_channel, user=user_in).count()
        if subchannels_with_same_channel==subchannels_subscribed_with_same_channel:
            UserSubchannelSubscription.objects.filter(parent_channel=self.sub_channel.channel_id, user=user_in).delete()
            subscribe_to_channel = UserChannelSubscription(user=user_in,channel=self_parent_channel)
            subscribe_to_channel.save()
    def subscribe_Byparameter(self, user_in): #this def subscribe users who wants to subscribe by attributes
        sub_channel_to_subscribe = self.sub_channel
        self_parent_channel = self.channel
        subscription = UserParameterSubscription(user = user_in, parent_channel = self_parent_channel, sub_channel = sub_channel_to_subscribe, parameter = self.parameter, choice = self.choice)
        #C1-Tharwat --- This will remove a subscription by a subchannel if a user is subscribed to a specfic paramter in it
        try:
            UserSubchannelSubscription.objects.filter(user = user_in, sub_channel = sub_channel_to_subscribe).delete()
        except:
            pass
            
        try:
            subscription.save()
        except:
            pass
    def __unicode__(self):
        return unicode(self.id)

#C1-Tharwat) this model is the result of the Many-to-Many relationship between the model Users and Post
#this model takes in a the seller's id, buyer's id, and the post id (related to the seller)
#the model has a primary key combination of all 3 attributes
class InterestedIn(models.Model):
    user_id_buyer = models.ForeignKey(UserProfile, related_name = 'buyer')
    user_id_seller = models.ForeignKey(UserProfile, related_name= 'seller')
    post = models.ForeignKey(Post)

    class Meta:                    #gives the model a primary key of these attributes
        unique_together = ("user_id_buyer", "user_id_seller", "post")     
    
    def __unicode__(self):         #converts the INT to Strings to be displayed
        return unicode(self.post_id) 
    

#c2-mohamed
#This table holds different values for the attribute (i.e for each attribute there will be different values), attribute_id is a Foreignkey that references the id ofthe attribute from the attributes model,value is the name of the different values that would be given for the attributes, and Post_id is a Foreign key that references the id of the post from the posts model#    
class UserChannelSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    channel = models.ForeignKey(Channel)
    class Meta: #to make sure a user don't subscribe to same channel twice
        unique_together = ("user", "channel")
    def __unicode__(self):
        return unicode(self.user)

#c2-mohamed
#this table holds all users subscribed to subchannels
class UserSubchannelSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    parent_channel = models.ForeignKey(Channel)
    sub_channel = models.ForeignKey(SubChannel)
    class Meta: #to make sure a user doesn't have the same subscription twice
        unique_together = ("user", "parent_channel", "sub_channel")
    def __unicode__(self):
        return unicode(self.user)

#c2-mohamed
#this holds all users subscribed to parameters
class UserParameterSubscription(models.Model):
    user = models.ForeignKey(UserProfile)
    parent_channel = models.ForeignKey(Channel)
    sub_channel = models.ForeignKey(SubChannel)
    parameter = models.ForeignKey(Attribute)
    choice = models.ForeignKey(AttributeChoice)
    class Meta: #to make sure aa user won't have the same subscription twice
        unique_together = ("user", "parent_channel", "sub_channel", "parameter", "choice")
    def __unicode__(self):
        return unicode(self.user)


class Comment(models.Model):
    content=models.CharField(max_length="500")
    date=models.DateTimeField()
    is_Hidden=models.BooleanField(default=False)
    post_id= models.ForeignKey(Post)
    user_id=models.ForeignKey(UserProfile)
   #c1_hala_comment i added def unicode to return the post state 
   #to identify it while testing to make sure it is saved in d 
    #i added comment tabel to save data taken from user to save in db 
    #to easily retreive it from when needed in the post when comment is posted
    def __unicode__(self):
        return self.content

#c1_abdelrahman this is the class that holds the users and the posts they added in the wish list.
class WishList(models.Model):
    user = models.ForeignKey(UserProfile)
    post = models.ForeignKey(Post)
    class Meta:
        unique_together = ("post","user")

#c2-mohamed awad
#this class holds all records regarding the activity log of users
#it contains the content that will be shown to user
#the user that the content will be shown to
#the url the user will be directed to upon clicking
#the log_type whether it is commenting, posting, subscribing..etc.
class ActivityLog(models.Model):
    content = models.CharField(max_length = 100)
    user = models.ForeignKey(UserProfile)
    url = models.CharField(max_length = 100)
    log_type = models.CharField(max_length = 10)
    activity_date = models.DateTimeField(default = datetime.datetime.now())
    # activity_date = models.DateField()
    def __unicode__(self):
        return unicode(self.activity_date) + unicode(self.content)

class social_identifier(models.Model):
    user = models.ForeignKey(UserProfile)
    provider_name=models.CharField(max_length = 200)
    provider_uid=models.CharField(max_length = 200)

    class Meta: #to make sure a user doesn't have the same indentifier twice
        unique_together = ("user", "provider_name", "provider_uid")

