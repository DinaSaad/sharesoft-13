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

    def getInterestedIn(self,post_id):
        interested = Interested_In.objects.filter(user_id_seller = user_id_seller, post_id = post_id)
        return interested

    def interestedIn(self, seller, post_id):
        interested = interested_IN(user_id_buyer = user_id_buyer, user_id_seller = seller, post_id = post)
        interested.save()

      
    


class Channel():


class Subchannel():



class Attribute():


class Post():

    class Post(models.Model):
    post_id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(User)

    def __unicode__(self):
        return unicode(self.post_id)

   # def canRate(self,user):
    #    post = Post.objects.filter(pk= post_id)
        #user = UserProfile.objects.filter(pk= user_id)
     #   if post.is_sold = true && post.buyer_id = user.id
      #      return True
       # else:
        #    return False

    def canRate(self,user):
        current_user = user
        if self.is_sold = true && self.buyer_id = user.id
            return True
        else:
            return False



class Comments():



class Subscribtion():



class Notification():


class Interested_In(models.Model):
    user_id_buyer = models.ForeignKey(User, related_name = 'buyer')
    user_id_seller = models.ForeignKey(User, related_name= 'seller')
    post_id = models.ForeignKey(Post)
    class Meta:
        unique_together = ("user_id_buyer", "user_id_seller", "post_id")   




