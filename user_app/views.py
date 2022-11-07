from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import User
import bcrypt

# Create your views here.

# The root route - registration/login page.
def index(request):
    request.session["last_page"] = "index"
    return render(request, template_name="index.html")

# Creates a new user in the database upon successful validation and redirects to the user dashboard.
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

# Logs in the user upon success validation and redirects to the user dashboard.
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

# Page with a form that allows the user to reset their password with an existing email and a new password.
def reset_password_page(request):
    request.session["last_page"] = "reset_password"
    return render(request, template_name="reset_password.html")

# Resets the user's password for the specified email upon successful validation.
def reset_password_in_db(request):
    data = {
        "email": request.POST["email"],
        "password": request.POST["password"],
        "confirm_password": request.POST["confirm_password"]
    }
    #print(data)
    errors = User.objects.validate_new_password(data)
    if len(errors) > 0:
        return JsonResponse(errors)
    return JsonResponse({ 'message': 'All good!' })

# Logs out the user, clears all session data and redirects to the root route.
def logout(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect("/")

# Provides a home for the user to make a decision between viewing inventory, vendors, or users.
def dashboard(request):
    if not "user_id" in request.session:
        return redirect("/")
    request.session["last_page"] = "dashboard"
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="dashboard.html")

# Creates a new user in the database upon successful validation and redirects to the list of all users.
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
    # print(data)
    errors = User.objects.validate_new_user(data)
    if len(errors) > 0:
        print(errors)
        return JsonResponse(errors)
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=data["first_name"], last_name=data["last_name"], email=data["email"], password=password_hash, is_admin=data["is_admin"])

    return JsonResponse({ 'message': 'All good!' })

# Generates a table containing all the registered users.
def all_users(request):
    if not "user_id" in request.session:
        return redirect("/")
    request.session["last_page"] = "all_users"
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_users": User.objects.all()
    }
    return render(request, context=context, template_name="all_users.html")

# Generates a form that allows a user to create a new user.
def new_user_form(request):
    if not "user_id" in request.session:
        return redirect("/")
    request.session["last_page"] = "new_user"
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="new_user.html")

# Generates a form that allows a user to edit the specified user's information.
def edit_user(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    request.session["last_page"] = "edit_user"
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "requested_user": User.objects.filter(id=user_id).first()
    }
    return render(request, context=context, template_name="edit_user.html")

# Updates the user's information in the database upon successful validation.
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
    errors = User.objects.validate_update_user(data)
    if len(errors) > 0:
        return JsonResponse(errors)
    
    password_hash = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()

    current_user = User.objects.filter(id=user_id).first()
    current_user.first_name = data["first_name"]
    current_user.last_name = data["last_name"]
    current_user.is_admin = data["is_admin"]
    current_user.password = password_hash
    current_user.save()

    return JsonResponse({ 'message': 'All good!' })

# Deletes the specified user from the database.
def delete_user(request, user_id):
    if not "user_id" in request.session:
        return redirect("/")
    user_to_delete = User.objects.filter(id=user_id).first()
    user_to_delete.delete()
    return redirect("/users")