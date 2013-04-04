from django.conf.urls.defaults import *
from django.contrib.auth.views import login,
urlpatterns = patterns('tager_www.views',
 
    (r'^postid/$', 'search_postid'),
    (r'^comment/$', 'post_comment'),
    (r'^postcomment/$', 'login_view'),
    (r'^time/$', 'current_datetime'),
)