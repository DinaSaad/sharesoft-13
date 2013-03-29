from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser

#since userprofile has different than abstractbaseuser attriubtes thats why will define our own custom manager that extends BaseUserManager.
class MyUserManager(BaseUserManager):
    # this will create user when name , email, password is entered 
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
 
        user = self.model(
            email=MyUserManager.normalize_email(email),
            
        )
 
        user.set_password(password)
        user.save(using=self._db)
        return user
     #this creates the admin user 
    def create_superuser(self, email, name , password):
        user = self.create_user(email,
            password=password, name=name
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

     #UserProfile class extends abdstractbaseuser which has core implementation of user model build in    django 
     #this class addes some fields to abstractbaseuser which is inherited 

class UserProfile (AbstractBaseUser):
    name = models.CharField(max_length=40)     
    email = models.EmailField(max_length=254, unique=True)
    facebook_uid = models.IntegerField(unique=True, null=True)
    accesstoken = models.CharField(max_length=50 , null=True , unique=True)
    date_Of_birth = models.DateField(null=True, blank=True)
    is_admin = models.BooleanField(default=False)           
    is_verfied = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='img',blank=True)
    activation_key = models.BooleanField(default=False)
    status = models.CharField(max_length=400 , null=True) 
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
     )
    gender = models.CharField(max_length=1, choices=gender_choices , null=True)
    
    # this tells UserProfile to use the custom manager made 
    objects = MyUserManager()  
    # this is the unique identifier , it can be any unique field
    USERNAME_FIELD = 'email'   
    # the requird fields are the fields which are mandotory , you dont put the USERNAME_fields in it 
    REQUIRED_FIELDS = ['name']  
    
    #these method are in the abstractbaseuser and These methods allow the admin to control access of the User to admin content: 
    is_admin = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin '
                    'site.')    


    is_active = models.BooleanField('active', default=True,    # returns true if the user is still active 
        help_text='Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.')

    def get_full_name(self):
        # return name . Could also be User.first_name User.last_name if you have these fields
        return self.name
 
    def get_short_name(self):
        # return name. Could also be User.first_name if you have this field
        return self.name
 
    def __unicode__(self):
        return self.email
     
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True

    # genrates setters and getters
    @property   
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin


class Channel():


class Subchannel():



class Attribute():


class Post():


class Comments():



class Subscribtion():



class Notification():


class InterestedIn():
	



