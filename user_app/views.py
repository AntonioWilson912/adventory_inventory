from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Login/registration page")

def reset_password_page(request):
    return HttpResponse("Reset your password")

def dashboard(request):
    return HttpResponse("Dashboard")

def all_users(request):
    return HttpResponse("All users")

def new_user_form(request):
    return HttpResponse("New user form")

def edit_user(request, user_id):
    return HttpResponse(f"Edit user {user_id}")