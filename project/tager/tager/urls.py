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
	# url(r'^tager_www/', include('tager_www.urls')),
    url(r'^advanced_att/$','tager_www.views.get_attributes_of_subchannel'),
    url(r'^advanced_subchannel/$','tager_www.views.advanced_view_subchannels'),
    url(r'^advanced_search/channel/$','tager_www.views.advanced_view_channels'),
    url(r'^advanced_search/$','tager_www.views.advanced_search'),
)


urlpatterns += patterns('fbregister.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
