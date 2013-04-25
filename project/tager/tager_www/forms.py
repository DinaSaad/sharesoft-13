from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.utils.datastructures import SortedDict
from tager_www.models import UserProfile
from captcha.fields import ReCaptchaField

# from parsley.decorators import parsleyfy



from tager_www.models import *


class PostForm(forms.Form):
    # cities = Location.objects.filter(country_name="Egypt")
    title = forms.CharField(max_length="30")
    description = forms.CharField(max_length = "200")
    price = forms.IntegerField()
    location = forms.CharField(max_length = 25, required = False)
    picture = forms.ImageField(required = False)
    picture1 = forms.ImageField(required = False)
    picture2 = forms.ImageField(required = False)
    picture3 = forms.ImageField(required = False)
    picture4 = forms.ImageField(required = False)
    picture5 = forms.ImageField(required = False)



#mahmoud ahmed-C2 user can identify the buyer of his post- the BuyerIdentificationForm what it does is 
#it takes the phone number of the buyer of the post which is provided and submitted buy the issuer of the post.

class BuyerIdentificationForm(forms.Form):
    buyer_phone_num = forms.CharField(max_length=12)
    
    #mahmoud ahmed- C2 user can identify the buyer of his post- it returns the buyer phone number.
    def GetBuyerNum(self):
        
        #buyer_number = self.cleaned_data["buyer_phone_num"]
        return self.buyer_phone_num
           
#mai c2: as a user i should be able to register 
# this class inheirts the built in forms.ModelForm
#it has 2 field the pass1 and pass2 with their lables and the widget hides the password (***) when specificing its a password input 
#the class meta has the model made which is UserProfile and the fields has the requied fields for creating the user and both are atumativally made in the form 
# the class has 2 method explaing them down 

class RegistrationForm(forms.ModelForm):
    
    password1 = forms.RegexField(label=("Password"),widget=forms.PasswordInput(attrs={'placeholder': 'password ','onkeyup': 'passwordStrength(this.value)'}),regex=r'^.*(?=.{6,})(?=.*[a-z])(?=.*[A-Z]).*$')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'placeholder': 'confirm password '}))
    captcha = ReCaptchaField(attrs={'theme' : 'white'})


    class Meta:
        model = UserProfile
        fields = ('name' , 'email')
        widgets = {
            'email': forms.TextInput(attrs = {'placeholder': 'email'}),
            'name' : forms.TextInput(attrs = {'placeholder': 'name'}),
        }
#mai c2:registeration
#this methods doesnt take any paramters and is useed for validating the password
#it gets pass1 and pass2 and compares to see if they match or not if they dont an error msg shows saying passwords dont match
#otherwise it just returns the password2
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
#mai c2:registeration
# this method is used to save the password as hashed format for safty (in the db it wont be stored as the password u enterted but hashed )
#it taked commit as a paramter and its set true 
#This save() method accepts an optional commit keyword argument, which accepts either True or False. 
#This is useful if you want to do custom processing on the object before saving it, or if you want to use one of the specialized model saving options. commit is True by default.
#after it saved the hashed password to the user and returns the user 
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#mai c2: registration 
#this class inherits a built in form called forms.form
#it has only one filed verify 
#this is for the verication of email 
class ConfirmationForm(forms.Form):
    verify = forms.CharField(label='verify')


class PasswordResetForm(forms.Form):
    # error_messages = {
    #     'unknown': _("That email address doesn't have an associated user account. Are you sure you've registered?"),
    #     'unusable': _("The user account associated with this email address cannot reset the password."),
    # }label=_("Email"), max_length=254
    email = forms.EmailField()

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown'])
        if any((user.password == UNUSABLE_PASSWORD)
               for user in self.users_cache):
            raise forms.ValidationError(self.error_messages['unusable'])
        return email

    def save(self, domain_override=None,
             subject_template_name='password_reset_subject.txt',
             email_template_name='password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.pk),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set his/her password without entering the
    old password
    """
    # error_messages = {
    #     'password_mismatch': _("The two password fields didn't match."),
    # }
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change his/her password by entering
    their old password.
    """
    # error_messages = dict(SetPasswordForm.error_messages, **{
    #     'password_incorrect': _("Your old password was entered incorrectly. "
    #                             "Please enter it again."),
    # })
    old_password = forms.CharField()

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'])
        return old_password

PasswordChangeForm.base_fields = SortedDict([
    (k, PasswordChangeForm.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
])
    verify = forms.CharField(label='verify',widget = forms.TextInput(attrs={'readonly': 'readonly '}))

