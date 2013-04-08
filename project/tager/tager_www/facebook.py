from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.core.urlresolvers import reverse
import urllib
from tager_www.models import *
#import requests
#from django.core.mail import EmailMultiAlternatives
#import random
#import string

APP_ID = '486824131372459'   # facebook app's app id
APP_SECRET = '23ecae8451f3a4b2a005fbd177a809b5'  # facebook app's app secret
LOGIN_REDIRECT_URL = '127.0.0.1:8000'  # The url that the user will be redirected to after logging in with facebook 
FACEBOOK_PERMISSIONS = ['email', 'user_about_me']  # facebook permissions
SCOPE_SEPARATOR = ' '


def facebook_login(request): # creates the connection with facebook and connects with facebook app
	if request.REQUEST.get("device"):
		device = request.REQUEST.get("device")
	else:
		device = "user-agent"
		params = {}
		params["client_id"] = APP_ID
		params["redirect_uri"] = request.build_absolute_uri(reverse("facebook_login_done"))
		params['scope'] = SCOPE_SEPARATOR.join(FACEBOOK_PERMISSIONS)
		params["device"] = device
		url = "https://graph.facebook.com/oauth/authorize?" + urllib.urlencode(params)
		if 'HTTP_REFERER' in request.META:
			request.session['next'] = request.META['HTTP_REFERER']
		return HttpResponseRedirect(url)


def facebook_login_done(request): # logs in the user returened from authenticate
	result = authenticate(request=request)
	
	
	if isinstance(result, AbstractBaseUser):
		
		login(request, result)
		print('inside login_done')
	if 'next' in request.session:
		next = request.session['next']
		del request.session['next']
		return HttpResponseRedirect('index')
	else:
		return HttpResponseRedirect(LOGIN_REDIRECT_URL)



#checks the facebooks authentication and gets the acces token and user information form facebook#then checks if the user is
#already there so it redirects to facebook_login_done or if the user isn't there then it creats the user and retun it to
#facebook_login_done

class FacebookBackend:

	def authenticate(self, request):
		user = None
		access_token = None
		params = {}
		params["client_id"] = APP_ID
		params["client_secret"] = APP_SECRET
		params["redirect_uri"] = request.build_absolute_uri(reverse("facebook_login_done"))
		params["code"] = request.GET.get('code', '')
		url = ("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(params))
		from cgi import parse_qs
		userdata = urllib.urlopen(url).read()
		res_parse_qs = parse_qs(userdata)
		if not ('access_token') in res_parse_qs:
			return None
		access_token = res_parse_qs['access_token'][-1]
		url = "https://graph.facebook.com/me?access_token=" + access_token
		import simplejson as json
		fb_data = json.loads(urllib.urlopen(url).read())
		uid = fb_data['id']
		if not fb_data:
			return None
		try:
		    fb_user = UserProfile.objects.get(email=fb_data.get('email', "") , facebook_uid=uid)
		    print fb_user, 'HELLO'
		    fb_user.accesstoken = access_token
		    fb_user.save()

		    return fb_user
		except UserProfile.DoesNotExist:
		    username = fb_data.get('username')
		    print(username)
			
		if username:
			print('xsgsxh')

			
			userProfile = UserProfile.objects.create(first_name=fb_data['first_name'])
			userProfile.facebook_uid=uid
			userProfile.last_name = fb_data['last_name']
			userProfile.email = fb_data.get('email', None)
			userProfile.accesstoken = access_token
			userProfile.save()
			return userProfile

	def get_user(self, user_id): # returns the user
		try:
			return User.objects.get(pk=user_id)  #^^ return User.objects.get(pk=user_id)
		except:
			return None

	def getContacts(self, request):
		params = {}
		params["client_id"] = APP_ID
		params["client_secret"] = APP_SECRET
		params["redirect_uri"] = request.build_absolute_uri(reverse("facebook_login_done"))
		params["code"] = request.GET.get('code', '')
		url = ("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(params))
		from cgi import parse_qs
		userdata = urllib.urlopen(url).read()
		res_parse_qs = parse_qs(userdata)
		if not ('access_token') in res_parse_qs:
			return None
		access_token = res_parse_qs['access_token'][-1]
		url = "https://graph.facebook.com/me?access_token=" + access_token + "fields=friends"
		import simplejson as json
		fb_data = json.loads(urllib.urlopen(url).read())
		uid = fb_data['id']
		if not fb_data:
			return None
		try:
			friend = UserProfile.objects.get(facebook_uid=uid, fb_data.get('id', "")) #, friend_facebook_id=fb_data.get('id')
	    	print friend
	    	friend.accesstoken = access_token
	    	friend.save()
	    	return friend
