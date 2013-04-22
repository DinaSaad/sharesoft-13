from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from tager_www.views import *



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    
    url(r'^logout/$', logout, {'next_page':'/login'}),  

    url(r'^$', 'tager_www.views.home'),
    url(r'^main$', 'tager_www.views.main'),
    url(r'^intrested/$', 'tager_www.views.intrested'),   
    url(r'^report/$', 'tager_www.views.report_the_post', name='reportThePost'),
    url(r'^login/$', 'tager_www.views.view_login'),
    url(r'^logged/$', 'tager_www.views.login'),
    url(r'^addBuyer/$', 'tager_www.views.Buyer_identification'),
    url(r'^register/$', 'tager_www.views.UserRegistration'),
    url(r'^homepage/$', 'tager_www.views.get_channels'),
    url(r'^viewingPosts/$', 'tager_www.views.view_checked_subchannel_posts'),

    url(r'^facebook/login/$', 'tager_www.views.facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'tager_www.views.facebook_login_done', name="facebook_login_done"),

    url(r'^subscribe/$', 'tager_www.views.return_channels'),
    url(r'^notifications/$', 'tager_www.views.return_notification'),
    url(r'^subchannels_sub/$', 'tager_www.views.return_subchannels'),
    url(r'^parameters_sub/$', 'tager_www.views.return_parameters'),
    url(r'^choices_sub/$', 'tager_www.views.return_choices'),
    url(r'^subscription_by_param/$', 'tager_www.views.subscribe_by_parameters'),
    url(r'^subscription_by_subchann/$', 'tager_www.views.subscription_by_subchann'),
    url(r'^subscription_by_chann/$', 'tager_www.views.subscription_by_chann'),

    url(r'^confirm_email/$','tager_www.views.confirm_email'),
    url(r'^profile/$', 'tager_www.views.view_profile'),
    url(r'^post/$', 'tager_www.views.view_post'),
    url(r'^rateUser/$', 'tager_www.views.User_Ratings'),
    url(r'^advanced_att/$','tager_www.views.get_attributes_of_subchannel'),
    url(r'^advanced_subchannel/$','tager_www.views.advanced_view_subchannels'),
    url(r'^advanced_search/channel/$','tager_www.views.advanced_view_channels'),
    url(r'^advanced_search/$','tager_www.views.advanced_search'),
    url(r'^viewsubchannels', 'tager_www.views.view_subchannels', name='index'),
    url(r'^viewchannels$', 'tager_www.views.view_channels', name='index'),
    url(r'^addpost$', 'tager_www.views.add_post', name='post_create'),
    url(r'^showpost$', 'tager_www.views.view_post', name='view post'),
    url(r'^viewsubchannels/$', 'tager_www.views.view_subchannels', name='index'),
    url(r'^viewchannels/$', 'tager_www.views.view_channels', name='index'),
    url(r'^addpost/$', 'tager_www.views.add_post', name='post_create'),
    url(r'^showpost/$', 'tager_www.views.view_post', name='view post'),
    url(r'^thankyou/$','tager_www.views.thankyou'),
    url(r'^search/$', 'tager_www.views.search', name='search'),
    url(r'^search_results/$', 'tager_www.views.search'),
    



    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)