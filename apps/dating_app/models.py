from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=50)
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=200)
	age = models.IntegerField()
	account_active = models.BooleanField(default=True)
	profile_pic_url = models.FileField(upload_to='img',default='img/user.png')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Answer(models.Model):
	gender = models.CharField(max_length=10)
	height = models.FloatField()
	feet = models.IntegerField()
	inches = models.IntegerField()
	language = models.CharField(max_length=10)
	zip_code = models.IntegerField()
	stack = models.CharField(max_length=15)
	religion = models.CharField(max_length=10)
	smoke = models.BooleanField(default=False)
	body_type = models.CharField(max_length=20)
	ethnicity = models.CharField(max_length=20)
	wants_children = models.BooleanField()
	about_you = models.TextField(max_length=1000)
	user = models.OneToOneField(User, related_name='my_answers')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Preference(models.Model):
	gender = models.CharField(max_length=10)
	height = models.FloatField()
	feet = models.IntegerField()
	inches = models.IntegerField()
	language = models.CharField(max_length=10)
	zip_code = models.IntegerField()
	stack = models.CharField(max_length=15)
	religion = models.CharField(max_length=10)
	smoke = models.BooleanField(default=False)
	body_type = models.CharField(max_length=20)
	ethnicity = models.CharField(max_length=20)
	wants_children = models.BooleanField()
	about_you = models.TextField(max_length=1000)
	user = models.OneToOneField(User, related_name='my_preferences')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Match(models.Model):
	user1 = models.ForeignKey(User, related_name='my_match')
	user2 = models.ForeignKey(User, related_name='matched_me')
	percent_match = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
	user1 = models.ForeignKey(User, related_name='my_likes')
	user2 = models.ForeignKey(User, related_name='liked_me')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Conversation(models.Model):
	user1 = models.ForeignKey(User, related_name='my_conversation1')
	user2 = models.ForeignKey(User,related_name='my_conversation2')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
	conversation = models.ForeignKey(Conversation,related_name='messages')
	text = models.TextField(max_length=1000)
	sender = models.ForeignKey(User, related_name='my_sent')
	receiver = models.ForeignKey(User,related_name='my_received')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Image(models.Model):
	user = models.ForeignKey(User,related_name='my_pic')
	user_pic = models.FileField(upload_to='img',default='img/user.png')
	profile_pic = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
	like1 = models.ForeignKey(User, related_name='liker')
	like2 = models.ForeignKey(User, related_name='likee')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
