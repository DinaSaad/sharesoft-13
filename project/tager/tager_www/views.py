# Create your views here.
from django.http import HttpResponse
from tager_www.models import UserProfile, UserFriend, Friend
    def insertFriends (request):
        user_original = request.UserProfile
        user_original_id = user_original.id
        friend_original = request.UserFriend
        friend_original_id = friend_original.id
               
        variable = Friend(user_id=user_original_id, user_friend_id = friend_original_id )
        variable.save()

  		# takes the id of the user
  		# takes id of the user's friend
    	#assign to the user , his friend in the table friend !
