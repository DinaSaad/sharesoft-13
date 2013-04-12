from django.conf.urls import *

from tager_www import views


from django.views.generic import ListView, DetailView
from tager_www.models import *
from tager_www.views import *

urlpatterns = patterns('tager_www.views',	
	url(r'^hello', views.view_subchannels, name='index'),
	url(r'^viewchannels$', views.view_channels, name='index'),
	url(r'^$', ListView.as_view(
    	queryset = Post.objects.all().order_by('id')[:5],
    	template_name = "post.html")),
    url(r'^reportPage/$', 'goToTheReportPage'),
    url(r'^report/$', 'reportThePost'),
    url(r'^advanced_search/att/$','tager_www.views.get_attributes_of_subchannel'),
    url(r'^advanced_search/subchannel/$','tager_www.views.view_subchannels'),
    url(r'^advanced_search/channel/$','tager_www.views.view_channels'),
    url(r'^advanced_search/$','tager_www.views.advanced_search'),
)
)
