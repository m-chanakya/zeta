from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from users.models import *

import json
from django.http import HttpResponse

@login_required()
def home(request):
	return render(request,"home.html")

@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, 'msg' : "User account created successfully"}
		name = data.get('name', False)
		mobile = data.get('mobile', False)
		if name and mobile:
			user = User(username = name)
			password = User.objects.make_random_password()
			user.set_password(password)
			try:
				user.save()
			except Exception as e:
				user = False
				response['status'] = 1
				response['msg'] = "Username not unique"
			if user:
				try:
					profile = Profile.objects.create(user = user, mobile_number = mobile)
				except Exception as e:
					print e
					response['status'] = 1
					response['msg'] = "Mobile number is incorrect"
		else:
			response['status'] = 1
			response['msg'] = "Username or Mobile number was not entered"
		return HttpResponse(json.dumps(response), content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def change_password(request):
	pass

@user_passes_test(lambda u: u.is_superuser)
def change_pin(request):
	pass

@user_passes_test(lambda u: u.is_superuser)
def lock(request):
	pass

@user_passes_test(lambda u: u.is_superuser)
def send_amount(request):
	pass

@user_passes_test(lambda u: u.is_superuser)
def history(request):
	pass
