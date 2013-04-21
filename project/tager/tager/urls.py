from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', 'tager_www.views.home'),
    url(r'^login/$', 'tager_www.views.view_login'),
    url(r'^logged/$', 'tager_www.views.login'),
    url(r'^logout/$', logout, {'next_page':'/'}),  
    url(r'^register/$', 'tager_www.views.UserRegistration'),
    url(r'^confirm_email/$','tager_www.views.confirm_email'),
    url(r'^profile/$', 'tager_www.views.view_profile'),
    url(r'^post/$', 'tager_www.views.view_post'),
    url(r'^rateUser/$', 'tager_www.views.User_Ratings'),
    url(r'^facebook/login/$', 'tager_www.views.facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'tager_www.views.facebook_login_done', name="facebook_login_done"),

    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fbregister/$', 'fbregister.views.index'),
)

urlpatterns += patterns('tager_www.facebook',
	# url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
 #    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
