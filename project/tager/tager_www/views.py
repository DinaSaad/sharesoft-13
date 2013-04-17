from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm
from tager_www.models import UserProfile 


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




def get_channels (request):
    channels = Channel.objects.all()
    channels_list = [] 
    for channel in channels:
        subchannels = Subchannel.objects.filter(channel_id_id=channel.id)
        subchannels_list = []
        for subchannel in subchannels:
            attributes =  Attribute.objects.filter(subchannel_id_id=subchannel.id)
            subchannels_list.append({'subchannel': subchannel, 'attributes': attributes})
            
        channels_list.append({'channel': channel, 'subchannels_list': subchannels_list} )
    print channels_list
    results = Post.objects.all()
    
    # subchannel_dictionary = {'subchannel' , subchannel}
    
    return render(request, 'homepage.html', {'all_channels': channels_list ,'results': results} )


# def allPosts():
#      post_list = Post.objects.all()
#      return render( 'homepage.html',{'post_list': post_list}) 





# Reem- As  c3 , (a system) I should be able to provide  a refinement bar along while previwing the posts  
# - this method creats variable channels , to store all channels available in the database, 
# variable subchannels , to store all subchannels available in the database,
#  channels_list is a list that holds dictionaries of channels and its subchannels.
# subchannels_list is a list that holds dictionaries os subchannels and its attributes, 
# the method then return the channels_list only , as it holds , every attribute of subchannel
# and every subchannel of a channel 

def view_checked_subchannel_posts(request):
    subchannel_id = request.GET["subch_id1 "]
    original_posts = request.GET ["results"]
    print sub_channel_id
    current_subchannel = Subchannel.objects.get(id =subchannel_id)
    posts_of_subchannel = (Post.objects.filter(sub_channel_id= current_subchannel).order_by('-quality_index'))
    print posts_of_subchannel
    results=[]
    for sub in posts_of_subchannel:
        for post in original_posts:
            if sub.id == post.id:
                results.order_by('-quality_index')
            else:
                results.append(sub).order_by('-quality_index')
     
    return render(request, "refineResults.html", {'results': results})

 
# Reem- As  c3 , (a system) I should be able to provide  a refinement bar along while previwing the posts  
# subchannel_id is the id retrieved from the webpage 
# its is matched with with the subchannel id in the post model , 
# the method returns the dictionairy of posts related to specific subchannels.


# .order_by('-quality_index'))
    
# def homePosts(request):
#     post_list = Post.objects.all()
#         # .exclude(is_hidden=True)
#         # .order_by('-quality_index'))
#     return post_list
    # render(request, "homepage.html", {'post_list': post_list})

def excludePosts (request):
    sub_channel_id = request.GET["subch_id1 "]
    original_posts = request.GET ["results"]
    print sub_channel_id
    current_subchannel = Subchannel.objects.get(id =sub_channel_id)
    posts_of_subchannels = (Post.objects.filter(sub_channel_id= current_subchannel).order_by('-quality_index'))
    print posts_of_subchannels
    results= original_posts
    for sub in posts_of_subchannels:
        for post in original_posts:
            if sub.id == post.id:
                post = Post.objects.filter(id = sub.id)
                results.remove(post)
            
                
     
    return render(request, "refineResults.html", {'results': results})