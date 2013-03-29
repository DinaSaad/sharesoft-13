from django.db import models
from django.contrib.auth.models import User



class UserFriend(models.Model):
    user = models.ForeignKey(User)
    # user_id = models.ForeignKey(UserProfile)
    email = models.CharField(max_length="50")

    # this class is like a temporary class to hold the user's friend data , to be matched later with the user

class Friend(models.Model):

    user_id = models.ForeignKey(UserProfile)
    user= user_id
    user_friend_id = models.ForeignKey(UserFriend) 
    user_friend = user_friend_id
    unique_together = (("user_id", "user_friend_id"),)
    # this class takes the user id and his friends id and insert them into table friend , 
    # where each user id matches with his friend's id

class UserProfile():


class Channel():


class Subchannel():



class Attribute():


class Post():


class Comments():



class Subscribtion():



class Notification():


class InterestedIn():
	



