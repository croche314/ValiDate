from django.conf.urls import url
from views import *

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^create_user$',create_user,name='create_user'),
	url(r'^login_user$',login_user,name='login_user'),
	url(r'^home$',home,name='home'),
	url(r'^logout$',logout,name='logout'),
	url(r'^show_user/(?P<user_id>\d+)$',show_user, name='show_user'),
	url(r'^edit_user/(?P<user_id>\d+)$',edit_user, name='edit_user'),
	url(r'^update_user/(?P<answer_id>\d+)$',update_user, name='update_user'),
	url(r'display_questions$',display_questions,name='display_questions'),
	url(r'^questions$',questions,name='questions'),
	url(r'^find_matches$',find_matches,name='find_matches'),
	url(r'^upload_pic$',upload_pic,name='upload_pic'),
	url(r'^new_message/(?P<receiver_id>\d+)$',new_message, name='new_message'),
	url(r'^create_message/(?P<receiver_id>\d+)$',create_message,name='create_message'),
	url(r'^show_my_messages/(?P<user_id>\d+)$',show_my_messages,name='show_my_messages'),
	url(r'^like_user/(?P<user_id>\d+)$',like_user,name='like_user'),
	url(r'^unlike_user/(?P<user_id>\d+)$',unlike_user,name='unlike_user'),
	url(r'^preference$',preference, name='preference'),
	url(r'^edit_preference$',edit_preference, name='edit_preference'),
	url(r'^delete_message/(?P<message_id>\d+)$',delete_message,name='delete_message'),
	url(r'^delete_pic/(?P<image_id>\d+)$',delete_pic,name='delete_pic'),
	url(r'^change_profile_pic/(?P<image_id>\d+)$',change_profile_pic,name='change_profile_pic'),



]
