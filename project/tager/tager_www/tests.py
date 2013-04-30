
# from django.test.TestCase import TestCase
from models import *
from django.utils import unittest
from django.test import TestCase
from django.test import Client
from tager_www.forms import *
from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.contrib.auth import SESSION_KEY 
from django.test.client import RequestFactory



class viewingPostsRelatedToSubchannel(TestCase):
	
    def setUp(self):
        self.channel = Channel.objects.create(name="cars", description="greate deals in cars")
        self.subchannel = SubChannel(name="4x4", channel= self.channel)

    def test_models(self):
        self.assertEqual(self.channel.name, "cars")
        self.assertEqual(self.subchannel.channel_id, 1)

	





# class TagerTest(TestCase):

#     def setUp(self):
#         self.tharwat = UserProfile.objects.create(name = 'Tharwat', email = '1@.com', password = '123456')
#         self.john = UserProfile.objects.create(name = 'John',  email = '2@.com', password = '123456')
#         self.post = Post.objects.create(state="BMW", user = self.tharwat, no_of_reports=0, is_hidden=False, 
#             pub_Date = datetime.datetime(2013,02,01), buyer = self.john)
#         self.interestedin = InterestedIn.objects.create(user_id_buyer = self.john, user_id_seller = self.tharwat, post = self.post)
#         report_reason = "Offensive"
#         self.report = Report.objects.create(reported_post = self.post, report_type = report_reason, reporting_user = self.john)

#     def test_models(self):
#         self.assertEqual(self.post.state, "BMW")
#         self.assertEqual(self.report.objects.count(), 1)
#         self.assertEqual(self.interestedin.objects.count(), 1)


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


class UserActionsTest(unittest.TestCase):
    def setUp(self):
        self.user1 = UserProfile(name="mahmoud", email="mahmoud@me.com",password="me",phone_number="111")
        self.user1.save()
        self.user2 = UserProfile(name="mai", email="mai@me.com", password="me",phone_number="222")
        self.user2.save()
        self.user3 = UserProfile(name="beshoy", email="beshoy@me.com", password="me",phone_number="333")
        self.user3.save()
        self.user4 = UserProfile(name="abdo", email="abdo@me.com", password="me",phone_number="444")
        self.user4.save()
        self.channel = Channel(name="cars",description="about cars")
        self.channel.save()
        self.subchannel = Subchannel(name="SUV", channel_id= channel)
        self.subchannel.save()
        self.post1 = Post(title="jeep",user= user1,sub_channel= subchannel,buyer= user2)
        self.post1.save()
        self.post2 = Post(title="navigator",user= user1 ,sub_channel=subchannel,buyer= user3)
        self.post2.save()
        self.post3 = Post(title="ram",user= user1 ,sub_channel=subchannel,buyer= user4)
        self.post2.save()
        self.post4 = Post(title="ram truck",user= user2 ,sub_channel=subchannel,buyer= user1)
        self.post2.save()

    def user_created(self):

        self.assertEqual(self.user1.id, '1')
        self.assertEqual(self.user2.id, '2')
        
        # post,phone_numpost,phone_num

    def add_buyers(self):
        self.assertEqual(user1.add_buyers(post1,"111"), False)
        self.assertEqual(user1.add_buyers(post2,"111"), True)
        self.assertEqual(user1.add_buyers(post1,"222"), False)
    
    
    def user_canRate_without_BuyerID(self):
        self.assertTrue(user2.canRate(self.post1),True)
        self.assertTrue(user1.canRate(self.post1),False)


    def user_get_interested_buyers(self):
        self.assertEqual(user1.get_interacting_people(),[user2,user3,user4])
        self.assertEqual(user2.get_interacting_people(),[user1])
        self.assertEqual(user3.get_interacting_people(),[user1])
        self.assertEqual(user4.get_interacting_people(),[user1])

class Postrelatedtests(unittest.TestCase):
    def setUp(self):
        
        self.user = UserProfile.objects.create(name="Abdelrahman", email="abdelrahman.maged@gmail.com")
        self.channel = Channel.objects.create(name="cars", description="greate deals in cars")
        self.subchannel = SubChannel.objects.create(name="4x4", channel= self.channel)

        self.post1 = Post.objects.create(title="test",
            description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
        self.post2 = Post.objects.create(title="test",
            description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
        self.factory = RequestFactory()
#     def test_user_can_post(self):
        
#         self.assertFalse(self.user.can_post())
#         self.user.is_verfied = True
#         self.user.save()
#         self.assertTrue(self.user.can_post())
        
        
#         self.post3 = Post.objects.create(title="test",
#             description="1",price="12",location="cairo", seller=self.user, subchannel = self.subchannel)
#         self.assertFalse(self.user.can_post())
#         self.user.is_premium = True
#         self.user.save()
#         self.assertTrue(self.user.can_post())
#         self.post4 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post5 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post6 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user, subchannel = self.subchannel)
#         self.post7 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post8 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post9 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user, subchannel = self.subchannel)
#         self.post10 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post11 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post12 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user, subchannel = self.subchannel)
#         self.user.is_premium = False
#         self.user.save()
#         self.assertEqual(self.user.add_to_wish_list(self.post1),"true")
#         WishList.objects.create(user=self.user, post = self.post1)
#         self.assertEqual(self.user.add_to_wish_list(self.post1),"false")
#         self.assertFalse(self.user.can_post())
    

     
# #   