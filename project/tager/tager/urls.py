from django.conf.urls import patterns, include, url
from django.contrib.auth.views import logout, login
from tager_www.views import *



# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',

    url(r'^social_login/$','tager_www.views.social_login'),  
    url(r'^logout/$', logout, {'next_page':'/main'}),  
    url(r'^logout/$', logout, {'next_page':'/login'}),  
    url(r'^profile/$', 'tager_www.views.view_profile'),

              
    url(r'^editposttitle/$', 'tager_www.views.edit_post_title'),
    url(r'^editpostprice/$', 'tager_www.views.edit_post_price'),
    url(r'^editpostdescription/$', 'tager_www.views.edit_post_description'),
    url(r'^editpostlocation/$', 'tager_www.views.edit_post_location'),
    url(r'^editpost/$', 'tager_www.views.edit_post'),
    url(r'^editpostattribute/$', 'tager_www.views.edit_post_attribute'),

    url(r'^removepostfromwishlist$', 'tager_www.views.remove_post_from_wishlist'),
    url(r'^logout/$', logout, {'next_page':'/'}),  
    url(r'^$', 'tager_www.views.home'),
    url(r'^main$', 'tager_www.views.main'),
    url(r'^addtomylist$', 'tager_www.views.add_to_wish_list'),  
    url(r'^intrested/$', 'tager_www.views.intrested'),   
    # url(r'^intrested/$', 'tager_www.views.intrested'),  

    url(r'^editing_pic/$', 'tager_www.views.editing_pic'),
    url(r'^emptywishlist/$', 'tager_www.views.empty_wish_list'),
    url(r'^edit_pic/$', 'tager_www.views.editing_pic'),
    url(r'^edit_name/$', 'tager_www.views.edit_name'),
    url(r'^edit_dob/$', 'tager_www.views.edit_date_of_birth'),
    url(r'^edit_work/$', 'tager_www.views.edit_work'),
    url(r'^edit_phone/$', 'tager_www.views.edit_phone'),  
    url(r'^private/$', 'tager_www.views.view_private'), 
    url(r'^private_number/$', 'tager_www.views.private_number'),
    url(r'^private_work/$', 'tager_www.views.private_work'),
    url(r'^public_number/$', 'tager_www.views.public_number'),
    url(r'^public_work/$', 'tager_www.views.public_work'),
    url(r'^edit_work/$', 'tager_www.views.edit_work'), 

    url(r'^account/$', 'tager_www.views.return_account_type'),
    url(r'^change_faccount/$', 'tager_www.views.change_faccounttype'),
    url(r'^change_paccount/$', 'tager_www.views.change_paccounttype'),

    url(r'^report/$', 'tager_www.views.report_the_post', name='reportThePost'),
    url(r'^login/$', 'tager_www.views.view_login'),
    url(r'^logged/$', 'tager_www.views.login'),
    url(r'^addBuyer/$', 'tager_www.views.Buyer_identification'),
    url(r'^register/$', 'tager_www.views.UserRegistration'),
 
    url(r'^viewingPosts/$', 'tager_www.views.view_checked_subchannel_posts'),

    url(r'^updatestatus/$', 'tager_www.views.update_status'),

    url(r'^menu_posts/$', 'tager_www.views.menuForSubchannels'),
    url(r'^channel_posts/$', 'tager_www.views.postsToChannels'),
    


    url(r'^facebook/login/$', 'tager_www.views.facebook_login', name="facebook_login"),
    url(r'^facebook/login/done/$', 'tager_www.views.facebook_login_done', name="facebook_login_done"),
    url(r'^subscribe/$', 'tager_www.views.return_channels'),
    url(r'^notifications/$', 'tager_www.views.return_notification'),
    url(r'^subchannels_sub/$', 'tager_www.views.return_subchannels'),
    url(r'^parameters_sub/$', 'tager_www.views.return_parameters'),
    url(r'^choices_sub/$', 'tager_www.views.return_choices'),
    url(r'^subscription_by_param/$', 'tager_www.views.subscribe_by_parameters'),
    url(r'^subscription_by_subchann/$', 'tager_www.views.subscription_by_subchann'),
    url(r'^subscription_by_chann/$', 'tager_www.views.subscription_by_chann'),
    url(r'^confirm_email/$','tager_www.views.confirm_email'),
    url(r'^profile/$', 'tager_www.views.view_profile'),
    url(r'^post/$', 'tager_www.views.view_post'),
    url(r'^rateUser/$', 'tager_www.views.User_Ratings'),
    url(r'^advanced_att/$','tager_www.views.get_attributes_of_subchannel'),
    url(r'^advanced_subchannel/$','tager_www.views.advanced_view_subchannels'),
    url(r'^advanced_subchannel_show/$','tager_www.views.advanced_render_subchannels'),
    url(r'^advanced_search/channel/$','tager_www.views.advanced_view_channels'),
    url(r'^advanced_search/channel_show/$','tager_www.views.advanced_render_channels'),
    url(r'^advanced_search/$','tager_www.views.advanced_search'),
    url(r'^viewsubchannels', 'tager_www.views.view_subchannels', name='index'),
    url(r'^viewchannels$', 'tager_www.views.view_channels', name='index'),
    url(r'^addpost$', 'tager_www.views.add_post', name='post_create'),
    url(r'^showpost$', 'tager_www.views.view_post', name='view post'),
    url(r'^thankyou/$','tager_www.views.thankyou'),
    url(r'^search/$', 'tager_www.views.search', name='search'),
    url(r'^search_results/$', 'tager_www.views.search'),
    url(r'^addComment/(?P<post_id>\d+)/$', 'tager_www.views.SavingComment', name="adingcomment"),
    url(r'^user_activity/$', 'tager_www.views.all_log'),
    url(r'^all_log/$', 'tager_www.views.all_log'),
    url(r'^all_log_post/$', 'tager_www.views.all_log_post'),
    url(r'^all_log_wish/$', 'tager_www.views.all_log_wish'),
    url(r'^all_log_interested/$', 'tager_www.views.all_log_interested'),
    url(r'^all_log_profile/$', 'tager_www.views.all_log_profile'),
    url(r'^all_log_wish/$', 'tager_www.views.all_log_wish'),
    url(r'^send_phone/$', 'tager_www.views.sms'),
    url(r'^send_sms/$', 'tager_www.views.sms_verify'),
    url(r'^refresh_notifications/$', 'tager_www.views.unread_notifications'),
    url(r'^deletepost/$', 'tager_www.views.hide_post'),

    # Examples:
    # url(r'^$', 'tager.views.home', name='home'),
    # url(r'^tager/', include('tager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
)


urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
