from django.conf.urls import *

from tager_www import views

urlpatterns = patterns('',	
	url(r'^$', views.index, name='index')
)
