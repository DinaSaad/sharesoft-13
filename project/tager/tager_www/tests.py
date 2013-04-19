from datetime import datetime
from django.test import Client
from django.test import TestCase
from tager_www import views
from tager_www.models import UserProfile
from tager_www.models import Channel
from tager_www.models import Subchannel
from tager_www.models import Post
from tager_www.models import Comment
from django.core.urlresolvers import reverse
from tager_www.models import *
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.utils import unittest
from django.test import TestCase
from django.test import Client
from tager_www.models import *
from tager_www.forms import *
from datetime import datetime, timedelta
from django.conf import settings


class TagerTest(TestCase):

    def setUp(self):
        self.tharwat = UserProfile.objects.create(name = 'Tharwat', email = '1@.com', password = '123456')
        self.john = UserProfile.objects.create(name = 'John',  email = '2@.com', password = '123456')
        self.post = Post.objects.create(state="BMW", user = self.tharwat, no_of_reports=0, is_hidden=False, 
            pub_Date = datetime.datetime(2013,02,01), buyer = self.john)
        self.interestedin = InterestedIn.objects.create(user_id_buyer = self.john, user_id_seller = self.tharwat, post = self.post)
        report_reason = "Offensive"
        self.report = Report.objects.create(reported_post = self.post, report_type = report_reason, reporting_user = self.john)

    def test_models(self):
        self.assertEqual(self.post.state, "BMW")
        self.assertEqual(self.report.objects.count(), 1)
        self.assertEqual(self.interestedin.objects.count(), 1)




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
        self.post2 = Post(title="navigator",user= user1 ,sub_channel=subchannel)
        self.post2.save()

    def user_created(self):
        self.assertEqual(self.user1.id, '1')
        self.assertEqual(self.user2.id, '2')
        
        # post,phone_numpost,phone_num

    def add_buyers(self):
        self.assertEqual(user1.add_buyers(post1,"0123456789"), False)
        self.assertEqual(user1.add_buyers(post2,"0123456789"), True)
        self.assertEqual(user1.add_buyers(post1,"9876543210"), False)
    
    
    def user_canRate_without_BuyerID(self):
        self.assertTrue(user2.canRate(self.post1),True)
        self.assertTrue(user1.canRate(self.post1),False)


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CommentTestCase(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        
        self.user = UserProfile.objects.create_user(
        name = "hala",  
        email = "hala@gmail.com",
        facebook_uid = 1,
        accesstoken = "dff",
        date_Of_birth = "1993-05-4",
        phone_number = "01065157152",
        is_admin =False,      
        is_verfied =True,
        is_premium =False,
        photo ="" ,
        activation_key ="ef",
        expiration_key_date ="2013-04-4" ,
        status = "single",
        gender = "F")
        
        self.channel=Channel.objects.create(
        name = "cars",
        description = "bmw")
        
        self.subchannel=Subchannel.objects.create(
        name = "hi",
        channel_id =self.channel)
        
        self.post = Post.objects.create(
        state = "state",
        expired = False,
        no_of_reports = 2,
        title = "text",
        is_hidden = False,
        quality_index = 0.4,
        description = "ddd",
        price = 9,
        edit_date = "2013-04-4",
        pub_Date = "2013-04-4",
        comments_count = 0,
        intersed_count = 2,
        picture = "",
        sub_channel_id =self.subchannel,
        user = self.user,
        buyer = self.user,
        is_sold = False)

       

    def test_saving_comments(self):
        """
        Tests that we can create a Post
        """
        c = Client()
        response=c.get(reverse('adingcomment', kwargs={'post_id' : 1, 'content':'hjhgh'}))
        comments= Comment.objects.all()
        self.assertEqual(len(comments),1)
 



