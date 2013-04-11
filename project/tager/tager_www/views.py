from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm
from tager_www.models import UserProfile 


def return_channels(request):
    channels = Channel.objects.all()
    return render_to_response ('subscriptions.html', {'channels': channels})

def return_subchannels(request):
    s_id = request.GET['ch_id']
    print s_id
    channels = Channel.objects.all()
    current_channel = Channel.objects.get(id=s_id)
    subchannels = Subchannel.objects.filter(channel_id = current_channel)
    return render_to_response ('subscriptions.html', {'subchannels': subchannels, 'channels': channels})

def return_parameters(request):
    sc_id = request.GET['sch_id']
    channels = Channel.objects.all()
    s_id = Subchannel.objects.get(id = sc_id).channel_id
    subchannels = Subchannel.objects.filter(channel_id = s_id)
    parameters = Attribute.objects.filter(subchannel_id = sc_id)
    return render_to_response ('subscriptions.html', {'subchannels': subchannels, 'channels': channels, 'parameters': parameters})

def return_choices(request):
    p_id = request.GET['p_id']
    subchannel_of_parameter = Attribute.objects.get(id = p_id).subchannel_id
    parameters = Attribute.objects.filter(subchannel_id = subchannel_of_parameter)
    channels = Channel.objects.all()
    subchannels = Subchannel.objects.all()
    choices = AttributeChoice.objects.filter(attribute_id = p_id)
    return render_to_response ('subscriptions.html', {'subchannels': subchannels, 'channels': channels, 'parameters': parameters, 'choices': choices})

def subscription_by_chann(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    user_id = request.user
    user = UserProfile.objects.get(id = user_id)
    subscription = Subscription.objects.get(channel=channel,sub_channel=None,parameter=None,choice=None)
    subscription.subscribe_Bychannel(user)
    return HttpResponseRedirect("subscriptions.html")

def subscription_by_subchann(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    sch_id = request.GET['sch_id']
    subchannel=Subchannel.objects.get(id=sch_id)
    user_id = request.user
    user = UserProfile.objects.get(id = user_id)
    subscription = Subscription.objects.get(channel=channel,sub_channel=subchannel,parameter=None,choice=None)
    subscription.subscribe_Bychannel(user)
    return HttpResponseRedirect("subscriptions.html")

def subscribe_by_parameters(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    sch_id = request.GET['sch_id']
    subchannel=Subchannel.objects.get(id=sch_id)
    p_id = request.GET['p_id']
    parameter=Attribute.objects.get(id=p_id)
    cho_id = request.GET['cho_id']
    choice=AttributeChoice.objects.get(id=p_id)
    user = UserProfile.objects.get(id = user_id)
    subscription = Subscription.objects.get(channel=channel,sub_channel=subchannel,parameter=parameter,choice=choice)
    subscription.subscribe_Bychannel(user)
    return HttpResponseRedirect("subscriptions.html")

def return_notification(request):
    # user_in_email = request.POST['email']
    user_in = UserProfile.objects.get(email = '1@3.com')
    all_notifications = Notification.objects.filter(user = user_in)
    if all_notifications is not None:
        return render_to_response ('notifications.html', {'all_notifications': all_notifications})
    else:
        pass


def home(request):
    return render_to_response ('home.html',context_instance=RequestContext(request))

#C2-mahmoud ahmed-the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.

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










    
