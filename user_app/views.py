from django.shortcuts import render, redirect
from django.http import JsonResponse
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
    #print(data)
    errors = User.objects.validate_new_user(data)
    if len(errors) > 0:
        return JsonResponse(errors) # Errors is already a dictionary
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], password=password_hash, is_admin=0)
    request.session["user_id"] = new_user.id

    return JsonResponse({ 'message': 'All good!' })

def login_user(request):
    data = {
        "email": request.POST["email"],
        "password": request.POST["password"]
    }
    #print(data)
    errors = User.objects.validate_existing_user(data)
    if len(errors) > 0:
        return JsonResponse(errors)

    user = User.objects.filter(email=data["email"])
    request.session["user_id"] = user[0].id

    return JsonResponse({ 'message': 'All good!' })
    
def reset_password_page(request):
    return render(request, template_name="reset_password.html")

def reset_password_in_db(request):
    data = {
        "email": request.POST["email"],
        "password": request.POST["password"],
        "confirm_password": request.POST["confirm_password"]
    }
    print(data)
    errors = User.objects.validate_new_password(data)
    if len(errors) > 0:
        return JsonResponse(errors)
    return JsonResponse({ 'message': 'All good!' })

def dashboard(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="dashboard.html")

def all_users(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_users": User.objects.all()
    }
    return render(request, context=context, template_name="all_users.html")

def new_user_form(request):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="new_user.html")

def create_user_in_db(request):
    if not "user_id" in request.session:
        return redirect("/")
    data = {
        "first_name": request.POST["first_name"],
        "last_name": request.POST["last_name"],
        "email": request.POST["email"],
        "is_admin": request.POST["is_admin"] if "is_admin" in request.POST else -1,
        "password": request.POST["password"],
        "confirm_password": request.POST["confirm_password"]
    }
    print(data)
    errors = User.objects.validate_new_user(data)
    if len(errors) > 0:
        print(errors)
        return JsonResponse(errors)
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], password=password_hash, is_admin=data["is_admin"])

    return JsonResponse({ 'message': 'All good!' })

def edit_user(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "requested_user": User.objects.filter(id=user_id).first()
    }
    return render(request, context=context, template_name="edit_user.html")

def update_user_in_db(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    data = {
        "first_name": request.POST["first_name"],
        "last_name": request.POST["last_name"],
        "is_admin": request.POST["is_admin"] if "is_admin" in request.POST else 1,
        "password": request.POST["password"],
        "confirm_password": request.POST["confirm_password"]
    }
    print(data)
    errors = User.objects.validate_update_user(data)
    if len(errors) > 0:
        return JsonResponse(errors)
        return redirect(f"/users/{user_id}/edit_user") # TODO: Change this to be an AJAX response later
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

    current_user = User.objects.filter(id=user_id).first()
    current_user.first_name = data["first_name"]
    current_user.last_name = data["last_name"]
    current_user.is_admin = data["is_admin"]
    current_user.password = password_hash
    current_user.save()

    return JsonResponse({ 'message': 'All good!' })
    return redirect("/users")

def delete_user(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    user_to_delete = User.objects.filter(id=user_id).first()
    user_to_delete.delete()
    return redirect("/users")

def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect("/")