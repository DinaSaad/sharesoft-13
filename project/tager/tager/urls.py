from django.conf.urls import *
from tager_www import views
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',	
	url(r'^hello', views.view_subchannels, name='index'),
	url(r'^viewchannels$', views.view_channels, name='index'),
	url(r'^search/', include('haystack.urls')),
	url(r'^tager/', include('tager.urls')),
    
)



