from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^/$', 'doList.views.home', name='home'),
    url(r'^delete/ToDoList/$', 'doList.views.create_guestbook', name='deleteList'),
    url(r'^/ToDoList/TaskDone$', 'doList.views.task_done', name='tasksDone'),
)