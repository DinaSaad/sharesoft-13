from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *


#the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response ('Profile.html',context_instance=RequestContext(request))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        
       return redirect("/login/")# Return an 'invalid login' error message.


def ViewPost(request):

    #post = Post.objects.get(pk= request.POST['post_id'])
    user = request.user
    rateSellerButtonFlag = user.canRate(request.POST['post_id']) 
    d = {'view_rating':rateSellerButtonFlag}
    
    return render_to_response('Post.html', d,context_instance=RequestContext(request))




