from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'tager_www.views.home'),
    url(r'^login/$', 'tager_www.views.login'),  
    url(r'^logout/$', logout, {'next_page':'/login'}),  

    url(r'^register/$', 'tager_www.views.UserRegistration'),
    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fbregister/$', 'fbregister.views.index'),
    url(r'^subscribe/$', 'tager_www.views.return_channels'),
    url(r'^notifications/$', 'tager_www.views.return_notification'),
    url(r'^subscribe/subchannels_sub/$', 'tager_www.views.return_subchannels'),
    url(r'^subscribe/subchannels_sub/parameters_sub/$', 'tager_www.views.return_parameters'),
    url(r'^subscribe/subchannels_sub/parameters_sub/choices_sub/$', 'tager_www.views.return_choices'),
    url(r'^subscribe/subchannels_sub/parameters_sub/choices_sub/subscription_by_param', 'tager_www.views.subscribe_by_parameters'),
    url(r'^subscribe/subchannel_sub/subscription_by_subchann/$', 'tager_www.views.subscription_by_subchann'),
    url(r'^subscribe/subscription_by_chann/$', 'tager_www.views.subscription_by_chann'),
)

urlpatterns += patterns('fbregister.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
