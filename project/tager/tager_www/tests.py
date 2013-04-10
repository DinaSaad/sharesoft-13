"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase


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
        phone_number = "01065157152"
        is_admin ="False",      
        is_verfied ="True",
        is_premium ="False" 
        photo ="" 
        activation_key ="ef" 
        expiration_key_date ="2013-04-4" 
        status = "single"
        gender = "F")
        self.post = Post.objects.create(
                state = "state",
                expired = "False",
                no_of_reports = 2,
                title = "text",
                is_hidden = "False",
                quality_index = 0.4,
                description = "ddd",
                price = 9,
                edit_date = "2013-04-4",
                pub_Date = "2013-04-4",
                comments_count = 0,
                intersed_count = 2,
                picture = ""
                sub_channel_id = models.ForeignKey(Subchannel)
                user = self.user,
                buyer = self.user,
                is_sold = "False")
        self.comment=Comment.objects.create(
        	content="sedg",
            date=datetime.datetime.now(),
            is_Hidden="False"
            post_id= self.post
            user_id=self.user)
        self.c = Client()


    def test_comment_creation(self):
        """
        Tests that we can create a Post
        """
        self.assertEqual(self.comment.content, "sedg")
        self.assertEqual(self.comment.user_id, self.user)

    def test_user_can_ comment(self):
        """
        Tests that a user is allowed to read.
        """
        self.c.login(username="hala@gmail.com", password="kolo")
        response = self.c.get('/news/get_comment/1/')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, '{}')
    def test_i_read_this(self):
        """
        Tests a new user marking the story as read.
        """
        self.c.login(username='newsposter', password='newspass')
        response = self.c.post('/news/read/1/', {'add':True})
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.content, '{\n    "read": true\n}')


