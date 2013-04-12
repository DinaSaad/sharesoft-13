from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import RegistrationForm , ConfirmationForm
from tager_www.models import UserProfile 
from django import forms 
import random 
import string
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.core.mail import send_mail 


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







#the login method is a method that allows user to log in it takes in a request
#which is of type post and it has the email and the password attribute which are 
#taken in as variables then they are authinticated and the authinticated user is 
#saved into variable user then there is an condition which check that the user is 
#actually there and if he is an active user then we log him in and render his profile page
#in case he has a disabled account then a message would appear. and if the user doesn't exist
#or information entered is wrong then he is redirected to the login page again.





def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response ('Profile.html',context_instance=RequestContext(request))# Redirect to a success page.
        else:
           return HttpResponse ("sorry your account is disabled") # Return a 'disabled account' error message
    else:
        
       return redirect("/login/")# Return an 'invalid login' error message.



#C2-mahmoud ahmed-this isn't all of view post but this part that i did is concerend with the apperance of the
#the rate the seller button which would appear to the buyer of the post only so what it does is
#it takes object user from the session and checks if this user can rate the post that is imbeded in 
#the request and then add the results in the dictonary.Then render the post html and pass the 
#dictionary.
#



def view_homepage(request):
    user = request.user  #logged in user 
    verfied = user.is_verfied
    d = {"check_verified" : verfied }
    return render_to_response('homepage.html', d, context_instance=RequestContext(request))


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
                
                return HttpResponseRedirect('/profile/')
        else:
                return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
    else:
        ''' user is not submitting the form, show them a blank registration form '''
        form = RegistrationForm()
        context = {'form': form}
        return render_to_response('register.html', context, context_instance=RequestContext(request))




        
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
     
    print "Start Confirm"


    if request.method == 'POST':
        print "the request is POST"  
        form = request.POST['verify'] 
        if form is not None: 
            print "The form is valid" 
            user = UserProfile.objects.get(activation_key=form)
            if user is not None :
                if not user.is_expired():
                    print "activation key is exists" 
                    user.is_verfied=True
                    print user.is_verfied 
                    user.save()
                
                else :  
                    print "key expired"
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
           return HttpResponseRedirect('/profile/')
    else:
        form = RegistrationForm()
        script = displayhtml(public_key=public_key)
    return render_to_response('register.html', {'form':form,'script':script}, context_instance=RequestContext(request))




        

#C1-Tharwat) This method directs the user to the report page to select a reason for reporting a post
def goToTheReportPage(request):
    return render_to_response('report.html')

#C1-Tharwat) This method takes the user input(reason) for reporting a post and calls the reportPost method in models.py
#reportPost in models.py then takes action to finish the reporting proccess
def reportThePost(request):
    return HttpResponse("hello")









    
