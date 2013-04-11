from django import forms
from tager_www.models import UserProfile
from captcha.fields import ReCaptchaField

#mai c2: as a user i should be able to register 
# this class inheirts the built in forms.ModelForm
#it has 2 field the pass1 and pass2 with their lables and the widget hides the password (***) when specificing its a password input 
#the class meta has the model made which is UserProfile and the fields has the requied fields for creating the user and both are atumativally made in the form 
# the class has 2 method explaing them down 

class RegistrationForm(forms.ModelForm):
    
    password1 = forms.RegexField(label=("Password"),widget=forms.PasswordInput(attrs={'onkeyup': 'passwordStrength(this.value)'}),regex=r'^.*(?=.{6,})(?=.*[a-z])(?=.*[A-Z]).*$')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    captcha = ReCaptchaField(attrs={'theme' : 'blackglass'})


    class Meta:
        model = UserProfile
        fields = ('email', 'name')

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
