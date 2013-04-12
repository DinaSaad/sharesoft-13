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
import datetime
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

# c1_hala viewPost method is a method that takes two parameters request and post_id,
#post variable is a variable that gets the Post from Post table with id that is matched with the id of post that entered
#as a parameter, and returns rendor-to-response that returns a post.html that contains the post itself that enters the methos
#as a parameter , that the user wants , and under that post there is a comment textarea and button called add that adds the
#comment the user wants to add under the post.
#and returns the variable post that returns the post the user comments on, and returns all the comments that related to
#this postt that were posted before.
def viewPost(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render_to_response('post.html', {'post':post, 'comments':Comment.objects.filter(post_id=post)}, context_instance=RequestContext(request))


#c1_hala this method called savingComment that takes two parameters request and post_id, the
#content variable takes from the request the content that the user types in, and userobject variable is a
#variable that the user as an object which rather than taking the user_id no takes the user as an object
#and saves it in the Comment table as an object, and post variable brings the post from post table with id
#that matches the post_id that taken as a paramter, and comment variable saves in the comment table
#the content taken and the date that was retreived at that time using datetime.now()
#and takes the user as an object, and takes the post id and saves it in the comment table.
#comment table by that saves each post with its comment content, date of the comment, and saves
#the users owner of the comment next to tthe comment. and at last the method returns the method viewPost
#which has the post and its past comments saved on it
def SavingComment(request, post_id):
    content = request.POST['content']
    userobject= request.user #UserProfile.objects.get(id=Comment.user_id)
    print request.user
    post = Post.objects.get(pk=post_id)
    # if userobject.is_active:
    comment = Comment(content=content, date=datetime.datetime.now(), user_id=userobject, post_id=post)
    comment.save()
    return viewPost(request, post_id)





# c1_hala this method called removePost that takes two parameters request and post id
#request parameter to bring the user from the request, and check if he is an admin or not
#and created a variable called hidepost that gets from Post object the post with id that matches
#the post_id that entered from the user as a parameter that he wants to bring
#and if he is an admin he will set the hidepost attribute is_hidden from false to true
#so the post would be hidden and unavailable, and returns the post.htmlagain without the post to make sure it is hidden
#while if he isnt and admin he will be redirected to HTTPResponse that says to the user you aren't an admin to be able to
#change state of is_hidden to true.
def removePost(request, post_id):
    admin= request.user
    hidepost=Post.objects.get(pk=post_id)
    if admin.is_admin:
        hidepost.is_hidden = True
        hidepost.save()
        return viewPost(request, post_id)
    else:
        hidepost.is_hidden = False
        # return viewPost(request, post_id)
        return HttpResponse("you aren't an admin to be able to delete post")



