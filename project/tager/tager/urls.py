from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from django.contrib import admin
from tager_www import views


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

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
    url(r'^fbregister/$', 'fbregister.views.index'),
	# url(r'^tager_www/', include('tager_www.urls')),
    #url(r'^post/$', 'tager_www.views.commenting'),
    #url(r'^homepage/$', 'tager_www.views.get_channels'),
    #url(r'^homepage/$', 'tager_www.views.view_subchannel_posts'),
    # url(r'^post/$', 'tager_www.views.get_posts'),
    url(r'^post/(?P<post_id>\d+)/$', 'tager_www.views.viewPost'),
    url(r'^addComment/(?P<post_id>\d+)/$', 'tager_www.views.SavingComment', name='addComment'),
    url(r'^hideComment/(?P<post_id>\d+)/$', 'tager_www.views.removePost'),
#c1_hala_AddComment
#calling post with its id in the url of the host, to go to the method viewPost to execute the method
#calling addComment with post id in the url of the host , that calls the savingComment method in the views that
#named also adingcomment to call it in the tests.
#c1_hala_hideComment
#calling hideComment with post_id in the host , to go to the methos removePost.

    # url(r'^homepage/$', 'tager_www.views.get_posts'),
    # url(r'^homepage/$', 'tager_www.views.view_posts_comments'),
)
#####
urlpatterns += patterns('fbregister.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbregister.views',
    url(r'^$', 'index', name="index"),
)
