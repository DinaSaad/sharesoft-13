from django.db import models
from django.contrib.auth.models import User

# this class has the user information for creation 
# it extends User model built in django which include username, email , password ,firstname , lastname 
class UserProfile(models.Model):       
    # date_Of_birth = models.DateField(null=True, blank=True)
    # is_admin = models.BooleanField(default=False)           
    # is_verfied = models.BooleanField(default=False)
    # is_premium = models.BooleanField(default=False)
    # photo = models.ImageField(upload_to='img',blank=True)
    # activation_key = models.BooleanField(default=False)
    # status = models.CharField(max_length=400) 
    # gender_choices = (
    #     ('M', 'Male'),
    #     ('F', 'Female'),
    # )
    # gender = models.CharField(max_length=1, choices=gender_choices)
    # users = models.ManyToManyField("self") # many users can add many users to their networks (profile)
    user_id = models.IntegerField(primary_key=True)

    def __unicode__(self):
        return unicode(self.user_id)

    # def __unicode__(self):               # returns name in string 
    #   return self.user_name

    #This method returns to the Seller (User) the list of buyers (User) interested in his (specific) post
    def getInterestedIn(self, post):         
        p = Post.objects.get(post_id= post)
        interested = InterestedIn.objects.filter(user_id_seller_id = self.user_id, post_id_id = p.post_id)
        return interested.user_id_buyer

class Post(models.Model):
    post_id = models.IntegerField(primary_key = True)
    user_id = models.ForeignKey(UserProfile)
    def __unicode__(self):
        return unicode(self.post_id)

# this model is the result of the Many-to-Many relationship between the model Users and Post
# this model takes in a the seller's id, buyer's id, and the post id (related to the seller)
# the model has a primary key combination of all 3 attributes
class InterestedIn(models.Model):
    user_id_buyer = models.ForeignKey(UserProfile, related_name = 'buyer')
    user_id_seller = models.ForeignKey(UserProfile, related_name= 'seller')
    post_id = models.ForeignKey(Post)

    class Meta:                    #gives the model a primary key of these attributes
        unique_together = ("user_id_buyer", "user_id_seller", "post_id")     
    
    def __unicode__(self):         #converts the INT to Strings to be displayed
        return unicode(self.post_id) 
    
