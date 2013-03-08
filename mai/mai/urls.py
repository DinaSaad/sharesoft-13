from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^login/$', 'auth.views.login_user'),
    # Examples:
    # url(r'^$', 'mai.views.home', name='home'),
    # url(r'^mai/', include('mai.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
