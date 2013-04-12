from django.test.TestCase import TestCase
from models import *

class viewingPostsRelatedToSubchannel(TestCase):
	def setUp(self):
        self.channel = channel.objects.create(name="cars", description="greate deals in cars")
        self.subchannel = subchannel(name="4x4", channel_id= channel)

	def test_models(self):
        self.assertEqual(self.channel.name, "cars")
        self.assertEqual(self.subchannel.channel_id_id, 1)

	