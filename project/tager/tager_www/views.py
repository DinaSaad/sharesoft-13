from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect, HttpResponse
from tager_www.models import *
from django.template import RequestContext
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import get_user_model  
from django.template import RequestContext
from tager_www.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse



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
            return UserProfile.objects.get(pk=user_id)
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



# Heba - C2 profile method - the profile method is a method that allows logged in users to view their 
# profile page. It takes in the reviewer who views the profile page and the user of this profile page varibales.
# it includes the user name, his date of birth, phone number, gender, account type checking if prepium or not and  
#  The logged in users are directed to the profile page whenever he wants to view it by clicking on the profile button
# from above. For the users who are not logged in or does not exist he will be redirected to the login page.
# @login_required
# def Profile(request, user_id):
#     if not request.user.is_authenticated():
#         HttpResponseRedirect('/login/')
#     reviewer = UserProfile.objects.get(id=request.user.id)
#     user = UserProfile.objects.get(id=user_id)
#     ctx = {'user': user}
#    
#     render_to_response('profile.html', ctx, context_instance=RequestContext(RequestContext))


# user.photo.url="/media/images.jpg"
#     user.save()

# Heba - C2 editing_info method - the editing_info method is a method that allows logged in users to edit their 
# information. It takes in a request of type post and varibales that are editable attributes that the user can edit,
# it includes the user name, his date of birth, phone number, gender, account type checking if prepium or not and  
# the photo of the user. The logged in users are directed to the editing page whenever he wants to edit an information
# about himself in which the editing form will be made available for him to write the modified information and saved 
# him on his account. For the users who are not logged in or does not exist he will be redirected to the login page.
@login_required
def editing_info(request):
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

        
    ctx = {'editing_form': editing_form}
    return render_to_response('editing.html', ctx, context_instance=RequestContext(request))



# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post and the status as a varibale in which the user can update and write what's
# on his mind. Logged in users click profile whenever they want to update their status to be directed to their profile 
# page where it displays their information and status. The user can write a new status in the text field whoch will be
# saved on his account. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page.
# @login_required
# def update_status(request):
#     if request.method == 'POST':
#         updating_form = UpdateStatusForm(request.POST)
#         if updating_form.is_valid():
#             tmmp_user = UserProfile.objects.get(pk=request.user.id)
#             status = updating_form.cleaned_data['status']
#             if status != "":
#                 tmmp_user.status = status
#                 tmmp_user.save()



#     else:
#         updating_form = UpdateStatusForm()

#     ctx = {'updating_form': updating_form}
#     return render_to_response('profile.html', ctx, context_instance=RequestContext(request))




    

# Heba - C2 updating status method - the update_Status method is a method that allows logged in users to update their 
# status. It takes in a request of type post and the status as a varibale in which the user can update and write what's
# on his mind. Logged in users click profile whenever they want to update their status to be directed to their profile 
# page where it displays their information and status. The user can write a new status in the text field whoch will be
# saved on his account. For user or guests who are not logged in or just viewing the profile will not be able to update
# the status and will be redirected to the login page.
# @csrf_protect
# def password_reset(request, is_admin_site=False,
                   
#                    email_template_name='password_reset_email.html',
#                    subject_template_name='password_reset_subject.txt',
#                    password_reset_form=PasswordResetForm,
#                    token_generator=default_token_generator,
#                    post_reset_redirect=None,
#                    from_email=None,
#                    ):
#                    #  template_name='registration/password_reset_form.html',
#                    # current_app=None,
#                    # extra_context=None)
#                 # extra_context=no-one
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('tager_www.views.password_reset_done')
#     if request.method == "POST":
#         form = password_reset_form(request.POST)
#         if form.is_valid():
#             opts = {
#                 'use_https': request.is_secure(),
#                 'token_generator': token_generator,
#                 'from_email': from_email,
#                 'email_template_name': email_template_name,
#                 'subject_template_name': subject_template_name,
#                 'request': request,
#             }
#             # if is_admin_site:
#             #     opts = dict(opts, domain_override=request.get_host())
#             # form.save(**opts)
#             send_mail()
#             return HttpResponseRedirect(post_reset_redirect)
#     else:
#         form = password_reset_form()
#     context = {
#         'form': form,
#     }
    
#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)

#     return render_to_response('password_reset_form.html', context, context_instance=RequestContext(request))

# def password_reset_done(request,
#                         template_name='password_reset_done.html',
#                         current_app=None):
# # extra_context=None
#     context = {}
#     # if extra_context is not None:
#     #     context.update(extra_context)
    
#     return render_to_response('password_reset_done.html', context, context_instance=RequestContext(request))


#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)


# # Doesn't need csrf_protect since no-one can guess the URL
# @sensitive_post_parameters()
# @never_cache
# def password_reset_confirm(request, uidb36=None, token=None,
#                            template_name='password_reset_confirm.html',
#                            token_generator=default_token_generator,
#                            set_password_form=SetPasswordForm,
#                            post_reset_redirect=None,
#                            current_app=None):
# # extra_context=None
#     """
#     View that checks the hash in a password reset link and presents a
#     form for entering a new password.
#     """
#     UserModel = get_user_model()
#     assert uidb36 is not None and token is not None  # checked by URLconf
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('tager_www.views.password_reset_complete')
#     try:
#         uid_int = base36_to_int(uidb36)
#         user = UserModel._default_manager.get(pk=uid_int)
#     except (ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None

#     if user is not None and token_generator.check_token(user, token):
#         validlink = True
#         if request.method == 'POST':
#             form = set_password_form(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(post_reset_redirect)
#         else:
#             form = set_password_form(None)
#     else:
#         validlink = False
#         form = None
#     context = {
#         'form': form,
#         'validlink': validlink,
#     }
#     # if extra_context is not None:
#     #     context.update(extra_context)
#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)

#     return render_to_response('password_reset_confirm.html', ctx, context_instance=RequestContext(request))




# def password_reset_complete(request,
#                             template_name='password_reset_complete.html',
#                              current_app=None ):
# # extra_context=None
#     context = {
#         'login_url': resolve_url(settings.LOGIN_URL)
#     }
#     # if extra_context is not None:
#     #     context.update(extra_context)
#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)

#     return render_to_response('password_reset_complete.html', ctx, context_instance=RequestContext(request))



# @sensitive_post_parameters()
# @csrf_protect
# @login_required
# def password_change(request,
#                     template_name='password_change_form.html',
#                     post_change_redirect=None,
#                     password_change_form=PasswordChangeForm,
#                     current_app=None):
#  # extra_context=None
#     if post_change_redirect is None:
#         post_change_redirect = reverse('tager_www.views.password_change_done')
#     if request.method == "POST":
#         form = password_change_form(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(post_change_redirect)
#     else:
#         form = password_change_form(user=request.user)
#     context = {
#         'form': form,
#     }
#     # if extra_context is not None:
#     #     context.update(extra_context)
#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)
#     return render_to_response('password_change_form.html', ctx, context_instance=RequestContext(request))



# @login_required
# def password_change_done(request,
#                          template_name='password_change_done.html',
#                          current_app=None):
# # extra_context=None
#     context = {}
#     # if extra_context is not None:
#     #     context.update(extra_context)
#     # return TemplateResponse(request, template_name, context,
#     #                         current_app=current_app)
#     return render_to_response('password_reset_complete.html', ctx, context_instance=RequestContext(request))








    
