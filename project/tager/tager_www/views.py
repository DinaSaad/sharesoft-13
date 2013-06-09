from django.contrib.auth.models import User, check_password
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import *
from tager_www.models import UserProfile 
from django import forms 
import random 
import string
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.core.mail import send_mail 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.core.mail import send_mail
from django.template import loader, Context
from django.template.loader import get_template
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render_to_response
from django.shortcuts import RequestContext
import re
import os

from tager_www.models import Post , UserProfile , Channel
from django.db.models import Q
import urllib
from django.utils.timezone import utc
import datetime
from datetime import datetime, timedelta
from django.conf import settings
from twilio.rest import TwilioRestClient
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
# from django.core.files import File 
import urllib2, urlparse
from django.core.files.base import ContentFile
import json
import pusher
from django.core import serializers

pusher.app_id = settings.PUSHER_APP_ID
pusher.key = settings.PUSHER_KEY
pusher.secret = settings.PUSHER_SECRET
push = pusher.Pusher()

APP_ID = '461240817281750'   # From facebook app's settings
APP_SECRET = 'f75f952c0b3a704beae940d38c14abb5'  # From facebook app's settings
LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000'  # The url that the user will be redirected to after logging in with facebook 
REDIRECT_URL = 'http://127.0.0.1:8000/main'
FACEBOOK_PERMISSIONS = ['email', 'user_about_me','user_photos']  # facebook permissions
FACEBOOK_FRIENDS_PERMISSIONS = ['friendlists'] 
SCOPE_SEPARATOR = ' '

LOGIN_URL="/login/"
login_url="/login/"

import urllib
import urllib2
import json
from django.contrib import auth

def social_login(request):
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        return HttpResponseRedirect('/')

    api_params = {
        'token': token,
        'apiKey': settings.JANRAIN_RPX_API_KEY,
        'format': 'json',
    }

    janrain_response = urllib2.urlopen(
            "https://rpxnow.com/api/v2/auth_info",
            urllib.urlencode(api_params))
    resp_json = janrain_response.read()
    auth_info = json.loads(resp_json)
    print auth_info['stat']
    u = None
    profile = None
    print auth_info['profile']
    form = PostForm(request.POST,request.FILES)


    if auth_info['stat'] == 'ok':
        profile = auth_info['profile']
        print profile.get('providerName')
        if UserProfile.objects.filter(email=profile.get('email')).exists():
            tmp=UserProfile.objects.get(email=profile.get('email'))
            if social_identifier.objects.filter(user=tmp,provider_name=profile.get('providerName'),provider_uid=profile.get('identifier')).exists():
                #User exist and identifier for that provider exists >> Now authorizee
                authenticate_social_login(request,tmp)
                return HttpResponseRedirect("/profile?user_id="+str(tmp.id))# Redirect to a success page.
            else : 
            #incase the user didt use that provider befour
                social_obj= social_identifier(user=tmp,provider_name=profile.get('providerName'),provider_uid=profile.get('identifier'))
                social_obj.save()
                #User and provider identifier added >> Now authorizee
                authenticate_social_login(request,tmp)
                return HttpResponseRedirect("/profile?user_id="+str(tmp.id))# Redirect to a success page.

        else: #incase of new user

            if profile.get('providerName') =="Twitter": 
            #if provider is twitter , get teh info then redirect to twiiter page to get the email
              fbidtmp=facebook_uid=profile.get('identifier')
              jmail=fbidtmp+"tmp@tager.com"
              juser=UserProfile(name=profile.get('displayName'),
                   facebook_uid=profile.get('identifier'),email=jmail)
              print "will render"
              return render (request, 'twitter.html', {'title':'Add your Twitter Email','user':juser})

            else : 
            #incase of other provider and a new user
                juser=UserProfile.objects.create_user(name=profile.get('displayName'),
                     email=profile.get('email'),is_verfied=True)

                """Store image locally  if facebook"""
                if profile.get('providerName') =="Facebook": 
                    image_url = profile.get("photo") # get this url from somewhere
                    image_data = urllib2.urlopen(image_url, timeout=5)
                    filename = urlparse.urlparse(image_data.geturl()).path.split('/')[-1]
                    print filename
                    juser.photo = filename
                    juser.photo.save(
                        filename,
                        ContentFile(image_data.read()),
                        save=False
                    )

                #genrate 14 char password then send it to the user
                juser.password = ''.join(random.choice(string.ascii_uppercase + string.digits+ juser.email) for x in range(14))
                title = "Auto Genrated Password"
                content = "You recived this email for using our social login ,Please Change your password , your auto genrated password is: " + str(juser.password) 
                send_mail(title, content, 'mai.zaied17@gmail.com.', [juser.email], fail_silently=False)
                juser.save()
                #added the social login info to social_ident table
                social_obj= social_identifier(user=juser,provider_name=profile.get('providerName'),provider_uid=profile.get('identifier'))
                social_obj.save()
                #User and provider identifier added >> Now authorizee
                authenticate_social_login(request,juser)
                return HttpResponseRedirect("/profile?user_id="+str(juser.id))# Redirect to a success page.

    return None

def authenticate_social_login(request,juser):
    authenticated_user = authenticate(mail=juser.email, password=juser.password)
    if authenticated_user is not None:
        if authenticated_user.is_active:
            django_login(request, authenticated_user)
            print "auth success logged"
            return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        print "auth failed"
        return render_to_response ('home.html',context_instance=RequestContext(request))


def twitter_reg(request):
  identifier = request.POST['twitterlink']
  jemail= request.POST['email']
  jname= request.POST['name']
  juser=UserProfile(name=jname,
       facebook_uid=identifier,email=jemail)
  juser.password = ''.join(random.choice(string.ascii_uppercase + string.digits+ juser.email) for x in range(20))
  title = "Auto Genrated Password"
  content = "You recived this email for using our social login ,Please Change your password , your auto genrated password is " + str(juser.password) 
  send_mail(title, content, 'mai.zaied17@gmail.com.', [juser.email], fail_silently=False)
  juser.save()
  social_obj= social_identifier(user=juser,provider_name="Twitter",provider_uid=identifier)
  social_obj.save()
  authenticate_social_login(request,juser)
  return HttpResponseRedirect("/profile?user_id="+str(juser.id))# Redirect to a success page.






class CustomAuthentication:
  def authenticate(self, mail, password):
      try:
          user = UserProfile.objects.get(email=mail)
          pwd_valid = check_password(password, user.password)
          if pwd_valid:    
              return user
      except UserProfile.DoesNotExist:
          return None

      try:
          user = UserProfile.objects.get(email=mail)
          if user.password == password:
              return user              
      except UserProfile.DoesNotExist:
          return None


          


  def get_user(self, user_id):
      try:
          return UserProfile.objects.get(pk=user_id)
      except User.DoesNotExist:
          return None  







def home(request):
    return render_to_response ('home.html',{'title':'Welcome to Tager'},context_instance=RequestContext(request))


def return_channels(request):
    channels = Channel.objects.all()
    return render(request, 'subscriptions.html', {'channels': channels})

#c2-mohamed awad
#this def return subchannels to subscriptions.html for the user to choose a subchannel to subscribe to
#it takes a request containing the channel id the user has choosen in subscriptions.html and returns all subchannels
#of that channel for the user to subscribe to
def return_subchannels(request):
    s_id = request.GET['ch_id']
    print s_id
    channels = Channel.objects.all()
    current_channel = Channel.objects.get(id=s_id)
    subchannels = SubChannel.objects.filter(channel_id = current_channel)
    print {'subchannels': subchannels}
    return render(request, 'subscriptions.html', {'subchannels': subchannels})

#c2-mohamed awad
#this def returns parameters to subscriptions.html for the user to choose a parameter to subscribe to
#it takes a request containing the subchannel id the user has choosen in subscriptions.html and returns all attributes
#of that subchannel for the user to choose from
def return_parameters(request):
    sc_id = request.GET['sch_id']
    channels = Channel.objects.all()
    s_id = SubChannel.objects.get(id = sc_id).channel_id
    subchannels = SubChannel.objects.filter(channel_id = s_id)
    parameters = Attribute.objects.filter(subchannel_id = sc_id)
    return render (request, 'subscriptions.html', {'subchannels': subchannels, 'channels': channels, 'parameters': parameters})
#c2-mohamed awad
#this def return choices to subscriptions.html for the user to choose a choice to subscribe to
#it takes a request containing the parameter id the user has choosen in subscriptions.html and returns all choices
#of that parameter for the user to subscribe to
def return_choices(request):
    p_id = request.GET['p_id']
    subchannel_of_parameter = Attribute.objects.get(id = p_id).subchannel_id
    parameters = Attribute.objects.filter(subchannel = subchannel_of_parameter)
    channels = Channel.objects.all()
    subchannels = SubChannel.objects.all()
    choices = AttributeChoice.objects.filter(attribute_id = p_id)
    return render (request, 'subscriptions.html', {'subchannels': subchannels, 'channels': channels, 'parameters': parameters, 'choices': choices})

#c2-mohamed awad
#this def allows user to subscribe by channel only
#it takes as a request the channel id the user is subscribed to and saves a new record in UserChannelSubscription table
#containing the user and channel as attributes
def subscription_by_chann(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    user = request.user
    print user
    subscriptions = Subscription.objects.filter(channel=channel).exclude(sub_channel__isnull=True,parameter__isnull=True,choice__isnull=True)
    for subscription in subscriptions:
        subscription.subscribe_Bychannel(user)
        break
    return render(request, 'subscriptions.html')

#c2-mohamed awad
#this def allows user to subscribe by subchannel only
#it takes as a request the channel id  and sub channel id the user is subscribed to and saves a new record in UserSubChannelSubscription table
#containing the user, channel, and subchannel as attributes
def subscription_by_subchann(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    sch_id = request.GET['sch_id']
    subchannel=SubChannel.objects.get(id=sch_id)
    user = request.user
    subscriptions = Subscription.objects.filter(channel=channel,sub_channel=subchannel).exclude(parameter__isnull=True,choice__isnull=True)
    for subscription in subscriptions:
        subscription.subscribe_Bysubchannel(user)
        break
    return render(request, 'subscriptions.html')

#c2-mohamed awad
#this def allows user to subscribe by parameters
#it takes as a request the channel id, subchannel id, parameter id and choice id the user is subscribed to and saves a new record in UserParameterSubscription table
#containing the user, channel, parameter and choice as attributes
def subscribe_by_parameters(request):
    ch_id = request.GET['ch_id']
    channel=Channel.objects.get(id=ch_id)
    sch_id = request.GET['sch_id']
    subchannel=SubChannel.objects.get(id=sch_id)
    p_id = request.GET['p_id']
    parameter=Attribute.objects.get(id=p_id)
    cho_id = request.GET['cho_id']
    choice=AttributeChoice.objects.get(id=p_id)
    user = request.user
    print user
    subscriptions = Subscription.objects.filter(channel=channel,sub_channel=subchannel,parameter=parameter,choice=choice)
    for subscription in subscriptions:
        subscription.subscribe_Byparameter(user)
        break
    return render(request, 'subscriptions.html')

#c2-mohamed awad
#this def takes a user as a request and returns all his related notifications to notifications.html
#from Notification table
def return_notification(request):
    user_in = request.user
    all_notifications = Notification.objects.filter(user = user_in).order_by('not_date').reverse()
    if all_notifications is not None:
        return render (request, 'notifications.html', {'all_notifications': all_notifications})
    else:
        pass

def view_login(request):
    return render_to_response ('login.html',context_instance=RequestContext(request))




def view_channels(request):
    list_of_channels = Channel.objects.all()    
    return render(request, 'addPost.html', {'list_of_channels': list_of_channels})

def view_subchannels(request):
    user = request.user
    sub_channel_id = request.GET['ch_id']
    current_channel = Channel.objects.filter(pk=sub_channel_id)
    list_of_subchannels = SubChannel.objects.filter(channel_id = current_channel)
    return render(request, 'addPost.html', {'user':user,'list_of_subchannels': list_of_subchannels})
#c1_abdelrahman the add_post function requires the user to be logged in.
#the sub_channel_id is received from the previous view. it displays a form to the user. 
#if the user filled the form correctly then the user will be redirected to the homepage. 
# if the form is not valid the form will be reloaded.
@login_required
def add_post(request):
    author = request.user
    sub_channel_id = request.GET['sub_ch_id']
    current_sub_channel = SubChannel.objects.get(id = sub_channel_id)
    list_of_attributes = Attribute.objects.filter(subchannel_id=current_sub_channel)

    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
        subchannel1  = SubChannel.objects.get(pk=sub_channel_id)
        p = Post.objects.create(quality_index = "0", title = form.cleaned_data['title']
            ,description = form.cleaned_data['description'] 
            ,price = form.cleaned_data['price']
            ,seller = author
            ,subchannel = subchannel1
            ,profile_picture = form.cleaned_data['picture']
            ,picture1 = form.cleaned_data['picture1']
            ,picture2 = form.cleaned_data['picture2']
            ,picture3 = form.cleaned_data['picture3']
            ,picture4 = form.cleaned_data['picture4']
            ,picture5 = form.cleaned_data['picture5']
            ,location = form.cleaned_data['location']
            ,
            )

        # p.post_Notification()
         
        
        for k in request.POST:
            if k.startswith('option_'):
                Value.objects.create(attribute_id=k[7:], value= request.POST[k], post_id = p.id)
                #c2-mohamed
                #the next try statement is to insert the value if new in AttributeChoice table
                # try:
                #     attribute_needed = Attribute.objects.get(pk=k[7:])
                #     AttributeChoice.objects.create(attribute_id = attribute_needed, value = request.POST[k])
                # except:
                #     pass
        #c2-mohamed
        #the next line calls post_Notification() to send notification to all subscribed users
        #to that post
        post_Notification(p)
        #c2-mohamed
        #the next five lines are written to save a tuple in ActivityLog table
        #to save it to make the user retrieve it when he logs into his activity log
        post_activity_content = "you posted in " + unicode(current_sub_channel.name) + "."
        post_activity_url = "showpost?post=" + unicode(p.id)
        post_log_type = "post"
        # post_log_date = datetime.datetime.now()
        log = ActivityLog.objects.create(content = post_activity_content, url = post_activity_url, log_type = post_log_type, user = author, activity_date = datetime.now())
        return HttpResponseRedirect('/main')
    else:

        form = PostForm()
        initial={'subject': 'I love your site!'}
    

    return render(request,'addPost.html', {'form': form, 'add_post': True, 'list_of_attributes': list_of_attributes})


#c2-mohamed awad
#this method saves notification in Notification table using content and user id
#first i find all users interested and subscribed to this post whether by channel, subchannel or parameter subscription
#this is done by finding all users subscribed to channel of the post and we add them to users_subscribed_to_channel_array
#then we find all users subscribed to subchannel of the post then we add it to users_subscribed_to_subchannel_array
#then we find all users subscribed to all attributes and values of the post and we add it to all_users_subscribed to attributes
#then we record all notifications in Notification table
def post_Notification(self):
    print self
    print "xxxxxxxxxxxxxxxxxxxxxx"
    post_owner = self.seller
    all_values_array=[]
    values_array=[]
    all_values = Value.objects.filter(post = self.id)
    for value in all_values:
        all_values_array.append(value)
        values_array.append(value.value)
    attributes_array = []
    for value in all_values_array:
        attribute  = value.attribute
        attributes_array.append(attribute.name)
    subchannel_of_post = self.subchannel
    channel_of_post = subchannel_of_post.channel
    users_subscribed_to_channel = UserChannelSubscription.objects.filter(channel=channel_of_post)
    users_subscribed_to_channel_array = []
    for i in users_subscribed_to_channel:
        users_subscribed_to_channel_array.append(i.user)
    users_subscribed_to_subchannel = UserSubchannelSubscription.objects.filter(sub_channel=subchannel_of_post)
    users_subscribed_to_subchannel_array = []
    for x in users_subscribed_to_subchannel:
        users_subscribed_to_subchannel_array.append(x.user)
    all_users_subscribed_to_attributes = []
    i = 0
    r = 0
    for z in attributes_array:
        value_in_array = values_array[i]
        attribute = Attribute.objects.get(name = attributes_array[r], subchannel = subchannel_of_post)
        r = r + 1
        try:
            value = AttributeChoice.objects.get(attribute_id = attribute, value = value_in_array)
        except:
            pass
        users_subscribed_to_attribute = UserParameterSubscription.objects.filter(sub_channel=subchannel_of_post, parameter = attribute, choice = value)
        i = i + 1
        for h in users_subscribed_to_attribute:
            all_users_subscribed_to_attributes.append(h.user)
    for q in users_subscribed_to_channel_array:
        not_content = "You have new posts to see in " + unicode(channel_of_post.name)
        not_url = "showpost?post="+unicode(self.id)
        try:
            not1 = Notification(user = q, content = not_content, url=not_url, image_url = self.profile_picture.url)
            not1.save()
            print "yyyyyyyyyyyyy"
            print not1.content
            # Pusher code begin
            # serialized_content = serializers.serialize('json', [ not1.content ])
            # serialized_url = serializers.serialize('json', [ not1.url ])
            push['notification'].trigger('interested_notification', {'user_id': q.id,
            'not_content': serialized_content, 'not_url': serialized_url})
            # Pusher code end
        except:
            not1 = Notification(user = q, content = not_content, url=not_url)
            not1.save()
            print "yyyyyyyyyyyyy"
            print not1.content
            # Pusher code begin
            # serialized_content = serializers.serialize('json', [ not_content ])
            # serialized_url = serializers.serialize('json', [ not_url ])
            push['notification'].trigger('interested_notification', {'user_id': q.id,
            'not_content': not_content, 'not_url': not_url})
            # Pusher code end
    for a in users_subscribed_to_subchannel_array:
        not_content = "You have new posts to see in " + unicode(subchannel_of_post.name)
        not_url = "showpost?post="+unicode(self.id)
        try:
            not1 = Notification(user = a, content = not_content, url=not_url, image_url = self.profile_picture.url)
            not1.save()
            # Pusher code begin
            # serialized_content = serializers.serialize('json', [ not_content ])
            # serialized_url = serializers.serialize('json', [ not_url ])
            push['notification'].trigger('interested_notification', {'user_id': q.id,
            'not_content': not_content, 'not_url': not_url})
            # Pusher code end
        except:
            not1 = Notification(user = a, content = not_content, url=not_url)
            not1.save()
            # Pusher code begin
            # serialized_content = serializers.serialize('json', [ not_content ])
            # serialized_url = serializers.serialize('json', [ not_url ])
            push['notification'].trigger('interested_notification', {'user_id': q.id,
            'not_content': not_content, 'not_url': not_url})
            # Pusher code end
    for b in all_users_subscribed_to_attributes:
        if not UserChannelSubscription.objects.filter(user = b, channel = channel_of_post).exists():
            if not UserSubchannelSubscription.objects.filter(user = b, parent_channel = channel_of_post, sub_channel = subchannel_of_post).exists():
                not_content = "You have new posts to see in " + unicode(subchannel_of_post.name) + " from " + unicode(self.seller.name)
                not_url = "showpost?post="+unicode(self.id)
                try:
                    not1 = Notification(user = b, content = not_content, url=not_url, image_url = self.profile_picture.url)
                    not1.save()
                    # Pusher code begin
                    # serialized_content = serializers.serialize('json', [ not_content ])
                    # serialized_url = serializers.serialize('json', [ not_url ])
                    push['notification'].trigger('interested_notification', {'user_id': q.id,
                    'not_content': not_content, 'not_url': not_url})
                    # Pusher code end
                except:
                    not1 = Notification(user = b, content = not_content, url=not_url)
                    not1.save()
                    # Pusher code begin
                    # serialized_content = serializers.serialize('json', [ not_content ])
                    # serialized_url = serializers.serialize('json', [ not_url ])
                    push['notification'].trigger('interested_notification', {'user_id': q.id,
                    'not_content': not_content, 'not_url': not_url})
                    # Pusher code end



#C2-mahmoud ahmed-the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.


def login(request):
    try:
        mail = request.POST['email']
        password = request.POST['password']
    except:
        LoginError = True
        return render_to_response ('login.html',{"LoginError":LoginError},context_instance=RequestContext(request))
    
    authenticated_user = authenticate(mail=mail, password=password)
    
    if authenticated_user is not None:
    
        print authenticated_user.is_active
        if authenticated_user.is_active:
    
            django_login(request, authenticated_user)
    
            return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        LoginError = True
        return render_to_response ('login.html',{"LoginError":LoginError},context_instance=RequestContext(request))
    

def check_Rate_Identify_buyer(request):
    post = Post.objects.get(pk= request.GET['post'])
    user = request.user
    print user.id
    creator = False
    if post.seller == user and post.buyer is None:
         creator = True
    rateSellerButtonFlag = user.can_rate(request.GET['post']) 
    print rateSellerButtonFlag
    d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator,'user':user}
    return d

def add_to_wish_list(request):
    user = request.user
    post = request.POST['post']
    can_wish = user.add_to_wish_list(post)
    post_obj = Post.objects.get(id = post)
    if can_wish:
        WishList.objects.create(user = user, post_id = post)
        #c2-mohamed
        #the next five lines are written to save a tuple in ActivityLog table
        #to save it to make the user retrieve it when he logs into his activity lo
        post_object = Post.objects.get(id=post)
        post_activity_content = "you added " + unicode(post_object.title) + " to your wish list."
        post_activity_url = "showpost?post=" + unicode(post_object.id)
        post_log_type = "wish"
        # post_log_date = datetime.datetime.now()
        log = ActivityLog.objects.create(content = post_activity_content, url = post_activity_url, log_type = post_log_type, user = user, activity_date = datetime.now())
        not_content = unicode(user.name) + " has added your post to his wish list."
        wish_notification(post_obj, not_content)
    return HttpResponse()

#c2-mohamed
#this def sends notification
#to the user who owns the post that the other user has added to his wish list
def wish_notification(post_in, content):
    post_owner = post_in.seller
    not_content = content
    not_url = "showpost?post=" + unicode(post_in.id)
    try:
        not1 = Notification(user = post_owner, content = not_content, url=not_url, image_url = self.photo.url, not_date=datetime.now())
        not1.save()
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end
    except:
        not1 = Notification(user = user_in, content = not_content, url=not_url, not_date=datetime.now())
        not1.save()
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end
#c1_abdelrahman this method takes the user as an input and it gets the post.
#from the the main page the post object object is extracted from the post table.
#list of attributes are extracted and also list_of_values of the attributes are given.
#it returns the post, list_of_attributes and list_of values of the attributes.

def view_post(request):
    user = request.user
    print "i am form 1yyyyyy"
    form1 = sms_verify(request)
    print "after"
    post_id = request.GET['post']
    post = Post.objects.get(id=post_id)
    post_can_be_wished = False
    is_intrested_inpost = False
    if user.is_authenticated():
        post_can_be_wished = user.add_to_wish_list(post_id)
        is_intrested_inpost=InterestedIn.objects.filter(user_id_buyer = user, post = post).exists()
        title = user.name 
    else:
        title = "welcome guest"
    test_post = Post.objects.get(id = post_id)
    test_post.post_state
    can_edit = False
    if test_post.seller == user:
        can_edit = True
    admin = False
    if user.is_authenticated():
        admin = user.is_admin
    subchannel1 = test_post.subchannel_id
    list_of_att_name = Attribute.objects.filter(subchannel_id = subchannel1)
    list_of_att_values = Value.objects.filter(post = test_post).order_by('attribute')
    list_of_attribute_values = Value.objects.filter(post = test_post).order_by('attribute')
    print list_of_attribute_values.count()
    list_of_att_number = Attribute.objects.filter(subchannel_id = subchannel1)

    #C1-Tharwat--- Calls the getInterestedIn method in order to render the list of interested buyers to the users
    #if the user is a guest it will render an empty list
    list_of_interested_buyers=[]
    if user.id is not None:
        list_of_interested_buyers = user.get_interested_in(post_id)
    #C1-Tharwat--- Calls all the report reasons from the models to show to the user when he wishes to report a post!!!
    report_reasons = ReportReasons.objects.all()
    #c1 abdelrahman returning boolean to the html to know whether the user is admin or not.
    print "is_intrested"
    # print InterestedIn.objects.filter(user_id_buyer = user, post = post).exists() 
    print user
    print post
    dic = {
    'admin': admin
    ,'no': list_of_att_number
    # 'admin': user.is_admin
    , 'can_edit': can_edit
    , 'canwish':post_can_be_wished
    , 'post': test_post
    , 'list_of_attribute_name': list_of_att_name
    , 'list_of_attribute_values': list_of_attribute_values
    , 'report_reasons': report_reasons
    , 'list_of_interested_buyers': list_of_interested_buyers
    , 'comments': Comment.objects.filter(post_id=post_id)
    , 'user_is_intrested': is_intrested_inpost 
    , 'title':title
    , 'post_id': post_id }

    if user.id is not None:
        d = check_Rate_Identify_buyer(request)
        dic.update(d)   
    return render(request, 'ViewPost.html',dic,context_instance=RequestContext(request))




#C2-mahmoud ahmed-As a user i can rate the buyer whom i bought from- User_ratings function takes request 
#as input and imbeded in this request is the session user which is the rater, post_owner which is the user 
#who posted the post, the post it self and the rating. after taking in the request and storing the attributes
#a method is then sent to calculate the rating of the post owner and this method is calculate_rating and
#after the rating is calculated the returned average rating is passed through the dictionary along with the 
#the post_owner object to the profile page to be used to show the rating.
#

def User_Ratings(request):
    rater = request.user
    post_owner = UserProfile.objects.get(id=request.GET['post_owner'])
    post = Post.objects.get(id=request.GET['post_id'])
    rating = request.GET['rating']
    user_rating = post_owner.calculate_rating(rating, post, rater)
    return HttpResponseRedirect("/")
    
#C2-mahmoud ahmed- As the post owner i can identify whom i sold my product to- what this function take 
#as input is a request coming from the user after he presses on add the buyer button in the post page.
#so what the method does is it checks if the request is post and is holding the filled form, if it does
#the GetBuyerNum() method is called to get the number of the buyer and store it in a variable. then the
#user adds the buyer through add_Buyer function whihc takes the post and the buyer phone number as inputs.
#and then you are redirected to the same page. another scenario if the data isn't valid it send the form 
#again through the dictonairy to be displayed again. third scenario is if there is no POST method coming
#through the request then it makes the form and send it through a dictionairy to be viewed through the 
#template.


def Buyer_identification(request):
    user = request.user
    if request.method == 'POST':
        form = BuyerIdentificationForm( request.POST )
        if form.is_valid():
            new_buyer_num = request.POST['buyer_phone_num']
            post = Post.objects.get(id=request.GET['post_id'])
            buyer_added = user.add_buyer(post, new_buyer_num)
            
            if buyer_added == False :
                form = BuyerIdentificationForm()
                d = {'form':form}
                return render_to_response( "add_buyer.html", d,context_instance = RequestContext( request ))
            
            d = {'form':form}
            return render_to_response( "ViewPost.html", d, context_instance = RequestContext( request ))
        else :
            d = {'form':form}
            return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

    else:
        form = BuyerIdentificationForm()
        d = {'form':form}
    return render_to_response( "add_buyer.html", d,context_instance = RequestContext( request ))

# C1_Tharwat - this method will takes in a request as a parameter and acceses the user id from it. it then filters the posts
# according to whether the user is subscribed to them through the channel, subchannel, or a certain parameters(s).
# it then returns to the myfeed.html the list of posts to the user
def viewMyFeed(request):
    user_id = request.user.id
    subscribed_posts = filter_subscribed_to_posts(user_id)
    return render(request, 'myfeed.html', {'subscribed_posts' : subscribed_posts})

# C1_Tharwat - A helper method that will be used viewMyFeed method 
# this method will do the filtering process for the user depending on his subscriptions and will return a list of posts
def filter_subscribed_to_posts(user_id):
    all_channels_subscribed = UserChannelSubscription.objects.filter(user = user_id)
    sub_channels_subscribed = UserSubchannelSubscription.objects.filter(user = user_id)
    parameters_subscribed = UserParameterSubscription.objects.filter(user = user_id)
    all_channels_subscribed_posts = []
    all_subchannels_subscribed_posts = []
    all_parameter_subscribed_posts = []
    all_posts = Post.objects.all()
    for channel in all_channels_subscribed:
        for post2 in all_posts:
            if post2.subchannel.channel == channel.channel:
                all_channels_subscribed_posts.append(post2)
    # for postsubchannel in all_posts:
    for subchannel in sub_channels_subscribed:
        for postsubchannel2 in all_posts:
            if postsubchannel2.subchannel == subchannel.sub_channel:
                all_subchannels_subscribed_posts.append(postsubchannel2)
    # for postparameter in all_posts:
    for parameter in parameters_subscribed:
        for post3 in all_posts:
            all_attributes_in_subchannel = Value.objects.filter(value = parameter.choice.value)
            for chh in all_attributes_in_subchannel:
                if chh.attribute.subchannel == post3.subchannel:
                    continue
                else:
                    chh.delete()
            for attribute_in_subchannel in all_attributes_in_subchannel:
                post_to_add = attribute_in_subchannel.post
                all_parameter_subscribed_posts.append(post_to_add)
                for post in all_subchannels_subscribed_posts:
                    all_values_with_same_post = Value.objects.filter(post = post)
                    for value in all_values_with_same_post:
                        if attribute_in_subchannel.attribute is value.attribute:
                            all_subchannels_subscribed_posts.remove(post)
                for post4 in all_channels_subscribed_posts:
                    all_values_with_same_post = Value.objects.filter(post = post4)
                    for value in all_values_with_same_post:
                        if attribute_in_subchannel.attribute is value.attribute:
                            all_subchannels_subscribed_posts.remove(post4)
    
    final_list = []
    
    for post5 in all_channels_subscribed_posts:
        final_list.append(post5)
    for post6 in all_subchannels_subscribed_posts:
        if post6 not in final_list:
            final_list.append(post6)
    for post7 in all_parameter_subscribed_posts:
        if post7 not in final_list:
            final_list.append(post7)
    return final_list
    
'''Beshoy - C1 Calculate Quality Index this method takes a Request , and then calles a Sort post Function,which makes some 
filtes to the posts then sort them according to quality index AND  render the list to index.html'''
def main(request):
    user = request.user
    user_can_post = False
    title = "Homepage"
    #c1_abdelrahman check whether the user can post or not.
    if user.is_authenticated():
        user_can_post = user.can_post()
    post_list = filter_home_posts()
    #C1-Tharwat --- this will loop on all the posts that will be in the list and call the post_state method in order to check their states
    for i in post_list:
        i.post_state()
    channels = Channel.objects.all()
    channels_list = [] 
    for channel in channels:
        subchannels = SubChannel.objects.filter(channel_id=channel.id)
        subchannels_list = []
        for subchannel in subchannels:
            subchannels_list.append({'subchannel': subchannel})
        channels_list.append({'channel': channel, 'subchannels_list': subchannels_list})
    post_list = Post.objects.all()   
    states=[]
    
    list_of_prices=[]
    all_posts=Post.objects.all()
    for post in all_posts:
        if post.state not in states: 
            states.append(post.state) 
        list_of_prices.append(post.price)
    print states
    if list_of_prices:
      price_min=min(list_of_prices)
      price_max =max(list_of_prices)
# Reem- As  c3 , (a system) I should be able to provide  a refinement bar along while previwing the posts  
# - this method creats variable channels , to store all channels available in the database, 
# variable subchannels , to store all subchannels available in the database,
#  channels_list is a list that holds dictionaries of channels and its subchannels.
# subchannels_list is a list that holds dictionaries os subchannels and its attributes, 
# the method then return the channels_list , as it holds every subchannel of a channel and the posts related to it 
# it also returns the mnimum and maximum price available 

    post_list=filter_posts(post_list) # to filter out (hidden and expired and sold posts) and sort by q-index
    return render_to_response('main.html',{'post_list': post_list , 'all_channels': channels_list ,'title':title, 'canpost': user_can_post , 'states': states},context_instance=RequestContext(request))  




'''Beshoy - C1 Calculate Quality filter home post this method takes no arguments  , and then perform some filtes on the all posts 
 execlude (sold , expired , hidden and quality index <50)Posts then sort them according to quality index AND  return a list of a filtered ordered posts'''
def filter_home_posts():
    post_list = (Post.objects.exclude(is_hidden=True)
        .exclude(expired=True)
        .exclude(is_sold=True)
        .exclude(quality_index__lt=50)
        .order_by('-quality_index'))
    return post_list

def filter_posts(post_list):
    print post_list
    post_filtered = (post_list.exclude(is_hidden=True)
        .exclude(expired=True)
        .exclude(is_sold=True)
        .order_by('-quality_index'))
    return post_filtered






def  get_user(self):    
    User = get_user_model()
    return User

#mai c2: registration
#this method takes in a post request  
#fills in the form (RegistrationForm) with the post data 
#it then validates the form with is_valid() method to run validation and return a boolean  whether the data was valid, it validates all the fields on the form
#then a user is made with the attibutes of the form (cleaned data) and user is saved 
# a random number is then made and sent to the user 
#sets the varaible creadted with the date of when the key is created 
# then it redirects him to profile page 
#or if there is errors it renders the same page again with the form and the request and a msg that says "please correct the following fields"
#if the user submits the form empty , the method will render the form again to the user with a msg " this field is required"

def UserRegistration(request):
    
    if request.method == 'POST':
       
        form = RegistrationForm(request.POST) 
        if form.is_valid(): 
                print form.cleaned_data['password1']
                user = UserProfile.objects.create_user(name=form.cleaned_data['name'], email = form.cleaned_data['email'], password = form.cleaned_data['password1'])
                 # this creates the user
                user.activation_key = ''.join(random.choice(string.ascii_uppercase + string.digits+ user.email) for x in range(20))
                created = datetime.now()
                user.save()
                title = "email verfication"
                content = "http://127.0.0.1:8000/confirm_email/?vc=" + str(user.activation_key) 
                send_mail(title, content, 'mai.zaied17@gmail.com.', [user.email], fail_silently=False)
                

                return HttpResponseRedirect('/thankyou/')

        else:
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        #add our registration form to context
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))

# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post and the status as a varibale in which the user can update and write what's
# on his mind. Logged in users click profile whenever they want to update their status to be directed to their profile 
# page where it displays their information and status. The user can write a new status in the text field whoch will be
# saved on his account. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page.

# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post holding status as a varibale in which the user can update and share what's
# on his mind. The user can write a new status in the text field which will be
# saved on his profile. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page. output of the method saves the new status in database 
@login_required
def update_status(request):
    user = request.user
    print user
    user.status = request.POST['status']
    print request.POST['status']
    user.save()
    return render(request, 'profile.html', {'user':user})

# Heba - C2 edit_name method - the edit_name method  allows logged in users to edit their 
# name. It takes in a request of type post holding name as a varibale in which the user can edit. The user can write a the name they want in the text field which will be
# saved on his profile. For user or guests who are not logged in or just viewing the profile will not be able to edit
#name and will be redirected to the login page. output of the method saves the new name in database 
@login_required
def edit_info(request):
    user = request.user
    print request.POST
    print request.POST['user_name']
    user.name = request.POST['user_name']
    if request.POST['dateofbirth']:
        user.date_Of_birth = request.POST['dateofbirth']
    user.works_at = request.POST['userwork']
    user.phone_number = request.POST['userphone']
    user.save()
    #c2-mohamed
    #the next lines are written to save a tuple in ActivityLog table
    #to save it to make the user retrieve it when he logs into his activity log
    #post_activity_content is to save the activity log content that will be shown to user
    #post_activity_url is to save the url the user will be directed to upon clicking the activity log
    #post_log_type is the type of the log type the user will choose in the activity log page   
    post_activity_content = "you edited your info ." 
    post_activity_url = "profile/?user_id=" + unicode(user.id)
    post_log_type = "profile"
    # post_log_date = datetime.datetime.now()
    log = ActivityLog.objects.create(content = post_activity_content, url = post_activity_url, log_type = post_log_type,user = user, activity_date = datetime.now())
    return HttpResponse (" ")



@login_required
def view_private(request):
    return render_to_response ('private.html', context_instance=RequestContext(request))

@login_required
def editing_pic(request):
    if request.method == 'POST': #if the form has been submitted
        editing_form = EditPicForm(request.POST, request.FILES)#a form bound to the POST data
        if editing_form.is_valid():#all validation rules pass
            success = True
            photo          = editing_form.cleaned_data['photo']
            
    else:
        editing_form =EditPicForm()#an unbound form

        
    ctx = {'editing_form': editing_form}
    return render_to_response('editing_pic.html', ctx, context_instance=RequestContext(request))



def return_account_type(request):
     return render_to_response ('account.html',context_instance=RequestContext(request))

# Heba - C2 change_faccounttype method - as a user i should be able to change my account type from premium to 
# free. The it allows logged in users to be able to change the account type through
# taking a request of type post holding a value for the account type, it takes this value and saves it in the
# users account_type value. the output of the method saves the new value for the account_type in the database.
def change_faccounttype(request):
    print"tessstttiinnggggg"
    user = request.user
    if request.POST['Type'] == 'false':
        user.is_premium = False
    else:
        user.is_premium = True
    user.save()
    return HttpResponse(" ")

#c1 abdelrahman this is a function that takes a request and from the request it gets the post that need to be hidden.
#then it hide it and return empty httpresponse.
def hide_post(request):
    post_id = request.POST['post']
    current_post = Post.objects.get(id = post_id)
    current_post.is_hidden = True
    current_post.save()
    return HttpResponse()

# Heba -C2 private_number method. is a method that allows the users to hide his number through taking a request 
# of type POST holding a value for private_number to be set to true and sets the phone_number of the user to a 
# string that says it is hidden.
def private_number(request):
    print"tessstttiinnggggg"
    user = request.user
    user.private_number = request.POST['Number']
    user.phone_number2 = user.phone_number
    user.phone_number = "The user has set this field to hidden"
    user.save()
    return HttpResponse(" ")

# Heba -C2 public_number method. is a method that allows the users to show his number through taking a request 
# of type POST holding a value for private_number to be set to false and sets the phone_number of the user to his
# actual number is the database.
def public_number(request):
    print"puwwwwwwwwww"
    user = request.user
    print user.phone_number
    user.private_number = request.POST['Number1']
    print request.POST['Number1']
    print user.private_number
    user.private_number = False
    print user.private_number
    user.phone_number = user.phone_number2
    user.save()
    print user.private_number
    return HttpResponse(" ")

# Heba -C2 public_work method. is a method that allows the users to show his work through taking a request 
# of type POST holding a value for private_work to be set to false and sets the works_at of the user to his
# actual work is the database.
def public_work(request):
    print"puwwwwwwwwww"
    user = request.user
    user.private_work = request.POST['Work1']
    print request.POST['Work1']
    print user.private_work
    user.private_work = False
    print user.private_work
    user.works_at = user.works_at2
    user.save()
    print user.private_work
    return HttpResponse(" ")

# Heba -C2 private_work method. is a method that allows the users to hide his works_at through taking a request 
# of type POST holding a value for private_work to be set to true and sets the works_at of the user to a 
# string that says it is hidden.
def private_work(request):
    print"tessstttiinnggggg"
    user = request.user
    user.private_work = request.POST['Work']
    user.works_at2 =user.works_at
    user.works_at= "The user has set this field to hidden"
    user.save()
    return HttpResponse(" ")
    
# Heba - C2 change_paccounttype method - as a user i should be able to change my account type from free to 
# premium. The it allows logged in users to be able to change the account type through
# taking a request of type post holding a value for the account type, it takes this value and saves it in the
# users account_type value. the output of the method saves the new value for the account_type in the database.
def change_paccounttype(request):
    print"tesssffffffff"
    user = request.user
    user.is_premium = request.POST['Type']
    user.save()
    return HttpResponse (" ")



# Reem- As  c3 , (a system) I should be able to provide  a refinement bar along while previwing the posts  
# the method GETS  a list of subchannel ID's , list of post states and a min price and a maximum price 
#  list of ID's is used to get subchannels ( results_of_subchannels ) and hence it retrives posts in post_list
# contributing in post lists , the list_of_states is matched with the post states and filtered 
# also the mnimum and maximum price are considered in order to filter prices within them .
def view_checked_subchannel_posts(request):
    list_of_subchannelsID = request.GET.getlist('list[]')
    list_of_states = request.GET.getlist('status[]')
    results_of_subchannels = []
    for li in list_of_subchannelsID:
        if li is not None:
            results_of_subchannels.append(SubChannel.objects.get(id = li))
   
    post_list_refined =[]
    
    for sub in results_of_subchannels:
        for state in list_of_states:
            post_list_refined.append(Post.objects.filter(subchannel = sub , state=state ))
    post_list = [val for sub1 in post_list_refined for val in sub1]
    print post_list
    return render(request, "filterPosts.html", {'post_list': post_list})
    

#Reem- As c3 I should prvide a vertical refinement bar ( Menu) , wlong with reviweing posts
# subchannel_id is the subchannel checked  
#the subchannel object (results_of_subchannels) related to the ID are retrieved and then the posts related are returned(post_list) 
def menuForSubchannels(request):
    subchannel_id = request.GET["sub_ch_id"]
    print subchannel_id
    current_subchannel = SubChannel.objects.get(id =subchannel_id)
    posts_of_subchannels = Post.objects.filter(subchannel_id= current_subchannel)
    print posts_of_subchannels
    return render(request, "filterPosts.html", {'post_list': posts_of_subchannels})




#C1-Tharwat) This method directs the user to the report page to select a reason for reporting a post
def goToTheReportPage(request):
    return render_to_response('report.html')

#C1-Tharwat) This method takes the user input(reason) for reporting a post and calls the reportPost method in models.py
#reportPost in models.py then takes action to finish the reporting proccess
def reportThePost(request):
    return HttpResponse("hello")

#C1-Tharwat) This method takes the user input(reason) for reporting a post and calls the reportPost method in models.py
#reportPost in models.py then takes action to finish the reporting proccess
def report_the_post(request):
    user = request.user
    post_id = request.POST['post_id']
    report_reason = request.POST['report_reason']
    reported_post = Post.objects.get(id = post_id)
    user.report_the_post(reported_post, report_reason)
    return HttpResponse()


def view_profile(request):
    try: 
        user = request.user
        user_owner = request.GET['user_id']
        #c1-abdelrahman this line retrieves the wished posts by the user.
        list_of_wished_posts = WishList.objects.filter(user_id = user_owner)
        verfied = user.is_verfied
        link = "http://127.0.0.1:8000/confirm_email/?vc=" + str(user.activation_key)
        user_profile = UserProfile.objects.get(id=request.GET['user_id'])
        interacting_list = user_profile.get_interacting_people()
        can_manage_wish_list = False
        # print user.id
        # print user_profile.id
        if user.id == user_profile.id:
            can_manage_wish_list = True
        print can_manage_wish_list
        # print interacting_list
        #c2-mohamed
        #the next 8 lines is to render maximum of two activities to put them in activity log div in profile.html
        activity_logs_to_render_array = []
        activity_logs_to_render_list = ActivityLog.objects.filter(user = user_owner)
        activity_log_counter = 0
        for activity in activity_logs_to_render_list:
            activity_log_counter = activity_log_counter + 1
            activity_logs_to_render_array.append(activity)
            if activity_log_counter is 2:
                break
        d = {'caneditwishlist': can_manage_wish_list,'list_of_wished_posts': list_of_wished_posts,'user':user_profile, "check_verified" : verfied , "link" : link,"interacting_list": interacting_list, 'activity_logs_to_render_array': activity_logs_to_render_array}

        if user.is_anonymous():
            title = "welcome guest"
            user_profile = UserProfile.objects.get(id=request.GET['user_id'])
            interacting_list = user_profile.get_interacting_people()
            annynmous_verfied = True
            link = "http://127.0.0.1:8000/register"

            d = {"title":title , "user":user_profile,"interacting_list": interacting_list,"check_ann_verified" : annynmous_verfied, "link" : link}
                    

        if user.is_authenticated():
            #c1-abdelrahman this line retrieves the wished posts by the user.
            list_of_wished_posts = WishList.objects.filter(user = user)
            verfied = user.is_verfied
            link = "http://127.0.0.1:8000/confirm_email/?vc=" + str(user.activation_key)
            user_profile = UserProfile.objects.get(id=request.GET['user_id'])
            interacting_list = user_profile.get_interacting_people()
            title = user_profile.name +"'s profile"
            if user.id == user_profile.id:
                can_manage_wish_list = True
        
            #c2-mohamed
            #the next 8 lines is to render maximum of two activities to put them in activity log div in profile.html
            activity_logs_to_render_array = []
            activity_logs_to_render_list = ActivityLog.objects.filter(user = user)
            activity_log_counter = 0
            for activity in activity_logs_to_render_list:
                activity_log_counter = activity_log_counter + 1
                activity_logs_to_render_array.append(activity)
                if activity_log_counter is 2:
                    break

            d = {'caneditwishlist': can_manage_wish_list
            ,'list_of_wished_posts': list_of_wished_posts
            , "title":title
            , 'user':user_profile
            , "check_verified" : verfied 
            , "link" : link
            , "interacting_list": interacting_list
            , 'activity_logs_to_render_array': activity_logs_to_render_array
            , 'my_posts': Post.objects.filter(seller=user_profile) 
            , 'my_intrested_in':InterestedIn.objects.filter(user_id_buyer=user_profile)}

    except: 
        err_msg = 'This user doesn\'t exist'
        return HttpResponse(err_msg) 
    else:
        return render_to_response ('profile.html', d ,context_instance=RequestContext(request))

        # GO TO USER PROFILE

#mai c2 L registeration thank you , it justs renders the html thank u 
def thankyou(request):
    return render_to_response ('thankyou.html',context_instance=RequestContext(request))

#mai c2 : registration
# this method takes a request and checks if the request is a post 
# at the beging the post is still empty so it goes in the else part 
#it saves the GEt request in a variable called v_code
#puts it in the form made (confirmationForm)
#pass this form in a dictionary 
#then renders the html with the form
#goes into the method checks if the post request has the code and saves it in a varable form
#then gets the user with this activitioncode 
#checks if the activeationkey is not emty and not expired 
#sets varable is_verfied = true
#rsaves the user
#if the activiation key is expired , a msg saying sry ur accound is disabled will be shown 
def confirm_email(request):
     
    if request.method == 'POST':
        
        form = request.POST['verify'] 
        if form is not None: 
           
            user = UserProfile.objects.get(activation_key=form)
            if user is not None :
                
                   
                user.is_verfied=True
               
                user.save()
                return HttpResponseRedirect('../main')
                
                

            return render_to_response('confirm_email.html', {'form': form}, context_instance=RequestContext(request))

    else : 
        #add our registration form to context
        v_code=request.GET.get('vc', '');
        form = ConfirmationForm(initial={'verify': v_code })
        context = {'form': form}
        return render_to_response('confirm_email.html', context, context_instance=RequestContext(request))
        



#mai: captcha -registration
#it takes a request 
# saves the form with the request data 
#gets the public key from the settings and saves it in publiic_key
#then renders the html with the form passed in a dic and the script 
# result : captcha shown 

def display_form(request):
    form = RegistrationForm(request.POST)
    # assuming your keys are in settings.py
    public_key = settings.RECAPTCHA_PUBLIC_KEY
    script = displayhtml(public_key=public_key)
    return render_to_response('register.html', {'form':form,'script':script}, context_instance=RequestContext(request))







#mai:captcha 
#takes a request and checks if its a post 
#checks if the submited captcha is correct , if not it sends a msg "sry its worng" and renders the html again with the script and captcha
#if its valid then it process the form normally

def verfiy_captcha(request):
    if request.method == 'POST':
        # Check the captcha
        check_captchaa = captcha.submit(request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'], settings.RECAPTCHA_PRIVATE_KEY, request.META['REMOTE_ADDR'])
        if check_captchaa.is_valid is False:
            # Captcha is wrong show a error ...
            return HttpResponse ("sorry its wrong")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Do form processing here...
           return HttpResponseRedirect('/login/')
    else:
        form = RegistrationForm()
        script = displayhtml(public_key=public_key)
    return render_to_response('register.html', {'form':form,'script':script}, context_instance=RequestContext(request))

    #mohamed hammad C3 
    #this method takes as input channel id and then returns its subchannels
def advanced_view_subchannels(request):
    s_id = request.POST['ad_ch_id']
    subchannels_list = SubChannel.objects.filter(channel_id = s_id)
    return render(request ,'refreshedsubchannels.html', {'subchannels_list': subchannels_list})
    #mohamed hammad C3 
    #this method returns all channels
def advanced_view_channels(request):
    channels_list = Channel.objects.all()
    return render(request,'advancedsearch.html', {'channels_list': channels_list})
    #mohamed hammad
    #C3
    #this method takes as input request channel id and renders this channel to main page
def advanced_render_channels(request):
    if request.GET.get('ad_ch_id' , False):
        channel_id = request.GET['ad_ch_id']
        channel = Channel.objects.get(id = channel_id)
        subchannels_list = SubChannel.objects.filter(channel_id = channel.id)
        print subchannels_list
        return render(request,'main.html', {'channel': channel , 'subchannels_list': subchannels_list})
    else: 
        return HttpResponse("please choose a channel")
    #mohamed hammad
    #C3
    #this method takes as input request subchannel id and renders this subchannel to main page
def advanced_render_subchannels(request):
    
    subchannel_id = request.GET.get('ad_sub_ch_id' , False)
    if subchannel_id != False:
        print subchannel_id
        post_list = Post.objects.filter(subchannel_id = subchannel_id)
        ret_subchannel = SubChannel.objects.get(id = subchannel_id)
        print post_list
        return render(request,'main.html', {'ret_subchannel': ret_subchannel , 'post_list': post_list})
    else:
        return HttpResponse("please choose a subchannel")

#mohamed tarek 
#c3 takes as input the subchannel id sellected then return all attributes of it 
#para
def get_attributes_of_subchannel(request):
    sub_id = request.POST['ad_sub_ch_id']
    list_of_attributes = Attribute.objects.filter(subchannel_id = sub_id)
    # print list_of_attributes

    return render(request, 'refreshedattributes.html', {'list_of_attributes' : list_of_attributes, 'sub_id': sub_id})
def advanced_search(request):#mohamed tarek c3 
                             #this method takes attributes as input and takes values from the user them compares them  
                             #to values to get the value obects containig the attribute ids and value iputed and them 
                             #searches for all the post ids that have all the searched criteria present the returns a list of post ids
    sub_id = request.GET['ad_sub_id']
    print "got subchannel id"
    print sub_id
    attributes = Attribute.objects.filter(subchannel_id = sub_id)
    price_req = request.GET['price']
    try:
        price = int(price_req)
        print price
    except ValueError:
        return HttpResponse("please type a number in the price feild")
    values =[]
    post = []
    value_obj =[]
    for w in attributes:
        name = w.name
        values.append(request.GET[name])
    result_search_obj = []
    flag = False
    result_search = []
    result = []
    post = []
    i = 0
    f = i+1
    null = ""
    if price:
        result_search_obj+=[ (Post.objects.filter(price = price , subchannel_id = sub_id)) ]
        result_search = [[] for o in result_search_obj]
        for aa in range(0,len(result_search_obj[0])):
            result_search[0].append(result_search_obj[0][aa].id)
    for j in range(1,len(values)):
        if values[j] == null:
            pass
        else:
            result_search_obj+=[ (Value.objects.filter(attribute= attributes[j] 
            , value = values[j])) ]
    if not result_search_obj:
        return HttpResponse("please enter something in the search")
    else:    
        for k in range(1,len(result_search_obj)):
            for l in range(0,len(result_search_obj[k])):
                test = result_search_obj[k][l].value
                result_search[k].append(result_search_obj[k][l].post.id)
        tmp=result_search[0]
        if len(result_search) == 1:
            post=result_search[0]
        else:
            for h in range(1,len(result_search)):
                post_temp = ""
                for g in range(0,len(result_search[h])):
                    if not result_search[h]:
                        flag = True
                        pass
                    else:
                        if flag == True:
                            h=h-1
                        loc = tmp[g]
                        tmep =result_search[h]
                        loce = tmep[g]
                        if loc == tmep[g]:
                            flag = True
                            post_temp = tmep[g]
                            post.append(post_temp)
        post_list =[]

        for a_post in post:
            post_list.append(Post.objects.get(id = a_post))
        
        if not post_list:
            return HttpResponse("there is no posts with these values please refine your search.")
        else:
            return render(request,'main.html', {'post_list' : post_list})



# c3_Nadeem Barakat: this method is to split the query entered by the user  where the whole sentence is splitted by spaces into words 
# and the method  get rid of the spaces and groups all the query together
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 


    #That combination aims to search keywords within a model by testing the given search fields.
    #1st loop : loops over the search terms enetered by the user in the query one by one
    #2nd loops is implemented to search for field name in the search fields and check whether it conatins the term (keyword) or not

def get_query(query_string, search_fields):
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields: 
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

    # this search method gets the search word from the user and takes it to search in the database 
    # the method filters the model by the search query and return the filtered list, this method
    # defines 3 new variables called found posts , found users , found channels  which are a list of all 
    #found results from the search process 
    # this method takes the query_string which is the query entered by the user 
    # the _query variable ( searches specific attributes in  each model  ex: post_query : 
    #searches in title and description)
def search(request):
    query_string = ''
    found_posts = None
    found_users= None
    found_channels = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        
        post_query = get_query(query_string, ['title', 'description',])
        user_query =  get_query(query_string, ['name'])
        channel_query =get_query(query_string, ['name'])
        found_posts = Post.objects.filter(post_query).order_by('-pub_date')
        found_users = UserProfile.objects.filter(user_query).order_by('-name')
        found_channels = Channel.objects.filter(channel_query)
          
        return render_to_response('main.html',{ 'query_string': query_string, 'post_list': found_posts, 'found_users': found_users,'found_channels' : found_channels },context_instance=RequestContext(request))
    else:
        return render(request,'main.html', {'post_list' : post_list, 'sorry': sorry})





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
    userobject= request.user #UserProfile.objects.get(user_id=Comment.user_id)
    post = Post.objects.get(pk=post_id)
    post.comments_count +=1
    comment = Comment(content=content, date=datetime.now(), user_id=userobject, post_id=post)
    comment.save()
    datetime2 = json.dumps(datetime.now(), default=date_handler)
    # Pusher code begin
    push['real_time_interaction'].trigger('real_time_comments', {'post_id': post_id,'content': content,
    'datetime': datetime2, 'commentor_id': userobject.id, 'commentor_name': userobject.name, 'post_owner': post.seller.id})
    # Pusher code end
    #c2-mohamed
    #the next lines is to send notification to the post owner
    post_seller = post.seller
    all_commentors_array = []
    all_commentors_lists = Comment.objects.filter(post_id=post).exclude(user_id=request.user)
    sent_to_owner = False
    for commentor in all_commentors_lists:
        if commentor.user_id in all_commentors_array:
            continue
        else:
            all_commentors_array.append(commentor.user_id)
    for commentor_to_send in all_commentors_array:
        if request.user is not commentor_to_send:
            if post.seller is commentor_to_send:
                continue
            else:
                not_content = unicode(userobject.name) + " commented on a post you commented on"
                comment_notification(commentor_to_send, post, not_content)
    if sent_to_owner == False:
        not_content = unicode(userobject.name) + " commented on your post"
        comment_notification(post_seller, post, not_content)
    return HttpResponseRedirect("/showpost?post="+str(post_id))

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

#c2-mohamed
#this def sends notification
#to the user who owns the post that the other user has commented on it
def comment_notification(user, post_in, content):
    user_in = user
    post_owner = post_in.seller
    not_content = content
    not_url = "showpost?post=" + unicode(post_in.id)
    try:
        not1 = Notification(user = user_in, content = not_content, url=not_url, image_url = self.photo.url, not_date=datetime.now())
        not1.save()
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end
    except:
        not1 = Notification(user = user_in, content = not_content, url=not_url, not_date=datetime.now())
        not1.save()
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end

#Beshoy intrested method Takes a request 
#then then check if the user is verified ,
#then input the values in  table [IntrestedIn] and Increment Intrested Counter
@login_required
def intrested(request):
    print "intrested views"
    post_in=request.POST["post_in"]
    post=Post.objects.get(pk=post_in)
    user=request.user
    if  InterestedIn.objects.filter(user_id_buyer = user, post = post_in).exists():
        intrest1=InterestedIn(user_id_buyer =user,user_id_seller =post_in.seller,post=post_in)
        intrest1.save()
        post_in.intersed_count=post_in.intersed_count+1
        post_in.save()
        #c2-mohamed
        #the next five lines are written to save a tuple in ActivityLog table
        #to save it to make the user retrieve it when he logs into his activity log
        #post_activity_content is to save the activity log content that will be shown to user
        #post_activity_url is to save the url the user will be directed to upon clicking the activity log
        #post_log_type is the type of the log type the user will choose in the activity log page
        post_activity_content = "you were interested in " + unicode(post_in.title)
        post_activity_url = "showpost?post=" + unicode(post_in.id)
        post_log_type = "profile"
        # post_log_date = datetime.datetime.now()
        log = ActivityLog.objects.create(content = post_activity_content, url = post_activity_url, log_type = post_log_type, user = user, activity_date = datetime.now())
        post_owner = post.seller
        interested_Notification(post)
    return HttpResponse()

#c2-mohamed
#this def sends notification
#to the user who owns the post that the other user has pushed interested on it
def interested_Notification(post_in):
    user_in = self
    post_owner = post_in.seller
    not_content = unicode(self.name) + " is interested in your post"
    not_url = "showpost?post=" + unicode(post_in.id)
    try:
        not1 = Notification(user = post_owner, content = not_content, url=not_url, image_url = post_in.photo.url, not_date=datetime.datetime.now())
        not1.save()
        # Pusher code begin
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end
    except:
        not1 = Notification(user = post_owner, content = not_content, url=not_url, not_date=datetime.datetime.now())
        not1.save()
        # Pusher code begin
        push['notification'].trigger('interested_notification', {'user_id': user_in.id,
        'not_content': not_content, 'not_url': not_url})
        # Pusher code end

#c2-mohamed
#thismethod renders to Activity.html
#it renders all activity log that belongs to that user
def all_log(request):
    author = request.user
    activities_log = ActivityLog.objects.filter(user = author).order_by('activity_date').reverse()
    return render (request, 'ActivityLog.html', {'activities_log':activities_log})

#c2-mohamed
#this method renders to Activity.html
#it renders all activity log of type post that belongs to that user
def all_log_post(request):
    author = request.user
    activities_log = ActivityLog.objects.filter(log_type="post", user = author).order_by('activity_date').reverse()
    return render (request, 'ActivityLog.html', {'activities_log':activities_log})

#c2-mohamed
#this method renders to Activity.html
#it renders all activity log of type interested that belongs to that user
def all_log_interested(request):
    author = request.user
    activities_log = ActivityLog.objects.filter(log_type="interested", user = author).order_by('activity_date').reverse()
    return render (request, 'ActivityLog.html', {'activities_log':activities_log})

#c2-mohamed
#this method renders to Activity.html
#it renders all activity log of type wish that belongs to that user
def all_log_wish(request):
    author = request.user
    activities_log = ActivityLog.objects.filter(log_type="wish", user = author).order_by('activity_date').reverse()
    return render (request, 'ActivityLog.html', {'activities_log':activities_log})

#c2-mohamed
#this method renders to Activity.html
#it renders all activity log of type profile that belongs to that user
def all_log_profile(request):
    author = request.user
    activities_log = ActivityLog.objects.filter(log_type="profile", user = author).order_by('activity_date').reverse()
    return render (request, 'ActivityLog.html', {'activities_log':activities_log})

#mai c2 : sms verfication 
# this methods taked in the number that u want to send the message to and the body 
# it doesnt return anything, it just sends the msg 
def send_sms(to_number,msg_body):

    account_sid = "AC9ec4b58090b478bc49c58aa6f3644cc7"
    auth_token  = "79ba8ebb0bf8377302f735f853cd7006"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.sms.messages.create(body=msg_body,
        to="+2"+str(to_number),
        from_="+18587369892")
    print message.sid

     

#mai c2 : sms verfication 
#this method takes a request 
# it creates a 5 charcter codde and saves this code to the user belong to the request 
# it takes the phone from the field of pphone number in the templates and saves this phone 
# then calls the mehtod that send the msg which takes thie phone number and the code that was generated 
# returns an emtpy response 
def sms(request):
    
    user = request.user
    
    
    user.sms_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(5))
    user.save()
  
    phone_no = request.POST['phone_number']
    user.phone_number = phone_no
    user.save()
    
    send_sms(phone_no ,user.sms_code)
    return HttpResponse(" ")


#mai : c2 : sms verifcation
#this method takes a request and checks if its a post
# it takes the code from the field in the template 
# then gets the user with that code 
# if the user id if the one who is doing the request 
#then it returns an httprespons with true   

def sms_verify(request):
   
    if request.method == 'POST':
       
        smscode = request.POST['sms_code']

 
        if smscode is not None: 
           
            try:
                user = UserProfile.objects.get(sms_code=smscode)
                if user.id == request.user.id:
                    user.phone_is_verified=True
                    user.save()
                    return HttpResponse('true')
                else:
                    return HttpResponse('false')
                
            except:
                return HttpResponse('false')
            return HttpResponse('correct code')


     

#c1_abdelrahman this method takes request as an input.
#it takes the post id and the user_id from the request.
#it deletes the post from the WishList table.

def remove_post_from_wishlist(request):
    user = request.user
    post = request.POST['post']
    post_in = Post.objects.get(id=post)
    WishList.objects.get(user = user, post_id = post).delete()
    #c2-mohamed
    #the next five lines are written to save a tuple in ActivityLog table
    #to save it to make the user retrieve it when he logs into his activity log
    #post_activity_content is to save the activity log content that will be shown to user
    #post_activity_url is to save the url the user will be directed to upon clicking the activity log
    #post_log_type is the type of the log type the user will choose in the activity log page
    post_in = Post.objects.get(id=post)
    post_activity_content = "you removed " + unicode(post_in.title) + " from your wish list."
    post_activity_url = "showpost?post=" + unicode(post_in.id)
    post_log_type = "wish"
    log = ActivityLog.objects.create(content = post_activity_content, url = post_activity_url, log_type = post_log_type, user = user, activity_date = datetime.now())
    return HttpResponse()

#c1_abdelrahman this method takes request as an input from the user. 
#then it retrieves a list from the table with all the posts wished by this user and deletes all of them.  
def empty_wish_list(request):
    user = request.user
    WishList.objects.filter(user=user).delete()
    return HttpResponse()


#c1_abdelrahman this method takes request as an input then it updates the attribute value by the value extracted from request.post.
def edit_post_attribute(request):
    user = request.user
    post_id = request.POST['post']
    attribute_id = request.POST['attribute']
    value = request.POST['value']
    current_value_instant = Value.objects.get(attribute = attribute_id ,post = post_id)
    current_value_instant.value = value
    current_value_instant.post.edit_date = datetime.now()
    current_value_instant.post.save()
    current_value_instant.save()
    return HttpResponse()
#c1_abdelrahman this method takes request as an input then it returns the post and the list of the attributes of the subchannel that the post belongs to and the list of the values of the attributes that is saved in the Values table.
#it checks whether the current of the user and then it renders to the html the list and whether the user can edit the post or not.
def edit_post(request):
    user = request.user
    post_id = request.GET['post']
    current_post = Post.objects.get(id = post_id)
    subchannel = current_post.subchannel_id
    list_of_attribute_name = Attribute.objects.filter(subchannel_id = subchannel)
    list_of_attribute_values = Value.objects.filter(post = current_post).order_by('attribute')
    list_of_attributes_numbers = Value.objects.filter(post = current_post).order_by('attribute')
    return render_to_response('editPost.html', {'current_post': current_post
    , 'list_of_attribute_name':list_of_attribute_name
    , 'list_of_attribute_values':list_of_attribute_values
    ,'list_of_attributes_numbers': list_of_attributes_numbers})
#c1_abdelrahman this method takes request as an input then it extracts the new description from the POST then it save it in the post table. it returns blank httpresponse. 
def edit_post_description(request):
    user = request.user
    new_description = request.POST['description']
    post_id = request.POST['post']
    current_post = Post.objects.get(id = post_id)
    current_post.description = new_description
    current_post.edit_date = datetime.now()
    current_post.save()
    return HttpResponse()
#c1_abdelrahman this method takes request as an input then it extracts the new price from the POST then it save it in the post table. it returns blank httpresponse.
def edit_post_price(request):
    user = request.user
    new_price = request.POST['price']
    post_id = request.POST['post']
    current_post = Post.objects.get(id = post_id)
    current_post.price = new_price
    current_post.edit_date = datetime.now()
    current_post.save()
    return HttpResponse()
#c1_abdelrahman this method takes request as an input then it extracts the new location from the POST then it save it in the post table. it returns blank httpresponse.
def edit_post_location(request):
    user = request.user
    new_location = request.POST['location']
    post_id = request.POST['post']
    current_post = Post.objects.get(id = post_id)
    current_post.location = new_location
    current_post.edit_date = datetime.now()
    current_post.save()
    return HttpResponse()
#c1_abdelrahman this method takes request as an input then it extracts the new title from the POST then it save it in the post table. it returns blank httpresponse.
def edit_post_title(request):
    user = request.user
    new_title = request.POST['title']
    post_id = request.POST['post']
    print post_id
    current_post = Post.objects.get(id = post_id)
    current_post.title = new_title
    current_post.edit_date = datetime.now()
    current_post.save()
    return HttpResponse()





#c1-abdelrahman it takes a request as an input.
# it returns a list of all the wished posts by the user to the profile.html

def view_posts_wished(request):
    user = request.user
    list_of_wished_posts = WishList.objects.filter(user_id = user)
    return render_to_response('profile.html', {'list_of_wished_posts': list_of_wished_posts})

#c2-mohamed awad
#this def returns unread notifications to base.html
def unread_notifications(request):
    user_in = request.user
    all_unread_notifications = Notification.objects.filter(user = user_in, read = False).order_by('not_date').reverse()
    if all_unread_notifications:
        print "after if"
        for notification in all_unread_notifications:
            print "after for"
            notification.read = True
            notification.save()
        all_unread_notifications.order_by('not_date')
        all_unread_notifications.reverse()
        return render (request, 'base.html', {'all_unread_notifications': all_unread_notifications})
    else:
        all_notifications = Notification.objects.filter(user = user_in).order_by('not_date').order_by('not_date').reverse()
        all_notifications.reverse()
        all_unread_notifications = []
        not_counter = 0
        for notification in all_notifications:
            all_unread_notifications.append(notification)
            not_counter = not_counter + 1
            if not_counter == 5:
                break
        return render (request, 'base.html',{'all_unread_notifications': all_unread_notifications})
