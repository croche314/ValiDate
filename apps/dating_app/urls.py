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
	url(r'^match_show/(?P<user_id>\d+)$', match_show, name='match_show'),
	url(r'^update_user/(?P<user_id>\d+)$',update_user, name='update_user'),
	url(r'display_questions$',display_questions,name='display_questions'),
	url(r'^questions$',questions,name='questions'),
	url(r'^find_matches$',find_matches,name='find_matches')
]
