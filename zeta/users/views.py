from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def home(request):
	return render(request,"home.html")

def create_user(request):
	pass

def change_password(request):
	pass

def change_pin(request):
	pass

def lock(request):
	pass

def send_amount(request):
	pass

def history(request):
	pass
