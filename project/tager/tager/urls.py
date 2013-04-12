from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'tager_www.views.home'),
    url(r'^login/$', 'tager_www.views.login'),  
    url(r'^logout/$', logout, {'next_page':'/login'}),  


    url(r'^editing/$', 'tager_www.views.editing_info'),
    url(r'^updating/$', 'tager_www.views.update_status'),
    url(r'^register/$', 'tager_www.views.UserRegistration'),
    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    
    # url(r'^resetpassword/$', 'tager_www.views.password_reset')
    # url(r'^resetpassword/passwordsent/$', 'tager_www.views.password_reset_done')
    # url(r'^resetpassword/done/$', 'tager_www.views.password_reset_complete')
    # url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'tager_www.views.password_reset_confirm')


    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fbregister/$', 'fbregister.views.index'),
	url(r'^tager_www/', include('tager_www.urls')),
)

urlpatterns += patterns('fbregister.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
