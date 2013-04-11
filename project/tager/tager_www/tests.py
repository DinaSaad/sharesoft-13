"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from datetime import datetime
from django.test import Client
from django.test import TestCase
from django.core.urlresolvers import reverse
from tager_www.models import *
from django.contrib.auth.models import User
from django.utils.timezone import utc

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

