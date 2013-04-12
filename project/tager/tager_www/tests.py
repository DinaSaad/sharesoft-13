from django.test import TestCase

from tager_www.models import UserProfile
from tager_www.forms import RegistrationForm
from django.test import Client
from datetime import datetime, timedelta
from django.conf import settings


class UserProfileTest(TestCase):

    def setUp(self):

        self.user1 = UserProfile.objects.create_user(email="mai@gmail.com", name="mai", password="123")
        self.user1.save()
        self.user2 = UserProfile.objects.create_user(email="ayia@gmail.com", name="ayia", password="123",status="testing")
        self.user2.save()
        self.user3 = UserProfile.objects.create_superuser(email="mahmoud@gmail.com", name="mahmoud", password="123")
        self.user3.save()

    def test_UserProfile(self):
        self.assertEqual(self.user1.email , "mai@gmail.com")
        self.assertEqual(self.user2.email , "ayia@gmail.com")
       
        profile1 = UserProfile.objects.get(pk=1)
        self.assertEquals(profile1.name,'mai')
        self.assertEquals(profile1.is_active,True)

        
        profile2 = UserProfile.objects.get(pk=3)
        self.assertFalse(profile2.status ,"testing")
    
        profile3 = UserProfile.objects.get(pk=3)
        self.assertEquals(profile3.is_admin,True)

        profile3.name = "mahmoud1"
        profile3.save()
        UserProfile.objects.get(pk=3)
        self.assertEquals(profile3.name,"mahmoud1")


        

    

    
    




# class MyViewTests(TestCase):

    
#     def setUp(self):
#         self.client = Client()

#     def test_registeration_views(self):
#         response = self.client.get("http://127.0.0.1:8000/register/")
#         self.assertEqual(response.status_code, 200)

#         form = RegistrationForm()
#         response = self.client.post("http://127.0.0.1:8000/register/",{'form': form})
#         self.assertEqual(response.status_code, 200) ## Redirect on form success

#         response = self.client.post("http://127.0.0.1:8000/register/", {})
#         self.assertEqual(response.status_code, 200)

#     def test_registration_form(self):

#         # form = RegistrationForm()
#         # self.assertEquals(False, form.is_valid())

#         # data = {}
#         # form = RegistrationForm(data)
#         # self.assertEquals(False, form.is_valid())
#         # self.assertEquals([u'This field is required.'], form.errors['email'])

from django.utils import unittest
from django.test import TestCase
from django.test import Client
from tager_www.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)



class UserActionsTest(unittest.TestCase):
    def setUp(self):
        self.user1 = UserProfile(name="mahmoud", email="mahmoud@me.com",password="me",phone_number="9876543210")
        self.user1.save()
        self.user2 = UserProfile(name="mai", email="mai@me.com", password="me",phone_number="0123456789")
        self.user2.save()
        self.channel = Channel(name="cars",description="about cars")
        self.channel.save()
        self.subchannel = Subchannel(name="SUV", channel_id= channel)
        self.subchannel.save()
        self.post1 = Post(title="jeep",user= user1,sub_channel= subchannel,buyer= user2)
        self.post1.save()

    def user_created(self):
        self.assertEqual(self.user1.id, '1')
        self.assertEqual(self.user2.id, '2')
        
        # post,phone_numpost,phone_num

    def user_canRate_without_BuyerID(self):
        self.assertTrue(user2.canRate(self.post1),True)
        self.assertTrue(user1.canRate(self.post1),False)

