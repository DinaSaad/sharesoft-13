from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from django.contrib import admin
from tager_www import views
# admin.autodiscover()

urlpatterns = patterns('',
    

    url(r'^$', 'tager_www.views.home'),
    url(r'^main$', 'tager_www.views.main'),
    url(r'^intrested/$', 'tager_www.views.intrested', name="intrested"),  
    url(r'^report/$', 'tager_www.views.report_the_post', name='reportThePost'),
    url(r'^getInterestedIn/$', 'tager_www.views.get_interested_in', name='getInterestedIn'),
    url(r'^login/$', 'tager_www.views.view_login'),
    url(r'^logged/$', 'tager_www.views.login'),
    url(r'^logout/$', logout, {'next_page':'/'}),  
    url(r'^addBuyer/$', 'tager_www.views.Buyer_identification'),
    url(r'^register/$', 'tager_www.views.UserRegistration'),
    url(r'^confirm_email/$','tager_www.views.confirm_email'),
    url(r'^profile/$', 'tager_www.views.view_profile'),
    url(r'^post/$', 'tager_www.views.view_post'),
    url(r'^rateUser/$', 'tager_www.views.User_Ratings'),
    url(r'^viewsubchannels/$', 'tager_www.views.view_subchannels', name='index'),
    url(r'^viewchannels/$', 'tager_www.views.view_channels', name='index'),
    url(r'^addpost/$', 'tager_www.views.add_post', name='post_create'),
    url(r'^showpost/$', 'tager_www.views.view_post', name='view post'),
    url(r'^thankyou/$','tager_www.views.thankyou'),
    url(r'^tager_www/', include('tager_www.urls')),
    url(r'^post/(?P<post_id>\d+)/$', 'tager_www.views.viewPost'),
    url(r'^addComment/(?P<post_id>\d+)/$', 'tager_www.views.SavingComment', name="adingcomment"),
    url(r'^hideComment/(?P<post_id>\d+)/$', 'tager_www.views.removePost'),


    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fbregister/$', 'fbregister.views.index'),
)

urlpatterns += patterns('fbregister.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
