
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

