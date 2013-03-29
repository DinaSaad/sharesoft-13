from django.db import models
from django.contrib.auth.models import User


class UserProfile():


class Channel():


class Subchannel():



class Attribute():


class Post():


class Comments():



class Subscribtion():




# the class Post identifies the post_id which is unique identification for the post
        
class Post(object):
    post_id=models.IntegerField
    num_of_posts=models.IntegerField()

    def ___unicode___(object):
        return unicode(post_id)



    # this method takes one argument which is the user an the method check that this user is :
    # logged in and verified or not 
    # an admin
    # free user and his number of posts less than 3
    #premium user and his numhber of posts less than 10 

    #otherwise this user cant post 




def  Can_Post(self)
       

        if all ([UserProfile.is_premium , num_of_posts<10, UserProfile.is_verified , UserProfile.is_admin ]):
            

            return true
        else
            if all ([UserProfile.is_premium==False, num_of_posts<10,]) :
            return true 


            else 

            return false 






def getValueList (posts, user_id):



    valueList = [] # array to hold list of values collected


    rows = arcpy.SearchCursor(posts) # create search cursor



    # iterate through table 

    for row in rows:

        value = row.getValue(user_id)



    

    valueList.sort()

    return valueList      # this list contains all users who have posts




#####

   #this method loops  valuelist list and returns number of posts that a certain user did using user_id 
def get_number_of_posts(self)

user = self.user_id 
valuelist.count(user_id)        ## predefined method which calculates number of occurance of ceratin user id in the list            
num_of_posts = valuelist.count

return num_of_posts



class Notification():


class InterestedIn():
	



