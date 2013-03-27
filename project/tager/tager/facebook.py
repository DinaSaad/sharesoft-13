APP_ID = 522495247789011 # From facebook app’s settings
APP_SECRET = 	a7e7b4388ac54d3376c861d8f463ac6a # From facebook app’s settings
	

LOGIN_REDIRECT_URL = http://www.google.com # The url that the user will be redirected toafter logging in with facebook

FACEBOOK_PERMISSIONS = ['email', 'user_about_me'] # facebook permissions
SCOPE_SEPARATOR = ''

def facebook_login(request):
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
	request.session['next'] = request.META['HTTP_REFERER']
	return HttpResponseRedirect(url)

def facebook_login_done(request):
	result = authenticate(request=request)
	login(request, result)
	if 'next' in request.session:
		next = request.session['next']
	return HttpResponseRedirect(LOGIN_REDIRECT_URL)

class FacebookBackend:
	def authenticate(self, request):
		user = None
		access_token = None 
		# assume logging in normal wayparams = {}
		params["client_id"] = APP_ID
		params["client_secret"] = APP_SECRET
		params["redirect_uri"] = request.build_absolute_uri(reverse("facebook_login_done"))
		params["code"] = request.GET.get('code', '')

		url = ("https://graph.facebook.com/oauth/access_token?"
			+ urllib.urlencode(params))
		from cgi import parse_qs
		userdata = urllib.urlopen(url).read()
		res_parse_qs = parse_qs(userdata)
		# Could be a bot query
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
			fb_user = UserProfile.objects.get(facebook_uid=uid, email=fb_data.get('email', None))
			fb_user.accesstoken = access_token
			fb_user.save()
		return fb_user
		except UserProfile.DoesNotExist:
			username = fb_data.get('username')
			if not username:
				username = uid
			userProfile = UserProfile.objects.create(username=username)
			userProfile.first_name = fb_data['first_name']
			userProfile.last_name = fb_data['last_name']
			userProfile.email = fb_data.get('email', None)
			userProfile.save()
			return userProfile

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except:
			return None