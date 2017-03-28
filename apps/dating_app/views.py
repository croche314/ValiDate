from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *
import bcrypt, re

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

	return render(request, 'dating_app/home.html')

def logout(request):
	request.session.clear()
	return redirect('dating:index')

def show_user(request,user_id):
	this_user = User.objects.get(id=request.session['user_id'])
	my_answers = Answer.objects.get(user_id=this_user.id)
	
	context = {
		'user': this_user,
		'answers': my_answers
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

def update_user(request, user_id):
	pass

def display_questions(request):
	return render(request, 'dating_app/questionaire.html')

def questions(request):
	gender = request.POST['html_gender']
	height = request.POST['html_height']
	language = request.POST['html_language']
	stack = request.POST['html_stack']
	religion = request.POST['html_religion']
	zipcode = request.POST['html_zip_code']
	smoke = request.POST['html_smoke']
	body = request.POST['html_body_type']
	ethnicity  = request.POST['html_ethnicity']
	children = request.POST['html_wants_children']
	about_you = request.POST['html_about_you']
	Answer.objects.create(gender=gender, height=height, language=language, stack=stack, religion=religion, zip_code=zipcode, smoke=smoke, body_type=body, ethnicity=ethnicity, wants_children=children,user_id=request.session['user_id'], about_you=about_you)
	return redirect('dating:find_matches')

def find_matches(request):
	user = Answer.objects.get(id=request.session['user_id'])
	answer_exclude = Answer.objects.exclude(id=request.session['user_id'])
	print "++++++++++++++++++++++++++++++++++++"
	print user.language
	print len(answer_exclude)
	for ans in answer_exclude:
		counter = 0
		if ans.gender != user.gender:
			if ans.height > (user.height-300) and ans.height < (user.height-300):
				counter += 1
			if ans.zip_code == user.zip_code:
				counter += 1
			if ans.stack == user.stack:
				counter += 2
			if ans.religion == user.religion:
				counter += 3
			if ans.smoke == user.smoke:
				counter += 1
			if ans.body_type == user.body_type:
				counter += 3
			if ans.wants_children == user.wants_children:
				counter += 1
			if counter > 7:
				Match.objects.create(user1 = request.session['user_id'], user2=ans.id)
	print "++++++++++++++++++++++++++++++++++++"
 	return redirect('dating:home')