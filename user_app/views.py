from django.shortcuts import render, redirect, HttpResponse
from .models import User
import bcrypt

# Create your views here.
def index(request):
    return render(request, template_name="index.html")

def register_user(request):
    data = {
        "first_name": request.POST["first_name"],
        "last_name": request.POST["last_name"],
        "email": request.POST["email"],
        "password": request.POST["password"],
        "confirm_password": request.POST["confirm_password"]
    }
    print(data)
    errors = User.objects.validate_new_user(data)
    if len(errors) > 0:
        return redirect("/")
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], password=password_hash, is_admin=1)
    request.session["user_id"] = new_user.id

    return redirect("/dashboard")

def login_user(request):
    data = {
        "email": request.POST["email"],
        "password": request.POST["password"]
    }
    errors = User.objects.validate_existing_user(data)
    if len(errors) > 0:
        return redirect("/")

    user = User.objects.filter(email=data["email"])
    request.session["user_id"] = user[0].id

    return redirect("/dashboard")
    
def reset_password_page(request):
    return render(request, template_name="reset_password.html")

def dashboard(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="dashboard.html")

def all_users(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="all_users.html")

def new_user_form(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="new_user.html")

def edit_user(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="edit_user.html")

def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect("/")