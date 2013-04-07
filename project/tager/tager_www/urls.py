from django.conf.urls import *

from tager_www import views

urlpatterns = patterns('',	
	url(r'^hello', views.view_subchannels, name='index'),
	url(r'^viewchannels$', views.view_channels, name='index'),
)
