from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm
from tager_www.models import UserProfile, Post, Comment 
import sqlite3
from django.utils import timezone


def home(request):
    return render_to_response ('home.html',context_instance=RequestContext(request))

#C2-mahmoud ahmed-the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.

def view_channels(request):
    list_of_channels = Channel.objects.all()    
    return render(request, 'index.html', {'list_of_channels': list_of_channels})

def view_subchannels(request):
    s_id = request.GET['ch_id']
    current_channel = Channel.objects.filter(pk=s_id)
    list_of_subchannels = Subchannel.objects.filter(channel_id = current_channel)
    return render(request, 'index.html', {'list_of_subchannels': list_of_subchannels})

def login(request):
    #print request
    #print "ldnfldnfndlfd"
    #print request.method
    mail = request.POST['email']
    password = request.POST['password']
   # print "before"
    # user = UserProfile.objects.get(email=mail)
    # print user.username
    # pk = user.username
    authenticated_user = authenticate(mail=mail, password=password)
    if authenticated_user is not None:
        print "auth"
        print authenticated_user.is_active
        if authenticated_user.is_active:
            print "act"
            django_login(request, authenticated_user)
            return render_to_response ('profile.html',context_instance=RequestContext(request))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        return render_to_response ('home.html',context_instance=RequestContext(request))
       #return redirect("/login/")# Return an 'invalid login' error message.

#C2-mahmoud ahmed-this isn't all of view post but this part that i did is concerend with the apperance of the
#the rate the seller button which would appear to the buyer of the post only so what it does is
#it takes object user from the session and checks if this user can rate the post that is imbeded in 
#the request and then add the results in the dictonary.Then render the post html and pass the 
#dictionary.
#
def view_post(request):

    post = Post.objects.get(pk= request.POST['post_id'])
    user = request.user
    creator = False
    if post.user_id == user:
         creator = True
    rateSellerButtonFlag = user.canRate(request.POST['post_id']) 
    d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator}
    
    if request.method == 'POST':
        form = BuyerIdentificationForm( request.POST )
        if form.is_valid():
            new_buyer_num = form.GetBuyerNum()
            buyer_added = user.add_Buyer(post, new_buyer_num)
            return HttpResponseRedirect( "/" )
        else :
            d.update({'form':form})
            return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

    else:
        form = BuyerIdentificationForm()
        d.update({'form':form})
    return render_to_response( "Post.html", d,context_instance = RequestContext( request ))



class CustomAuthentication:
    def authenticate(self, mail, password):
        try:
            user = UserProfile.objects.get(email=mail)
            if user.password == password:
                return user
        except UserProfile.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return UserProfile.object.get(pk=user_id)
        except UserProfile.DoesNotExist:
            return None




def  get_user(self):    
    User = get_user_model()
    return User



def UserRegistration(request):
     #if the user is already logged in , registered , go to profile 
    #if request.user.is_authenticated():
     #   return HttpResponseRedirect('/profile/')
     #if they r submitting the form back
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # takes the registeration form and fills it with what is entered
        if form.is_valid(): # validates all the fields on the firm,The first time you call is_valid() or access the errors attribute of a ModelForm triggers form validation as well as model validation.
                user = UserProfile.objects.create_user(name=form.cleaned_data['name'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
                user.save() # this creates the user 
                
                return HttpResponseRedirect('/profile/')
        else:
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        #add our registration form to context
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))

def commenting(request, pk):
#"""Add a new comment."""
    p = request.POST

    if p.has_key("content"):

        comment = Comment(post=Post.objects.get(pk=pk))
        cf = CommentForm(p, instance=comment)
        comment = cf.save(commit=False)
        comment.save()
        return HttpResponseRedirect(reverse("db.tager_www.views.post", args=[pk]))
# c1_hala this method purpose is to add a new comment, the method takes two parameters the request itself and the primary key
#variable p takes the request then checks if the request
#contains content ,then will make new variable called comment that will bring the comment table part that
# relates to post with pk = pk that taken as a parameter in the method, and saves in it the comment then the method
#redirects the user to page of the post.


# def view_posts_comments(request):
#     post_id = request.GET['post_id']
#     comments_of_posts = Comment.objects.filter(post_id_id= post_id)
#     return render(request, 'homepage.html', {'comments_of_posts': comments_of_posts})

 



# def commenting(request):
    # # if user.is_active:
    # #     if user.is_verfied:
    # if request.method == 'POST':
    #     form = RegistrationForm(request.POST)
    #     if form.is_valid():
    #         user=UserProfile.objects.all()
    #         post=Post.objects.all()
    #         p=Comment(content=request.POST['content'], date=timezone.now(), post_id=post[0], user_id=user[0].user_id)
    #         p.save()
    #         html = "<html><body>It is now .</body></html>" 
    #         return HttpResponse(html)
    #             # return HttpResponseRedirect('Comments.html')
    #     else:
    #             return render_to_response('Comments.html', {'form': form}, context_instance=RequestContext(request))
    # else:
    #     ''' user is not submitting the form, show them a blank registration form '''

    #     html = "<html><body>It is now .</body></html>" 
    #     return HttpResponse(html)
    #     # context = {'form': form}
    #     # return render_to_response('Comments.html', context, context_instance=RequestContext(request))

    
    # #     else:
    # #        return HttpResponse ("sorry your account is not verfied") # Return a 'disabled account' error message
    # # else:
        
    # #   return redirect("/login/")# Return an 'invalid login' error message.



def view_comments(request, pk):
#"""Single post with comments and a comment form."""
    post = Post.objects.get(pk=int(pk))
    comments = Comment.objects.filter(post=post)
    d = dict(post=post, comments=comments, form=CommentForm(), user=request.user)
    d.update(csrf(request))
    return render_to_response("post.html", d)
    # return render_to_response(request, 'Comments.html', {'List of comments':com},context_instance=RequestContext(request))

#c1_hala this method purpose is to view the comments, 
#so the method takes 2 parameters one the request it self and one the primary key
#post variable takes the result of search in Post table for the post with primary key = the primary key the user wants
#then variable d goes to dictionary and brings from it the post information saved about it that i brought in variable post 
#and brings from it the old comments saved in that particular post and the user who commented 
#then variable d is updated with the info from the dictionary, and the method response with post.html that has the post 
# and the commented needed that was posted before.











    
