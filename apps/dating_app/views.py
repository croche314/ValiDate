from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse, resolve
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from itertools import chain
from urlparse import urlparse
from django.db.models import Q
from .models import *
import bcrypt, re
import json
import urllib2

from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Login and Registration
def index(request):
	if 'username' in request.session:
		print '-' * 50
		print 'session:'
		print '[username]:',request.session['username']
		print '[user_id]:',request.session['user_id']
		print '-' * 50
	else:
		print '-' * 50
		print 'no user logged in'
		print '-' * 50
	return render(request, 'dating_app/login.html')

def create_user(request):
	# Create a new User using html form inputs from Index(login.html)
	server_name = request.POST['html_name']
	server_username = request.POST['html_username']
	server_email = request.POST['html_email']
	emailValid = re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',server_email)
	server_age = request.POST['html_age']
	server_password = request.POST['html_password']
	server_confirm_pw = request.POST['html_confirm_password']

	# Validate user input
	if len(server_name)<1 or len(server_username)<1 or len(server_email)<1 or len(server_age)<1 or len(server_password)<1 or len(server_confirm_pw)<1:
		messages.warning(request,'Please make sure no fields are blank')
		return redirect('dating:index')
	elif len(server_password)<6:
		messages.warning(request, 'password must be at least 6 characters')
		return redirect('dating:index')
	elif emailValid == None:
		messages.warning(request, 'invalid email format')
		return redirect('dating:index')
	elif server_password != server_confirm_pw:
		messages.warning(request,'passwords must match')
		return redirect('dating:index')
	else:
		# If valid, create new user
		try:
			hashed_pw = bcrypt.hashpw(server_password.encode("UTF-8"),bcrypt.gensalt())
			print '-' * 50
			print 'hashed pword successfully:', hashed_pw
			print '-' * 50
			new_user = User.objects.create(name=server_name,username=server_username,email=server_email,age=server_age,password=hashed_pw)
			default_pic = Image.objects.create(user=new_user,user_pic='img/user.png')
			print '-' * 50
			print 'created user successfully'
			print '-' * 50
			request.session['user_id'] = new_user.id
			request.session['username'] = server_username
			request.session['name'] = server_name

			# If creation successful, redirect to Home page
			return redirect('dating:display_questions')

		except:
			print '-' * 50
			print 'error hashing password or creating user'
			print '-' * 50
			messages.warning(request, 'hashing password or creating user')
			# If unsuccessful, redirect back to index, display errors
			return redirect('dating:questions')

def login_user(request):
	# If login fields match a User, insert session info, and redirect to Home page
	server_email = request.POST['html_email']
	server_password = request.POST['html_password']

	# Validate user input
	if len(server_email)<1 or len(server_password)<1:
		messages.warning(request, 'both login fields are required')
		return redirect('dating:index')
	elif len(server_password)<6:
		messages.warning(request, 'password must be at least 6 characters')
		return redirect('dating:index')
	else:
		# If valid, search the database for user
		try:
			this_user = User.objects.get(email=server_email)
			print '-' * 50
			print 'password',this_user.password
			print '-' * 50
			if this_user.password == bcrypt.hashpw(server_password.encode("UTF-8"),this_user.password.encode("UTF-8")):
				request.session['user_id'] = this_user.id
				request.session['username'] = this_user.username
				print '-' * 50
				print 'Login successful!'
				print 'CURRENT USER'
				print 'id:',request.session['user_id']
				print 'username:',request.session['username']
				print '-' * 50

				return redirect('dating:home')

			else: # email found but password does not match that email
				messages.warning(request, 'invalid password, try again')

				return redirect('dating:index')
		except: # no email matches what the user submitted
			messages.warning(request, 'user not found')

			return redirect('dating:index')

# Home Page
def home(request):
	print '-' * 50
	print 'CURRENT SESSION'
	print '[username]:',request.session['username']
	print '[user_id]:',request.session['user_id']
	print '-' * 50
	all_pics = Image.objects.filter(profile_pic=True)
	pic_dict = {}
	context = {
		'match': Match.objects.filter(user1_id = request.session['user_id']),
		'match2': Match.objects.filter(user2_id=request.session['user_id']),
		'all_users': User.objects.exclude(id=request.session['user_id']),
		'all_pics': all_pics,
	}

	return render(request, 'dating_app/home.html', context)

def logout(request):
	request.session.clear()
	return redirect('dating:index')

def show_user(request,user_id):
	this_user = User.objects.get(id=user_id)
	my_answers = Answer.objects.get(user_id=this_user.id)
	profile_pic = ""
	try: # find user's profile pic
		profile_pic_url = this_user.profile_pic_url
	except: # If no profile pic is found for this user, default image is shown
		profile_pic_url = 'img/user.png'
	try:
		like = Like.objects.get(like1_id=request.session['user_id'], like2_id=user_id)
	except:
		like = False
	my_likes = Like.objects.filter(like1_id=request.session['user_id'])

	# Gather all gallery pictures
	my_gallery = Image.objects.filter(user_id=this_user.id)
	context = {
		'user': this_user,
		'answers': my_answers,
		'like': like,
		'my_like': my_likes,
		'profile_pic': profile_pic_url,
		'my_gallery': my_gallery
	}
	return render(request, 'dating_app/show_user.html', context)

def edit_user(request,user_id):
	print 'user_id:',user_id
	print 'session[user_id]:',request.session['user_id']
	if str(user_id) != str(request.session['user_id']):
		messages.warning(request, 'You do not have permission to edit another user')
		return redirect('dating:home')
	else:
		this_user = User.objects.get(id=request.session['user_id'])
		my_answers = Answer.objects.get(user_id=this_user.id)
		context = {
			'user': this_user,
			'answers': my_answers
		}
		return render(request, 'dating_app/edit_user.html', context)

def update_user(request, answer_id):
	name = request.POST['html_name']
	username = request.POST['html_username']
	age = request.POST['html_age']
	gender = request.POST['html_gender']
	feet = request.POST['html_feet']
	inches = request.POST['html_inches']
	height = float(feet) + float(inches)/12
	language = request.POST['html_language']
	stack = request.POST['html_stack']
	religion = request.POST['html_religion']
	smoke = request.POST['html_smoke']
	body = request.POST['html_body_type']
	ethnicity  = request.POST['html_ethnicity']
	children = request.POST['html_wants_children']
	about_you = request.POST['html_about_you']

	# If any fields are blank, send back to edit_user
	if len(gender)<1 or len(str(height))<1 or len(language)<1 or len(stack)<1 or len(religion)<1 or len(smoke)<1 or len(body)<1 or len(ethnicity)<1 or len(children)<1 or len(about_you)<1:
		messages.warning(request, 'Make sure all fields are filled in')
		return redirect('dating:edit_user')
	else: # If valid, update answers
		Answer.objects.filter(id=answer_id).update(gender=gender,height=height, feet=feet, inches=inches,language=language,stack=stack,religion=religion,smoke=smoke,body_type=body,ethnicity=ethnicity,wants_children=children,about_you=about_you)
		User.objects.filter(id=request.session['user_id']).update(name=name,username=username,age=age)
		messages.success(request, 'Answers updated!')
		Match.objects.filter(user1_id=request.session['user_id']).delete()
		Match.objects.filter(user2_id=request.session['user_id']).delete()
		user = Answer.objects.get(id=request.session['user_id'])
		answer_exclude = Answer.objects.exclude(id=request.session['user_id'])
		user1zip = user.zip_code
		for ans in answer_exclude:
			counter = 0
			user2zip = ans.zip_code
			distance = find_distance(user1zip,user2zip)
			if ans.gender != user.gender:
				if ans.height > (user.height-10) and ans.height < (user.height-10):
					counter += 2
				if ans.zip_code == user.zip_code:
					counter += 3
				if distance <= 5:
					counter += 4
				if distance > 5:
					counter = counter - 1
				if ans.stack == user.stack:
					counter += 2
				if ans.religion == user.religion:
					counter += 3
				if ans.smoke == user.smoke:
					counter += 1
				if ans.body_type == user.body_type:
						counter += 3
				if ans.wants_children == user.wants_children:
					counter += 2
				if counter > 5:
					percent_match= (float(counter)/12)*100
					int(percent_match)
					Match.objects.create(user1_id = user.id, user2_id =ans.id, percent_match=percent_match)
		return redirect(reverse('dating:show_user',kwargs={'user_id': request.session['user_id']}))



def display_questions(request):
	return render(request, 'dating_app/questionaire.html')

def questions(request):
	gender = request.POST['html_gender']
	feet = request.POST['html_feet']
	inches = request.POST['html_inches']
	try:
		height = float(feet) + float(inches)/12
	except:
		messages.warning(request, 'Must include a height')
		return redirect('dating:display_questions')
	language = request.POST['html_language']
	stack = request.POST['html_stack']
	religion = request.POST['html_religion']
	zipcode = request.POST['html_zip_code']
	smoke = request.POST['html_smoke']
	body = request.POST['html_body_type']
	ethnicity  = request.POST['html_ethnicity']
	children = request.POST['html_wants_children']
	about_you = request.POST['html_about_you']
	if len(language)<1 or len(stack)<1 or len(religion)<1 or len(smoke)<1 or len(body)<1 or len(ethnicity)<1 or len(children)<1 or len(about_you)<1:
		messages.warning(request, 'Make sure all fields are filled in')
		return redirect('dating:display_questions')
	Answer.objects.create(gender=gender, height=height, language=language, stack=stack, religion=religion, zip_code=zipcode, smoke=smoke, body_type=body, ethnicity=ethnicity, wants_children=children,user_id=request.session['user_id'], about_you=about_you, feet=feet, inches=inches)
	return redirect('dating:edit_preference')

def find_matches(request):
	try:
		Match.objects.filter(user1_id=request.session['user_id']).delete()
	except:
		pass
	preference = Preference.objects.get(user_id=request.session['user_id'])
	print "+++++++++++++++++++"
	print preference
	print "+++++++++++++++++++"
	user = Answer.objects.get(id=request.session['user_id'])
	answer_exclude = Answer.objects.exclude(id=request.session['user_id'])
	user1zip = user.zip_code
	print "+++++++++++++++++++++"
	print preference.gender
	print "+++++++++++++++++++++"
	for ans in answer_exclude:
		counter = 0
		user2zip = ans.zip_code
		distance = find_distance(user1zip,user2zip)
		if ans.gender == preference.gender:
			if ans.height > (preference.height-10) and ans.height < (preference.height-10):
				counter += 2
			if distance <= 5:
				counter += 4
			if distance > 5:
				counter = counter - 1
			if ans.stack == preference.stack:
				counter += 2
			if ans.religion == preference.religion:
				counter += 3
			if ans.smoke == preference.smoke:
				counter += 3
			if ans.body_type == preference.body_type:
				counter += 3
			if ans.wants_children == preference.wants_children:
				counter += 1
			if counter > 8:
				percent_match= (float(counter)/15)*100
				int(percent_match)
				Match.objects.create(user1_id = user.id, user2_id =ans.id, percent_match=percent_match)
				print counter
				print str(percent_match) +"-------------"
 	return redirect('dating:home')

def find_distance(user1zip,user2zip):
	url = 'https://www.zipcodeapi.com/rest/GoVJDjzV4jOwn0efU8t0LMQUNMYZUp8BN4kqnTmrdbYAbcP5li675W1SJ0REp0fd/distance.json/'+str(user1zip)+'/'+str(user2zip)+'/mile'
	#data = json.load(urllib2.urlopen(url))
	#return data['distance']
	return 4.0

def upload_pic(request):
	user_id = request.session['user_id']
	this_user = User.objects.get(id=user_id)

	if 'image' in request.FILES:
		image = request.FILES['image']
		try:
			new_image = Image.objects.create(user_id=request.session['user_id'], user_pic=image,profile_pic=False)
			this_user.profile_pic_url = new_image.user_pic
			messages.success(request, 'Photo uploaded!')
			return redirect(reverse('dating:show_user',kwargs={'user_id':request.session['user_id']}))
		except:
			messages.warning(request, 'Photo not uploaded, try again')
			return redirect(reverse('dating:show_user',kwargs={'user_id':request.session['user_id']}))
	else:
		messages.warning(request, 'No image found, try again')
		return redirect(reverse('dating:show_user',kwargs={'user_id':request.session['user_id']}))

def delete_pic(request,image_id):
	this_user = User.objects.get(id=request.session['user_id'])
	this_pic = Image.objects.get(id=image_id)
	if this_pic.user_pic == this_user.profile_pic_url:
		this_user.profile_pic_url = 'img/user.png'
	this_pic.delete()

	new_pic = Image.objects.filter(user_id=this_user.id)

	if len(new_pic) > 0:
		new_pic[0].profile_pic = True
		new_pic[0].save()
	messages.success(request, 'Image deleted!')
	return redirect(reverse('dating:show_user',kwargs={'user_id':this_user.id}))


def change_profile_pic(request,image_id):
	this_user = User.objects.get(id=request.session['user_id'])
	this_pic = Image.objects.get(id=image_id)
	original_profile = Image.objects.filter(user_id=this_user.id).filter(profile_pic=True)

	if len(original_profile) > 0:
		original_profile = original_profile[0]
		original_profile.profile_pic=False
		original_profile.save()

	this_user.profile_pic_url = this_pic.user_pic
	print 'this_user.profiile_pic_url',this_user.profile_pic_url
	this_user.save()
	this_pic.profile_pic = True
	this_pic.save()

	return redirect(reverse('dating:show_user',kwargs={'user_id':this_user.id}))


def new_message(request,receiver_id):
	this_user = User.objects.get(id=request.session['user_id'])
	receiver = User.objects.get(id=receiver_id)
	my_conversations_with_this_user = Conversation.objects.filter(user1=this_user.id).filter(user2=receiver_id) | Conversation.objects.filter(user2=this_user.id).filter(user1=receiver_id)
	if len(my_conversations_with_this_user) == 0:
		new_conversation = Conversation.objects.create(user1=this_user,user2=receiver)
		conversation_id = new_conversation.id
		context = {
			'receiver': receiver,
			'conversation_id': conversation_id
		}
		return render(request, 'new_message.html', context)
	else:
		return redirect(reverse('dating:show_my_messages', kwargs={'user_id':this_user.id}))
		


def create_message(request,receiver_id,conversation_id):
	sender = User.objects.get(id=request.session['user_id'])
	receiver = User.objects.get(id=receiver_id)
	message_text = request.POST['html_message_text']

	new_message = Message.objects.create(sender=sender, receiver=receiver, text=message_text,conversation_id=conversation_id)

	return redirect(reverse('dating:show_my_messages', kwargs={'user_id':sender.id}))

def show_my_messages(request,user_id):
	this_user = User.objects.get(id=user_id)
	sent_messages = Message.objects.filter(sender_id=user_id).order_by('-created_at')
	received_messages = Message.objects.filter(receiver_id=user_id).order_by('-created_at')
	all_my_messages = list(chain(sent_messages,received_messages))
	
	user1_converations = Conversation.objects.filter(user1=this_user.id)
	user2_conversations = Conversation.objects.filter(user2=this_user.id)
	all_my_conversations = list(chain(user1_converations,user2_conversations))

	print '-' * 50
	print 'all of my conversations:',all_my_conversations
	print '-' * 50 
	all_messages = {}

	for conversation in all_my_conversations:
		messages_in_this_conversation = Message.objects.filter(conversation_id=conversation.id)
		all_messages[conversation.id] = messages_in_this_conversation
	print all_messages
		# for message in messages_in_this_conversation:
		# 	print conversation.id
		# 	print message.sender.username
		# 	print message.text
	context = {
		'all_my_messages': all_my_messages,
		'all_my_conversations': all_my_conversations,
		'all_messages': all_messages
	}
	return render(request, 'dating_app/my_messages.html', context)

def like_user(request, user_id):
	current_url = request.META['HTTP_REFERER']
	o = urlparse(current_url).path
	like1 = request.session['user_id']
	like2 = user_id
	Like.objects.create(like1_id=like1, like2_id=like2)
	return redirect(o)

def unlike_user(request, user_id):
	current_url= request.META['HTTP_REFERER']
	o = urlparse(current_url).path
	like1 = request.session['user_id']
	like2 = user_id
	Like.objects.filter(like1_id=like1, like2_id=like2).delete()
	return redirect(o)

def preference(request):
	try:
		Preference.objects.filter(user_id=request.session['user_id']).delete()
	except:
		pass
	gender = request.POST['html_gender']
	feet = request.POST['html_feet']
	inches = request.POST['html_inches']
	try:
		height = float(feet) + float(inches)/12
	except:
		messages.warning(request, 'Must include a height')
		return redirect('dating:display_questions')
	language = request.POST['html_language']
	stack = request.POST['html_stack']
	religion = request.POST['html_religion']
	zipcode = request.POST['html_zip_code']
	smoke = request.POST['html_smoke']
	body = request.POST['html_body_type']
	ethnicity  = request.POST['html_ethnicity']
	children = request.POST['html_wants_children']
	if len(language)<1 or len(stack)<1 or len(religion)<1 or len(smoke)<1 or len(body)<1 or len(ethnicity)<1 or len(children)<1:
		messages.warning(request, 'Make sure all fields are filled in')
		return redirect('dating:display_questions')
	Preference.objects.create(gender=gender, height=height, language=language, stack=stack, religion=religion, zip_code=zipcode, smoke=smoke, body_type=body, ethnicity=ethnicity, wants_children=children,user_id=request.session['user_id'], feet=feet, inches=inches)
	return redirect('dating:find_matches')

def edit_preference(request):
	return render(request, 'dating_app/preference.html')

def delete_message(request,message_id):
	this_message = Message.objects.get(id=message_id)
	this_message.delete()
	messages.success(request, 'Message deleted!')
	return redirect(reverse('dating:show_my_messages', kwargs={'user_id':request.session['user_id']}))

def search_query(request):
	pass
