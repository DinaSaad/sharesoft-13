from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fbapp/$', 'fbapp.views.index'),
)

urlpatterns += patterns('fbapp.facebook',
	url(r'^facebook/login/$', 'facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'facebook_login_done', name="facebook_login_done"),
)

urlpatterns += patterns('fbapp.views',
    url(r'^$', 'index', name="index"),
)