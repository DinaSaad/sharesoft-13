from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm , PostForm
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
    return render_to_response('index.html', {'list_of_subchannels': list_of_subchannels})

def add_post(request):
    sub_channel_id = request.GET['sub_ch_id']
    current_sub_channel = Subchannel.objects.get(id = sub_channel_id)
    list_of_attributes = Attribute.objects.filter(subchannel_id=current_sub_channel)
    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
        author = request.user
        subchannel  = Subchannel.objects.get(pk=sub_channel_id)
        p = Post.objects.create(quality_index = "0", title = form.cleaned_data['title']
            ,description = form.cleaned_data['description'] 
            ,price = form.cleaned_data['price']
            ,user = author
            ,sub_channel_id = subchannel
            ,profile_picture = form.cleaned_data['picture']
            ,picture1 = form.cleaned_data['picture1']
            ,picture2 = form.cleaned_data['picture2']
            ,picture3 = form.cleaned_data['picture3']
            ,picture4 = form.cleaned_data['picture4']
            ,picture5 = form.cleaned_data['picture5'])

        
        for k in request.POST:
            if k.startswith('option_'):
                Value.objects.create(attribute_id_id=k[7:], value= request.POST[k], Post_id_id = p.id)    
        return HttpResponse("Thank you for adding your post")
    else:
        form = PostForm()
        initial={'subject': 'I love your site!'}
    

    return render_to_response('index.html', {'form': form, 'add_post': True, 'list_of_attributes': list_of_attributes})

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

def view_post(request):
    post_id = Post.objects.get(id=6)
    subchannel1 = post_id.sub_channel_id
    list_of_att_name = Attribute.objects.filter(subchannel_id = subchannel1)
    list_of_att_values = Value.objects.filter(Post_id = post_id)
    post = post_id
    return render(request, 'ViewPost.html', {'post': post, 'list_of_att_name': list_of_att_name, 'list_of_att_values': list_of_att_values})

# def view_post(request):

#     post = Post.objects.get(pk= request.POST['post_id'])
#     user = request.user
#     creator = False
#     if post.user_id == user:
#          creator = True
#     rateSellerButtonFlag = user.canRate(request.POST['post_id']) 
#     d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator}
    
#     if request.method == 'POST':
#         form = BuyerIdentificationForm( request.POST )
#         if form.is_valid():
#             new_buyer_num = form.GetBuyerNum()
#             buyer_added = user.add_Buyer(post, new_buyer_num)
#             return HttpResponseRedirect( "/" )
#         else :
#             d.update({'form':form})
#             return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

#     else:
#         form = BuyerIdentificationForm()
#         d.update({'form':form})
#     return render_to_response( "Post.html", d,context_instance = RequestContext( request ))



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

#C1-Tharwat) This method directs the user to the report page to select a reason for reporting a post
def goToTheReportPage(request):
    return render_to_response('report.html')

#C1-Tharwat) This method takes the user input(reason) for reporting a post and calls the reportPost method in models.py
#reportPost in models.py then takes action to finish the reporting proccess
def reportThePost(request):
    return HttpResponse("hello")









    
