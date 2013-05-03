
# from django.test.TestCase import TestCase
from models import *
from django.utils import unittest
from django.test import TestCase
from django.test import Client
# from tager_www.forms import *
# from datetime import datetime, timedelta
# from django.conf import settings
# from django.core.urlresolvers import reverse
# from django.contrib.auth.models import User
# from django.utils.timezone import utc
# from django.contrib.auth import SESSION_KEY 
from django.test.client import RequestFactory
from views import *
from django.shortcuts import RequestContext


# x





# # class TagerTest(TestCase):

# #     def setUp(self):
# #         self.tharwat = UserProfile.objects.create(name = 'Tharwat', email = '1@.com', password = '123456')
# #         self.john = UserProfile.objects.create(name = 'John',  email = '2@.com', password = '123456')
# #         self.post = Post.objects.create(state="BMW", user = self.tharwat, no_of_reports=0, is_hidden=False, 
# #             pub_Date = datetime.datetime(2013,02,01), buyer = self.john)
# #         self.interestedin = InterestedIn.objects.create(user_id_buyer = self.john, user_id_seller = self.tharwat, post = self.post)
# #         report_reason = "Offensive"
# #         self.report = Report.objects.create(reported_post = self.post, report_type = report_reason, reporting_user = self.john)

# #     def test_models(self):
# #         self.assertEqual(self.post.state, "BMW")
# #         self.assertEqual(self.report.objects.count(), 1)
# #         self.assertEqual(self.interestedin.objects.count(), 1)


# class UserProfileTest(TestCase):

#     def setUp(self):

#         self.user1 = UserProfile.objects.create_user(email="mai@gmail.com", name="mai", password="123")
#         self.user1.save()
#         self.user2 = UserProfile.objects.create_user(email="ayia@gmail.com", name="ayia", password="123",status="testing")
#         self.user2.save()
#         self.user3 = UserProfile.objects.create_superuser(email="mahmoud@gmail.com", name="mahmoud", password="123")
#         self.user3.save()

#     def test_UserProfile(self):
#         self.assertEqual(self.user1.email , "mai@gmail.com")
#         self.assertEqual(self.user2.email , "ayia@gmail.com")
       
#         profile1 = UserProfile.objects.get(pk=1)
#         self.assertEquals(profile1.name,'mai')
#         self.assertEquals(profile1.is_active,True)

        
#         profile2 = UserProfile.objects.get(pk=3)
#         # self.assertFalse(profile2.status ,"testing")
    
#         profile3 = UserProfile.objects.get(pk=3)
#         # self.assertEquals(profile3.is_admin,True)

#         profile3.name = "mahmoud1"
#         profile3.save()
#         UserProfile.objects.get(pk=3)
#         self.assertEquals(profile3.name,"mahmoud1")


# class UserActionsTest(unittest.TestCase):
#     def setUp(self):
#         self.user1 = UserProfile(name="mahmoud", email="mahmoud@me.com",password="me",phone_number="111")
#         self.user1.save()
#         self.user2 = UserProfile(name="mai", email="mai@me.com", password="me",phone_number="222")
#         self.user2.save()
#         self.user3 = UserProfile(name="beshoy", email="beshoy@me.com", password="me",phone_number="333")
#         self.user3.save()
#         self.user4 = UserProfile(name="abdo", email="abdo@me.com", password="me",phone_number="444")
#         self.user4.save()
#         self.channel = Channel(name="cars",description="about cars")
#         self.channel.save()
#         self.subchannel = Subchannel(name="SUV", channel_id= channel)
#         self.subchannel.save()
#         self.post1 = Post(title="jeep",user= user1,sub_channel= subchannel,buyer= user2)
#         self.post1.save()
#         self.post2 = Post(title="navigator",user= user1 ,sub_channel=subchannel,buyer= user3)
#         self.post2.save()
#         self.post3 = Post(title="ram",user= user1 ,sub_channel=subchannel,buyer= user4)
#         self.post2.save()
#         self.post4 = Post(title="ram truck",user= user2 ,sub_channel=subchannel,buyer= user1)
#         self.post2.save()

#     def user_created(self):

#         self.assertEqual(self.user1.id, '1')
#         self.assertEqual(self.user2.id, '2')
        
#         # post,phone_numpost,phone_num

#     def add_buyers(self):
#         self.assertEqual(user1.add_buyers(post1,"111"), False)
#         self.assertEqual(user1.add_buyers(post2,"111"), True)
#         self.assertEqual(user1.add_buyers(post1,"222"), False)
    
    
#     def user_canRate_without_BuyerID(self):
#         self.assertTrue(user2.canRate(self.post1),True)
#         self.assertTrue(user1.canRate(self.post1),False)


#     def user_get_interested_buyers(self):
#         self.assertEqual(user1.get_interacting_people(),[user2,user3,user4])
#         self.assertEqual(user2.get_interacting_people(),[user1])
#         self.assertEqual(user3.get_interacting_people(),[user1])
#         self.assertEqual(user4.get_interacting_people(),[user1])




# class Postrelatedtests(unittest.TestCase):
#     def setUp(self):
        
#         self.user = UserProfile.objects.create(name="mai", email="abdelrahman.maged@gmail.com")
#         self.channel = Channel.objects.create(name="cars", description="greate deals in cars")
#         self.subchannel = SubChannel.objects.create(name="4x4", channel= self.channel)

#         self.post1 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.post2 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.factory = RequestFactory()
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
    

  
# class  intersted(unittest.TestCase):

#     def setUp(self):
#         self.client = Client()
#         self.user = UserProfile.objects.create_user(email="mai@gmail.com", name="mai",password = "123")
#         self.channel = Channel.objects.create(name="cars", description="greate deals in cars")
#         self.subchannel = SubChannel.objects.create(name="4x4", channel= self.channel)



#         self.post2 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.factory = RequestFactory()
 
    

    # def test_sms(self):
        
    #     user = self.client.login(email='mai@gmail.com', password='123')        
    #     self.assertEqual(self.user.sms_code, None)  #no code saved yet

        
    #     response = self.client.post('/send_phone/',{'phone_number': '01112285911'})
    #     self.assertEqual(response.status_code, 200)
    #     self.assertFalse(self.user.sms_code , None)  #code is saved
    #     sms_code = self.user.sms_code
    #     response = self.client.post('/send_sms/',{'sms_code': sms_code})  
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post('/send_sms/',{'sms_code': "12r"}) # handeled in my code if the user enters a wrong code



# class  Postrelatedtests(unittest.TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()
#         self.client = Client()
        
#         # self.adminuser = UserProfile.objects.create_user(email="abdelrahmanmaged@gmail.com", name="abdelrahman",password = "123")

        # self.adminuser = UserProfile.objects.create_user(email="abdelrahmanmaged@gmail.com", name="abdelrahman",password = "123")

        
    # def test_user_can_post(self):
    #     self.channel = Channel.objects.create(name="Automotive", description="test channel")
    #     self.subchannel = SubChannel.objects.create(name="Bus", channel= self.channel)
    #     self.testuser = UserProfile.objects.create_user(email="abdelrahman@gmail.com", name="abdelrahman",password = "123")
    #     self.assertEqual(self.testuser.can_post(),False)
    #     self.testuser.is_verfied = True
    #     self.testuser.save()
    #     self.assertEqual(self.testuser.can_post(),True)
    #     self.post1 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.testuser , subchannel = self.subchannel)
    #     self.post2 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.testuser , 
    #          subchannel = self.subchannel)
    #     self.assertEqual(self.testuser.can_post(),True)
    #     self.post3 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.testuser , 
    #          subchannel = self.subchannel)
    #     self.assertEqual(self.testuser.can_post(),False)
    #     self.testuser.is_premium = True
    #     self.testuser.save()
    #     self.assertEqual(self.testuser.can_post(),True)
    #     self.assertEqual(self.testuser.add_to_wish_list(self.post1),"true")
    #     WishList.objects.create(user = self.testuser, post = self.post1)
    #     self.assertEqual(self.testuser.add_to_wish_list(self.post1),"false")
    #     self.assertEqual(self.testuser.add_to_wish_list(self.post2),"true")

    # def test_admin_can_hide_post(self):
    #     self.adminuser = UserProfile.objects.create_user(email="adminabdelrahman@gmail.com", name="abdelrahman",password = "123")
    #     self.channel = Channel.objects.create(name="Automotive2", description="test channel")
    #     self.subchannel = SubChannel.objects.create(name="Bus2", channel= self.channel)
    #     self.adminuser.is_admin = True
    #     self.adminuser.save()
    #     user = self.client.login(email='adminabdelrahman@gmail.com', password='123')
        
    #     self.post3 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.adminuser , 
    #          subchannel = self.subchannel)
    #     response = self.client.post('/deletepost/',{'post': self.post3.id})
    #     self.testpostresult = Post.objects.get(id=self.post3.id)
    #     self.assertTrue(self.testpostresult.is_hidden)
    #     self.assertEqual(response.status_code,200)
    
    # def test_post_author_can_edit_post(self):
    #     self.adminuser = UserProfile.objects.create_user(email="editabdelrahman@gmail.com", name="abdelrahman",password = "123")
    #     self.channel = Channel.objects.create(name="Automotive3", description="test channel")
    #     self.subchannel = SubChannel.objects.create(name="Bus3", channel= self.channel)
    #     self.post3 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.adminuser , 
    #          subchannel = self.subchannel)
    #     self.testattribute = Attribute.objects.create(name="colour", subchannel = self.subchannel, weight="1")
    #     self.value = Value.objects.create(attribute = self.testattribute,post= self.post3, value="467")
    #     user = self.client.login(email='editabdelrahman@gmail.com', password='123')
    #     response = self.client.post('/editposttitle/',{'post':1, 'title':"hello"})
    #     self.resultpost = Post.objects.get(id=1)
    #     self.assertEqual(self.resultpost.title,"hello")
    #     self.assertEqual(response.status_code,200)
    #     response = self.client.post('/editpostdescription/',{'post':1, 'description':"testdescription"})
    #     self.resultpost = Post.objects.get(id=1)
    #     self.assertEqual(self.resultpost.description,"testdescription")
    #     self.assertEqual(response.status_code,200)
    #     response = self.client.post('/editpostprice/',{'post':1, 'price':"12345"})
    #     self.resultpost = Post.objects.get(id=1)
    #     self.assertEqual(self.resultpost.price,12345)
    #     self.assertEqual(response.status_code,200)
    #     response = self.client.post('/editpostlocation/',{'post':1, 'location':"testlocation"})
    #     self.resultpost = Post.objects.get(id=1)
    #     self.assertEqual(self.resultpost.location,"testlocation")
    #     self.assertEqual(response.status_code,200)

        
    #     response = self.client.post('/editpostattribute/',{'post':self.post3.id, 'attribute':self.testattribute.id, 'value':"testing"})
    #     self.resultvalue = Value.objects.get(id=1)
    #     self.assertEqual(self.resultvalue.value,"testing")
    #     self.assertEqual(response.status_code,200)

    # def test_user_can_add_and_delete_posts_to_from_wishlist(self):
    #     self.wishuser = UserProfile.objects.create_user(email="wishabdelrahman@gmail.com", name="abdelrahman",password = "123")
    #     self.channel = Channel.objects.create(name="Automotive4", description="test channel")
    #     self.subchannel = SubChannel.objects.create(name="Bus4", channel= self.channel)
    #     self.post3 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.wishuser , 
    #          subchannel = self.subchannel)
    #     self.post4 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.wishuser , 
    #          subchannel = self.subchannel)
    #     self.post5 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.wishuser , 
    #          subchannel = self.subchannel)
    #     self.post6 = Post.objects.create(title="test",
    #          description="1", price="12",location="cairo", seller=self.wishuser , 
    #          subchannel = self.subchannel)
    #     user = self.client.login(email='wishabdelrahman@gmail.com', password='123')
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,0)
    #     response = self.client.post('/addtomylist',{'post':self.post3.id})
    #     self.assertEqual(response.status_code,200)
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,1)

    #     response = self.client.post('/removepostfromwishlist',{'post':self.post3.id})
    #     self.assertEqual(response.status_code,200)
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,0)
    #     response = self.client.post('/addtomylist',{'post':self.post4.id})
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,1)
    #     response = self.client.post('/addtomylist',{'post':self.post5.id})
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,2)
    #     response = self.client.post('/addtomylist',{'post':self.post6.id})
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,3)
    #     response = self.client.post('/emptywishlist/')
    #     self.assertEqual(response.status_code,200)
    #     count = WishList.objects.all().count()
    #     self.assertEqual(count,0)
        
#     def test_user_can_post(self):
#         self.channel = Channel.objects.create(name="Automotive", description="test channel")
#         self.subchannel = SubChannel.objects.create(name="Bus", channel= self.channel)
#         self.testuser = UserProfile.objects.create_user(email="abdelrahman@gmail.com", name="abdelrahman",password = "123")
#         self.assertEqual(self.testuser.can_post(),False)
#         self.testuser.is_verfied = True
#         self.testuser.save()
#         self.assertEqual(self.testuser.can_post(),True)
#         self.post1 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.testuser , subchannel = self.subchannel)
#         self.post2 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.testuser , 
#              subchannel = self.subchannel)
#         self.assertEqual(self.testuser.can_post(),True)
#         self.post3 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.testuser , 
#              subchannel = self.subchannel)
#         self.assertEqual(self.testuser.can_post(),False)
#         self.testuser.is_premium = True
#         self.testuser.save()
#         self.assertEqual(self.testuser.can_post(),True)
#         self.assertEqual(self.testuser.add_to_wish_list(self.post1),"true")
#         WishList.objects.create(user = self.testuser, post = self.post1)
#         self.assertEqual(self.testuser.add_to_wish_list(self.post1),"false")
#         self.assertEqual(self.testuser.add_to_wish_list(self.post2),"true")

#     def test_admin_can_hide_post(self):
#         self.adminuser = UserProfile.objects.create_user(email="adminabdelrahman@gmail.com", name="abdelrahman",password = "123")
#         self.channel = Channel.objects.create(name="Automotive2", description="test channel")
#         self.subchannel = SubChannel.objects.create(name="Bus2", channel= self.channel)
#         self.adminuser.is_admin = True
#         self.adminuser.save()
#         user = self.client.login(email='adminabdelrahman@gmail.com', password='123')
        
#         self.post3 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.adminuser , 
#              subchannel = self.subchannel)
#         response = self.client.post('/deletepost/',{'post': self.post3.id})
#         self.testpostresult = Post.objects.get(id=self.post3.id)
#         self.assertTrue(self.testpostresult.is_hidden)
#         self.assertEqual(response.status_code,200)
    
#     def test_post_author_can_edit_post(self):
#         self.adminuser = UserProfile.objects.create_user(email="editabdelrahman@gmail.com", name="abdelrahman",password = "123")
#         self.channel = Channel.objects.create(name="Automotive3", description="test channel")
#         self.subchannel = SubChannel.objects.create(name="Bus3", channel= self.channel)
#         self.post3 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.adminuser , 
#              subchannel = self.subchannel)
#         self.testattribute = Attribute.objects.create(name="colour", subchannel = self.subchannel, weight="1")
#         self.value = Value.objects.create(attribute = self.testattribute,post= self.post3, value="467")
#         user = self.client.login(email='editabdelrahman@gmail.com', password='123')
#         response = self.client.post('/editposttitle/',{'post':1, 'title':"hello"})
#         self.resultpost = Post.objects.get(id=1)
#         self.assertEqual(self.resultpost.title,"hello")
#         self.assertEqual(response.status_code,200)
#         response = self.client.post('/editpostdescription/',{'post':1, 'description':"testdescription"})
#         self.resultpost = Post.objects.get(id=1)
#         self.assertEqual(self.resultpost.description,"testdescription")
#         self.assertEqual(response.status_code,200)
#         response = self.client.post('/editpostprice/',{'post':1, 'price':"12345"})
#         self.resultpost = Post.objects.get(id=1)
#         self.assertEqual(self.resultpost.price,12345)
#         self.assertEqual(response.status_code,200)
#         response = self.client.post('/editpostlocation/',{'post':1, 'location':"testlocation"})
#         self.resultpost = Post.objects.get(id=1)
#         self.assertEqual(self.resultpost.location,"testlocation")
#         self.assertEqual(response.status_code,200)
        
#         response = self.client.post('/editpostattribute/',{'post':self.post3.id, 'attribute':self.testattribute.id, 'value':"testing"})
#         self.resultvalue = Value.objects.get(id=1)
#         self.assertEqual(self.resultvalue.value,"testing")
#         self.assertEqual(response.status_code,200)

#     def test_user_can_add_and_delete_posts_to_from_wishlist(self):
#         self.wishuser = UserProfile.objects.create_user(email="wishabdelrahman@gmail.com", name="abdelrahman",password = "123")
#         self.channel = Channel.objects.create(name="Automotive4", description="test channel")
#         self.subchannel = SubChannel.objects.create(name="Bus4", channel= self.channel)
#         self.post3 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.wishuser , 
#              subchannel = self.subchannel)
#         self.post4 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.wishuser , 
#              subchannel = self.subchannel)
#         self.post5 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.wishuser , 
#              subchannel = self.subchannel)
#         self.post6 = Post.objects.create(title="test",
#              description="1", price="12",location="cairo", seller=self.wishuser , 
#              subchannel = self.subchannel)
#         user = self.client.login(email='wishabdelrahman@gmail.com', password='123')
#         count = WishList.objects.all().count()
#         self.assertEqual(count,0)
#         response = self.client.post('/addtomylist',{'post':self.post3.id})
#         self.assertEqual(response.status_code,200)
#         count = WishList.objects.all().count()
#         self.assertEqual(count,1)

#         response = self.client.post('/removepostfromwishlist',{'post':self.post3.id})
#         self.assertEqual(response.status_code,200)
#         count = WishList.objects.all().count()
#         self.assertEqual(count,0)
#         response = self.client.post('/addtomylist',{'post':self.post4.id})
#         count = WishList.objects.all().count()
#         self.assertEqual(count,1)
#         response = self.client.post('/addtomylist',{'post':self.post5.id})
#         count = WishList.objects.all().count()
#         self.assertEqual(count,2)
#         response = self.client.post('/addtomylist',{'post':self.post6.id})
#         count = WishList.objects.all().count()
#         self.assertEqual(count,3)
#         response = self.client.post('/emptywishlist/')
#         self.assertEqual(response.status_code,200)
#         count = WishList.objects.all().count()
#         self.assertEqual(count,0)
        



class  AccountsType(unittest.TestCase):


    def setUp(self):

        self.user1 = UserProfile.objects.create_user(email="riham@gmail.com", name="riham", password="123", is_premium = False)
        self.user1.save()
        self.user2 = UserProfile.objects.create_user(email="ahmad@gmail.com", name="ayia", password="123",is_premium = True)
        self.user2.save()

    def test_changingAccountType(self):
        self.assertEqual(self.user1.email , "riham@gmail.com")
        self.assertEqual(self.user2.email , "ahmad@gmail.com")

        heba = UserProfile.objects.get(pk=1)
        ahmad = UserProfile.objects.get(pk=2)
        heba.is_premium = True
        ahmad.is_premium = False
        heba.save()
        ahmad.save()
        UserProfile.objects.get(pk=1)
        UserProfile.objects.get(pk=2)
        self.assertEqual(heba.is_premium, True)
        self.assertEqual(ahmad.is_premium, False)


   
# class  PrivateSettings(unittest.TestCase):

# def setUp(self):

#         self.user1 = UserProfile.objects.create_user(email="heba@gmail.com", name="mai", password="123", private_number = False, private_work = False)
#         self.user1.save()
#         self.user2 = UserProfile.objects.create_user(email="ahmad@gmail.com", name="ayia", password="123",private_number = True, private_work = True)
#         self.user2.save()

#     def test_user_privatenumber(self):
#         user6 = UserProfile.objects.get(id=1)
#         self.assertEqual(self.user6.name, 'Happy')
#         self.assertEqual(self.user6.private_number, False)

#         user6.private_number = True
#         user6.save()
#         self.assertEqual(self.user6.private_number(),True)
#         self.assertEqual(self.user6.private_number, True)

#      def test_user_private1-work(self):
#         user7 = UserProfile.objects.get(id=2)
#         self.assertEqual(self.user7.name, 'Ahmad')
#         self.assertEqual(self.user7.private_work, False)

#         user7.private_work = True
#         user7.save()
#         self.assertEqual(self.user7.priavte_work(),True)
#         self.assertEqual(self.user7.private_work, True)

# class TestSubchannelRelatedPosts(unittest.TestCase):
#     def initiateSubchannelsAndPosts(self):
#         U1 = UserProfile(name="test user 1",email="test123@test.com",password="123",is_verfied = True,activation_key = True);U1.save();
#         self.Ch1 = Channel.objects.create(name="channel 1 ",description="ch1 descrip");Ch1.save();

#         self.Sub1 = SubChannel.objects.create(name="first sub to channel 1",channel_id=(Ch1.id));Sub1.save();
#         self.Sub2 = SubChannel.objects.create(name="secnd sub to channel 1",channel_id=(Ch1.id));Sub2.save();

#         self.P1= Post.objects.create(state="New",expired=False,title="Title of post 1",is_hidden=False,quality_index=67,price=100,is_sold=False,subchannel=Sub1,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="cairo");P1.save();
#         self.P2= Post.objects.create(state="archived",expired=False,title="Title of post 2",is_hidden=False,quality_index=80,price=100,is_sold=False,subchannel=Sub1,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="sharm");P2.save();
#         self.P3= Post.objects.create(state="old",expired=False,title="Title of post 3",is_hidden=False,quality_index=60,price=100,is_sold=False,subchannel=Sub1,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="alex");P3.save();
#         self.P4= Post.objects.create(state="New",expired=False,title="Title of post 4",is_hidden=False,quality_index=90,price=100,is_sold=False,subchannel=Sub2,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="alex");P4.save();
#         self.P5= Post.objects.create(state="archived",expired=False,title="Title of post 5",is_hidden=False,quality_index=100,price=100,is_sold=True,subchannel=Sub2,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="giza");P5.save();
#         self.P6= Post.objects.create(state="old",expired=False,title="Title of post 6",is_hidden=True,quality_index=100,price=100,is_sold=False,subchannel=Sub2,seller=U1,no_of_reports=0,pub_date=datetime.now(), location="cairo");P6.save();

#         self.assertEqual(P3.subchannel, 'Sub1')
#         self.assertEqual(P4.subchannel, 'Sub2')
#         check_posts = menuForSubchannels(1)
#         self.assertEqual(check_posts, 'P1,P2,P3')


#         list_of_subchannelIDs = [Sub1.id]
#         list_of_states = [ 'New', 'old']
#         view_posts = view_checked_subchannel_posts(list_of_states, list_of_subchannelIDs)
#         self.assertEqual(view_posts, 'P1,P3') 
#         list_of_subchannelIDs2 = [Sub1.id, Sub2.id]
#         list_of_states2 = [ 'New', 'archived']
#         view_posts2 = view_checked_subchannel_posts(list_of_states, list_of_subchannelIDs)
#         self.assertEqual(view_posts2, 'P1,P2,P4,P5') 



# class ActivityLog(object):
#     def setUp(self):
#         self.client = Client()
#         user1=UserProfile(name='Mohamed',email='1@3.com',password='123');user1.save()
#         user2=UserProfile(name='Amr',email='2@3.com',password='123');user2.save()
#         channel1=Channel(name='cars',description='jkj');channel1.save()
#         subchannel1=SubChannel(name='sport cars',channel=channel1);subchannel1.save()
#         subchannel2=SubChannel(name='SUV',channel=channel1);subchannel2.save()
#         attribute1=Attribute(name='color',subchannel=subchannel1,weight=1);attribute1.save()
#         attribute2=Attribute(name='color',subchannel=subchannel2,weight=1);attribute2.save()
#         choice1=AttributeChoice(attribute_id=attribute1, value='red');choice1.save()
#         choice2=AttributeChoice(attribute_id=attribute2, value='red');choice2.save()
#         subscription1=Subscription(channel=channel1,sub_channel=subchannel1,parameter=attribute1,choice=choice1);subscription1.save()
#         subscription2=Subscription(channel=channel1,sub_channel=subchannel1);subscription2.save()
#         subscription3=Subscription(channel=channel1);subscription3.save()
#         subscription4=Subscription(channel=channel1,sub_channel=subchannel2,parameter=attribute2,choice=choice2);subscription4.save()
#         subscription5=Subscription(channel=channel1,sub_channel=subchannel2);subscription5.save()
#         channel2=Channel(name='Anaimals',description='jkj');channel2.save()
#         subchannel3=SubChannel(name='Cats',channel=channel2);subchannel3.save()
#         subchannel4=SubChannel(name='Dogs',channel=channel2);subchannel4.save()
#         attribute3=Attribute(name='age',subchannel=subchannel3,weight=1);attribute3.save()
#         attribute4=Attribute(name='age',subchannel=subchannel4,weight=1);attribute4.save()
#         choice3=AttributeChoice(attribute_id=attribute3, value='2');choice3.save()
#         choice4=AttributeChoice(attribute_id=attribute4, value='2');choice4.save()
#         subscription6=Subscription(channel=channel2,sub_channel=subchannel3,parameter=attribute3,choice=choice3);subscription6.save()
#         subscription7=Subscription(channel=channel2,sub_channel=subchannel3);subscription7.save()
#         subscription8=Subscription(channel=channel2);subscription8.save()
#         subscription9=Subscription(channel=channel2,sub_channel=subchannel4,parameter=attribute4,choice=choice4);subscription9.save()
#         subscription10=Subscription(channel=channel2,sub_channel=subchannel4);subscription10.save()
#         P1= Post(state="New",expired=False,title="Title of post 1",is_hidden=False,quality_index=67,price=100,is_sold=False,subchannel=subchannel1,seller=user1,no_of_reports=0,pub_date=datetime.dtaetime.datetime.now());P1.save();
#         P2= Post(state="New",expired=False,title="Title of post 2",is_hidden=False,quality_index=80,price=100,is_sold=False,subchannel=subchannel1,seller=user1,no_of_reports=0,pub_date=datetime.datetime.now());P2.save();
#         P3= Post(state="New",expired=False,title="Title of post 3",is_hidden=False,quality_index=60,price=100,is_sold=False,subchannel=subchannel2,seller=user1,no_of_reports=0,pub_date=datetime.datetime.now());P3.save();
#         P4= Post(state="New",expired=False,title="Title of post 4",is_hidden=False,quality_index=90,price=100,is_sold=False,subchannel=subchannel2,seller=user1,no_of_reports=0,pub_date=datetime.datetime.now());P4.save();
#         P5= Post(state="New",expired=False,title="Title of post 5",is_hidden=False,quality_index=100,price=100,is_sold=True,subchannel=subchannel3,seller=user1,no_of_reports=0,pub_date=datetime.datetime.now());P5.save();
#         P6= Post(state="New",expired=False,title="Title of post 6",is_hidden=True,quality_index=100,price=100,is_sold=False,subchannel=subchannel3,seller=user2,no_of_reports=0,pub_date=datetime.datetime.now());P6.save();
#         P7= Post(state="New",expired=True,title="Title of post 7",is_hidden=False,quality_index=100,price=100,is_sold=False,subchannel=subchannel4,seller=user2,no_of_reports=0,pub_date=datetime.datetime.now());P7.save();


#     def test_activity(self):       
#         user = self.client.login(email='mai@gmail.com', password='123')
#         response = self.client.post('/all_log/')
#         self.assertEqual(response.status_code, 200)
#         response = self.client.post('/all_log_post/')  
#         self.assertEqual(response.status_code, 200)
#         response = self.client.post('/all_log_wish/') # handeled in my code if the user enters a wrong code
#         self.assertEqual(response.status_code, 200)
#         response = self.client.post('/all_log_interested/')  
#         self.assertEqual(response.status_code, 200)
#         response = self.client.post('/all_log_profile/')  
#         self.assertEqual(response.status_code, 200)

# class intrested_in(unittest.TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = UserProfile.objects.create_user(email="mai@gmail.com", name="mai",password = "123")
#         self.channel = Channel.objects.create(name="cars", description="greate deals in cars")
#         self.subchannel = SubChannel.objects.create(name="4x4", channel= self.channel)
#         self.post2 = Post.objects.create(title="test",
#             description="1", price="12",location="cairo", seller=self.user , subchannel = self.subchannel)
#         self.factory = RequestFactory()
    
#     def interestedin(self):     
#         self.assertEqual(InterestedIn.objects.filter(user_id_buyer = user, post = post).exists(),False)
#         response = self.client.post('/intrested/',{'post_id': post.id})
#         self.assertEqual(InterestedIn.objects.filter(user_id_buyer = user, post = post).exists(),True)

