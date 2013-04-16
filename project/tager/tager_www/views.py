from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm, BuyerIdentificationForm
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
            print "user logged in"
            return HttpResponseRedirect("/profile?user_id="+str(authenticated_user.id))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        return render_to_response ('register.html',context_instance=RequestContext(request))
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
    if post.user == user and post.buyer is None:
         creator = True
    rateSellerButtonFlag = user.can_rate(request.GET['post_id']) 
    print rateSellerButtonFlag
    d = {'view_rating':rateSellerButtonFlag, 'add_buyer_button': creator, 'post':post,'user':user}
    
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
    # print request.POST
    if request.method == 'POST':
        # print request.POST
        form = BuyerIdentificationForm( request.POST )
        if form.is_valid():
            new_buyer_num = request.POST['buyer_phone_num']
            post = Post.objects.get(id=request.GET['post_id'])
            # new_buyer_num = form.GetBuyerNum()
            buyer_added = user.add_Buyer(post, new_buyer_num)
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




def  get_user(self):    
    User = get_user_model()
    return User



def UserRegistration(request):
     #if the user is already logged in , registered , go to profile 
    #if request.user.is_authenticated():
     #   return HttpResponseRedirect('/profile/')
     #if they r submitting the form back
    print request.POST
    if request.method == 'POST':
        print request.POST
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


def view_channels(request):
    list_of_channels = Channel.objects.all()    
    return render(request, 'index.html', {'list_of_channels': list_of_channels})

def view_subchannels(request):
    s_id = request.GET['ch_id']
    current_channel = Channel.objects.filter(pk=s_id)
    list_of_subchannels = Subchannel.objects.filter(channel_id = current_channel)
    return render(request, 'index.html', {'list_of_subchannels': list_of_subchannels})







    
