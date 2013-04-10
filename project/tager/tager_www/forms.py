from django import forms

from tager_www.models import *

#c1_abdelrahman a form to add the basic attributes of the post
class PostForm(forms.Form):
    title = forms.CharField(max_length="30")
    description = forms.CharField(max_length="30")
    price = forms.IntegerField()
    picture = forms.ImageField()
    picture1 = forms.ImageField()
    picture2 = forms.ImageField()
    picture3 = forms.ImageField()
    picture4 = forms.ImageField()
    picture5 = forms.ImageField()


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
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

#this methods doesnt take any paramters and is useed for validating the password
#it gets pass1 and pass2 and compares to see if they match or not if they dont an error msg shows saying passwords dont match
#otherwise it just returns the password2
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

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

