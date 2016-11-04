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
		response['data'] = {}
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
					response['data']['username'] = user.username
					response['data']['mobile'] = profile.mobile_number
					response['data']['id'] = user.id
					response['data']['password'] = password
					response['data']['pin'] = profile.pin
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
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, 'msg' : "Password updated"}
		response['data'] = {}
		userid = data.get('userid', False)
		newpass = data.get('newpass', False)
		if userid and newpass:
			if User.objects.filter(pk=userid).exists():
				user = User.objects.filter(pk=userid).first()
				user.set_password(newpass)
				user.save()
				response['data']['id'] = user.id
				response['data']['password'] = newpass
			else:
				response['status'] = 1
				response['msg'] = "user doesn't exist"
		else:
			response['status'] = 1
			response['msg'] = "userId or new password was not entered"
		return HttpResponse(json.dumps(response), content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def change_pin(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, 'msg' : "Pin updated"}
		response['data'] = {}
		userid = data.get('userid', False)
		newpin = data.get('newpin', False)
		if userid and newpin:
			if User.objects.filter(pk=userid).exists():
				user = User.objects.filter(pk=userid).first()
				profile = user.profile
				try:
					profile.pin = newpin
					profile.save()
				except:
					response['status'] = 1
					response['msg'] = "invalid pin"
				response['data']['id'] = user.id
				response['data']['pin'] = profile.pin
			else:
				response['status'] = 1
				response['msg'] = "user doesn't exist"
		else:
			response['status'] = 1
			response['msg'] = "userId or new pin was not entered"
		return HttpResponse(json.dumps(response), content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def lock(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, 'msg' : "User status updated"}
		response['data'] = {}
		userid = data.get('userid', False)
		is_active = data.get('is_active', False)
		if userid and is_active:
			if User.objects.filter(pk=userid).exists():
				user = User.objects.filter(pk=userid).first()
				if is_active == "true":
					user.is_active = True
				elif is_active == "false":
					user.is_active = False
				user.save()
				response['data']['id'] = user.id
				response['data']['status'] = user.is_active
			else:
				response['status'] = 1
				response['msg'] = "user doesn't exist"
		else:
			response['status'] = 1
			response['msg'] = "userId or lock/unlock was not entered"
		return HttpResponse(json.dumps(response), content_type="application/json")

@user_passes_test(lambda u: u.is_superuser)
def send_money(request):
	if request.method == 'POST':
		data = request.POST
		response = {'status': 0, 'msg' : "Money transferred"}
		response['data'] = {}
		userid = data.get('userid', False)
		amount = int(data.get('amount', False))
		if userid and amount and amount>=0:
			if User.objects.filter(pk=userid).exists():
				user = User.objects.filter(pk=userid).first()
				profile = user.profile
				profile.points += amount
				profile.save()
				transaction = Transcation.objects.create(user = user, amount = amount)
				response['data']['id'] = user.id
				response['data']['points'] = profile.points
			else:
				response['status'] = 1
				response['msg'] = "user doesn't exist"
		else:
			response['status'] = 1
			response['msg'] = "userId or correct amount was not entered"
		return HttpResponse(json.dumps(response), content_type="application/json")

def make_transaction_json(transaction):
	return {
		'user': transaction.user.username,
		'amount': transaction.amount,
		'date': transaction.created.strftime("%Y:%M:%d %H::%M")
	}

@user_passes_test(lambda u: u.is_superuser)
def history(request):
	if request.method == 'GET':
		response = {'status': 0, 'msg' : "Money transferred"}
		response['data'] = []
		for each in Transcation.objects.all().order_by("created"):
			response['data'].append(make_transaction_json(each))
		return HttpResponse(json.dumps(response), content_type="application/json")