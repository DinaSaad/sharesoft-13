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




def home(request):
    return render_to_response ('home.html',context_instance=RequestContext(request))

def view_login(request):
    return render_to_response ('login.html',context_instance=RequestContext(request))

#C2-mahmoud ahmed-the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.



def view_channels(request):
    list_of_channels = Channel.objects.all()    
    return render(request, 'addPost.html', {'list_of_channels': list_of_channels})

def view_subchannels(request):
    sub_channel_id = request.GET['ch_id']
    current_channel = Channel.objects.filter(pk=sub_channel_id)
    list_of_subchannels = SubChannel.objects.filter(channel_id = current_channel)
    return render(request, 'addPost.html', {'list_of_subchannels': list_of_subchannels})

@login_required
def add_post(request):
    sub_channel_id = request.GET['sub_ch_id']
    # location = request.GET['location_id']
    current_sub_channel = SubChannel.objects.get(id = sub_channel_id)
    list_of_attributes = Attribute.objects.filter(subchannel_id=current_sub_channel)

    form = PostForm(request.POST,request.FILES)
    if form.is_valid():
        author = request.user
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
                Value.objects.create(attribute_id_id=k[7:], value= request.POST[k], Post_id_id = p.id)    
        return HttpResponse('Thank you for adding the post')
    else:

        form = PostForm()
        initial={'subject': 'I love your site!'}
    

    return render_to_response('addPost.html', {'form': form, 'add_post': True, 'list_of_attributes': list_of_attributes})

# def view_location(request):
    
#     return render_to_response('addPost.html', {)




# def login(request):
#     #print request
#     #print "ldnfldnfndlfd"
#     #print request.method
#     mail = request.POST['email']
#     password = request.POST['password']
#     # print "before"
#     # user = UserProfile.objects.get(email=mail)
#     # print user.username
#     # pk = user.username
#     authenticated_user = authenticate(mail=mail, password=password)
#     if authenticated_user is not None:
#         print "auth"
#         print authenticated_user.is_active
#         if authenticated_user.is_active:
#             print "act"
#             django_login(request, authenticated_user)
#             print "user logged in"
#             return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))# Redirect to a success page.
#         else:
#            return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
#     else:
#         return render_to_response ('home.html',context_instance=RequestContext(request))
#        #return redirect("/login/")# Return an 'invalid login' error message.

def login(request):
    mail = request.POST['email']
    password = request.POST['password']

    authenticated_user = authenticate(mail=mail, password=password)
    if authenticated_user is not None:
        print "auth"
        print authenticated_user.is_active
        if authenticated_user.is_active:
            print "act"
            django_login(request, authenticated_user)
            print "user logged in"
            return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))# Redirect to a success page.
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

    post = Post.objects.get(pk= request.GET['post_id'])
    user = request.user
    print user.id
    creator = False
    if post.seller == user and post.buyer is None:
         creator = True
    rateSellerButtonFlag = user.can_rate(request.GET['post_id']) 
    print rateSellerButtonFlag
    d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator, 'post':post,'user':user}
    
    # if request.method == 'POST':
    #     form = BuyerIdentificationForm( request.POST )
    #     if form.is_valid():
    #         new_buyer_num = form.GetBuyerNum()
    #         buyer_added = user.add_Buyer(post, new_buyer_num)
    #         return HttpResponseRedirect( "/" )
    #     else :
    #         d.update({'form':form})
    #         return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

    # else:
    #     form = BuyerIdentificationForm()
    #     d.update({'form':form})
    return render_to_response( "post.html", d,context_instance = RequestContext( request ))

#C2-mahmoud ahmed-As a user i can rate the buyer whom i bought from- User_ratings function takes request 
#as input and imbeded in this request is the session user which is the rater, post_owner which is the user 
#who posted the post, the post it self and the rating. after taking in the request and storing the attributes
#a method is then sent to calculate the rating of the post owner and this method is calculate_rating and
#after the rating is calculated the returned average rating is passed through the dictionary along with the 
#the post_owner object to the profile page to be used to show the rating.
#

def User_Ratings(request):
    # print request
    rater = request.user
    post_owner = UserProfile.objects.get(id=request.GET['post_owner'])
    post = Post.objects.get(id=request.GET['post_id'])
    rating = request.GET['rating']
    user_rating = post_owner.calculate_rating(rating, post, rater)
    # d = {"user_rating":user_rating, 'post_owner':post_owner}
    # return render_to_response( "profile.html", d,context_instance = RequestContext( request ))
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
            # new_buyer_num = form.GetBuyerNum()
            buyer_added = user.add_buyer(post, new_buyer_num)
            d = {'form':form}
            return render_to_response( "post.html", d, context_instance = RequestContext( request ))
            # return HttpResponseRedirect( "/" )
        else :
            d = {'form':form}
            return render_to_response( "add_buyer.html", d, context_instance = RequestContext( request ))

    else:
        form = BuyerIdentificationForm()
        d = {'form':form}
    return render_to_response( "add_buyer.html", d,context_instance = RequestContext( request ))

    
'''Beshoy - C1 Calculate Quality Index this method takes a Request , and then calles a Sort post Function,which makes some 
filtes to the posts then sort them according to quality index AND  render the list to index.html'''
def index(request):
    post_list = filter_home_posts()
    return render_to_response('index.html',{'post_list': post_list},context_instance=RequestContext(request))  

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
    post_filtered = (post_list.objects.exclude(is_hidden=True)
        .exclude(expired=True)
        .exclude(is_sold=True)
        .order_by('-quality_index'))
    return post_filtered




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
            return UserProfile.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None






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


def view_profile(request):
    try: 
        user = request.user
        # print user
        verfied = user.is_verfied
        link = "http://127.0.0.1:8000/confirm_email/?vc=" + str(user.activation_key)
        print "v"
        user_profile = UserProfile.objects.get(id=request.GET['user_id'])
        d = {'user':user_profile, "check_verified" : verfied , "link" : link}
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
                if not user.is_expired():
                   
                    user.is_verfied=True
                   
                    user.save()
                    return HttpResponseRedirect('/main/')
                
                else :  
                 
                    return HttpResponse ("sorry your account is disabled because the activation key has expired")

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


#mai: captcha -registration
#it takes a request 
# saves the form with the request data 
#gets the public key from the settings and saves it in publiic_key
#then renders the html with the form passed in a dic and the script 
# result : captcha shown 



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
    # print request.POST
    s_id = request.POST['ad_ch_id']

    # print s_id
    #current_channel = Channel.objects.filter(channel_id = s_id)
    list_of_subchannels = SubChannel.objects.filter(channel_id = s_id)
    return render(request ,'refreshedsubchannels.html', {'list_of_subchannels': list_of_subchannels})
    #mohamed hammad C3 
    #this method returns all channels

def advanced_view_channels(request):
    list_of_channels = Channel.objects.all() 
    return render(request,'advancedsearch.html', {'list_of_channels': list_of_channels})

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
    for j in range(0,len(values)):
        if values[j] == null:
            pass
        else:
            result_search_obj+=[ (Value.objects.filter(attribute= attributes[j] 
            , value = values[j])) ]
    if not result_search_obj:
        return HttpResponse("please enter something in the search")
    else:
        result_search = [[] for o in result_search_obj]    
        for k in range(0,len(result_search_obj)):
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
            return render('main.html', {'post_list' : post_list})


# def advanced_search_helper(basic_search_list):#mohamed tarek c3 
#                              #this method takes attributes as input and takes values from the user them compares them  
#                              #to values to get the value obects containig the attribute ids and value iputed and them 
#                              #searches for all the post ids that have all the searched criteria present the returns a list of post ids
#     sub_id = request.GET['sub_ch_id']
#     attributes = Attribute.objects.filter(subchannel_id = sub_id)
#     values =[]
#     post = []
#     value_obj =[]
#     for w in attributes:
#         name = w.name
#         values.append(request.GET[name])
#     result_search_obj = []
#     flag = False
#     result_search = []
#     result = []
#     post = []
#     i = 0
#     f = i+1
#     null = ""
#     basic_search_values = []
#     for r in range(0,len(basic_search_list)):
#         basic_search_values = [(Value.objects.filter(post = basic_search_list[r])) ]
#     for j in range(0,len(values)):
#         if values[j] == null:
#             pass
#         else:
#             for e in range(0,len(values)):
#             result_search_obj+=[ (Value.objects.filter(attribute_id = attributes[j].id 
#             , value = values[j])) ]
#     if not result_search_obj:
#         return HttpResponse("please enter something in the search")
#     else:
#         result_search = [[] for o in result_search_obj]    
#         for k in range(0,len(result_search_obj)):
#             for l in range(0,len(result_search_obj[k])):
#                 test = result_search_obj[k][l].value
#                 result_search[k].append(result_search_obj[k][l].post.id)
#         tmp=result_search[0]
#         if len(result_search) == 1:
#             post=result_search[0]
#         else:
#             for h in range(1,len(result_search)):
#                 post_temp = ""
#                 for g in range(0,len(result_search[h])):
#                     if not result_search[h]:
#                         flag = True
#                         pass
#                     else:
#                         if flag == True:
#                             h=h-1
#                         loc = tmp[g]
#                         tmep =result_search[h]
#                         loce = tmep[g]
#                         if loc == tmep[g]:
#                             flag = True
#                             post_temp = tmep[g]
#                             post.append(post_temp)
#         post_obj =[]
#         for a_post in post:
#             post_obj.append(Post.objects.get(id = a_post))
#         if not post_obj:
#             return HttpResponse("there is no posts with these values please refine your search.")

#         else:
#             print post_obj
#             post_list=filter_posts(post_obj)
#             return render('main.html', {'post_list' : post_list})
