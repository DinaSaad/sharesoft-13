from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from tager_www.forms import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
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
    if post.user == user:
         creator = True
    rateSellerButtonFlag = user.canRate(request.GET['post_id']) 
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
            new_buyer_num = form.GetBuyerNum()
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

# Heba - C2 editing_info method - the editing_info method is a method that allows logged in users to edit their 
# information. It takes in a request of type post and varibales that are editable attributes that the user can edit,
# it includes the user name, his date of birth, phone number, gender, account type checking if prepium or not and  
# the photo of the user. The logged in users are directed to the editing page whenever he wants to edit an information
# about himself in which the editing form will be made available for him to write the modified information and saved 
# him on his account. For the users who are not logged in or does not exist he will be redirected to the login page.
@login_required
def editing_UsersInformation(request):
    if request.method == 'POST': #if the form has been submitted
        editing_form = EditingUserProfileForm(request.POST, request.FILES)#a form bound to the POST data
        if editing_form.is_valid():#all validation rules pass
            # user_id = request.UserProfile.id
            tmp_user = UserProfile.objects.get(pk=request.user.id)
            name          = editing_form.cleaned_data['name']
            date_Of_birth = editing_form.cleaned_data['date_Of_birth']
            phone_number  = editing_form.cleaned_data['phone_number']
            gender        = editing_form.cleaned_data['gender']
            photo         = editing_form.cleaned_data['photo']

            if name != "":
                tmp_user.name = name
                tmp_user.save()
            if date_Of_birth != "":
                tmp_user.date_Of_birth = date_Of_birth
                tmp_user.save()
            if phone_number != "":
                tmp_user.phone_number = phone_number
                tmp_user.save()
            if gender != "":
                tmp_user.gender = gender
                tmp_user.save()
            if photo != "":
                tmp_user.photo = photo
                tmp_user.save()
            # is_premium = editing_form.cleaned_data['is_premium']
            # return HttpResponseRedirect('/Thank/') #redirect after POST
    else:
        editing_form =EditingUserProfileForm()#an unbound form  
    context = {'editing_form': editing_form}
    return render_to_response('editing.html', context, context_instance=RequestContext(request))

# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post and the status as a varibale in which the user can update and write what's
# on his mind. Logged in users click profile whenever they want to update their status to be directed to their profile 
# page where it displays their information and status. The user can write a new status in the text field whoch will be
# saved on his account. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page.
@login_required
def update_status(request):
    if request.method == 'POST':
        updating_form = UpdateStatusForm(request.POST)
        if updating_form.is_valid():
            temporary_user = UserProfile.objects.get(pk=request.user.id)
            status = updating_form.cleaned_data['status']
            if status != "":
                temporary_user.status = status
                temporary_user.save()
    else:
        updating_form = UpdateStatusForm()

    context = {'updating_form': updating_form}
    return render_to_response('profile.html', context, context_instance=RequestContext(request))

# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post and the status as a varibale in which the user can update and write what's
# on his mind. Logged in users click profile whenever they want to update their status to be directed to their profile 
# page where it displays their information and status. The user can write a new status in the text field whoch will be
# saved on his account. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page.
@csrf_protect
def password_reset(request, is_admin_site=False,
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   ):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('tager_www.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            title = "Reseting Your Password. "
            content = " You're receiving this email because you requested a password reset for your user account at Tager.com PLEASE follow the link: http://127.0.0.1:8000/reset/confirm/"
            send_mail(title, content, 'mai.zaied17@gmail.com.', [request.user.email], fail_silently=False)
            # opts = {
            #     'use_https': request.is_secure(),
            #     'token_generator': token_generator,
            #     'from_email': from_email,
            #     'email_template_name': email_template_name,
            #     'subject_template_name': subject_template_name,
            #     'request': request,
            # }
            # if is_admin_site:
            #     opts = dict(opts, domain_override=request.get_host())
            # form.save(**opts)
            # title = "Reseting Your Password. You're receiving this email because you requested a password reset for your user account at Tager.com PLEASE follow the link"
            # content = "http://127.0.0.1:8000/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/"
            # send_mail(title, content, 'mai.zaied17@gmail.com.', [request.user.email], fail_silently=False)
            
# http://127.0.0.1:8000/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+) +str({% url 'tager_www.views.password_reset_confirm' uidb36=uid token=token %})"             
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
    }
    
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)

    return render_to_response('password_reset_form.html', context, context_instance=RequestContext(request))

def password_reset_done(request,
                        template_name='password_reset_done.html',
                        current_app=None):
# extra_context=None
    context = {}
    # if extra_context is not None:
    #     context.update(extra_context)
    
    return render_to_response('password_reset_done.html', context, context_instance=RequestContext(request))


    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb36=None, token=None,
                           template_name='password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None):
# extra_context=None
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb36 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('tager_www.views.password_reset_complete')
    try:
        uid_int = base36_to_int(uidb36)
        user = UserModel._default_manager.get(pk=uid_int)
    except (ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(None)
    else:
        validlink = False
        form = None
    context = {
        'form': form,
        'validlink': validlink,
    }
    # if extra_context is not None:
    #     context.update(extra_context)
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)

    return render_to_response('password_reset_confirm.html', context, context_instance=RequestContext(request))




def password_reset_complete(request,
                            template_name='password_reset_complete.html',
                             current_app=None ):
# extra_context=None
    context = {
        'login_url': resolve_url(settings.LOGIN_URL)
    }
    # if extra_context is not None:
    #     context.update(extra_context)
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)

    return render_to_response('password_reset_complete.html', context, context_instance=RequestContext(request))



@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None):
 # extra_context=None
    if post_change_redirect is None:
        post_change_redirect = reverse('tager_www.views.password_change_done')
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    # if extra_context is not None:
    #     context.update(extra_context)
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)
    return render_to_response('password_change_form.html', context, context_instance=RequestContext(request))



@login_required
def password_change_done(request,
                         template_name='password_change_done.html',
                         current_app=None):
# extra_context=None
    context = {}
    # if extra_context is not None:
    #     context.update(extra_context)
    # return TemplateResponse(request, template_name, context,
    #                         current_app=current_app)
    return render_to_response('password_reset_complete.html', context, context_instance=RequestContext(request))


# Heba - C2 profile method - the profile method is a method that allows logged in users to view their 
# profile page. It takes in the reviewer who views the profile page and the user of this profile page varibales.
# it includes the user name, his date of birth, phone number, gender, account type checking if prepium or not and  
#  The logged in users are directed to the profile page whenever he wants to view it by clicking on the profile button
# from above. For the users who are not logged in or does not exist he will be redirected to the login page.
