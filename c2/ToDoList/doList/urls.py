from django.conf.urls import patterns, url

from doList import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)