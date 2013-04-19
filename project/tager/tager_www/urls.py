from django.conf.urls import *

from tager_www import views


from django.views.generic import ListView, DetailView
from tager_www.models import *
from tager_www.views import *

urlpatterns = patterns('tager_www.views',
	url(r'^hello', views.view_subchannels, name='index'),
	url(r'^viewchannels$', views.view_channels, name='index'),
	# url(r'^$', ListView.as_view(
 #    	posts = Post.objects.all().order_by('id')[:5],
 #    	template_name = "post.html")),
	url(r'^$', 'show_posts', name='posts'),
    

urlpatterns = patterns('',	
	

)
