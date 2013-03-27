from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *

def ViewPost(request):

    post = Post.objects.get(pk= request.POST['post_id'])
    user = request.user
    rateSellerButtonFlag = post.canRate(user) 
    d = {'view_rating':rateSellerButtonFlag}
    return render_to_response('Post.html', d)


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







