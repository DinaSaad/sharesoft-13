from django.http import HttpResponse
from django.shortcuts import render
from tager_www.models import UserProfile
#This method return to the templates true or false. if it returns true this means that the user can see the post button 
#if false this means that the user can not see the add post button.
#it is done by getting the current user requesting the view and invoke the method of canPost on it. 
#If it returns true it will be transferred to the template as a dictionary
def index(request): 
	# current_user = request.UserProfile
	current_user = UserProfile.objects.filter(pk=1)
	can_see_button = current_user.canPost()
	return render(request, 'index.html', {'can_post':can_see_button})
