from django.shortcuts import render, HttpResponse, redirect
from user_app.models import User

# Create your views here.
def all_vendors(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="all_vendors.html")

def view_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="view_vendor.html")

def new_vendor_form(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="new_vendor.html")

def edit_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="edit_vendor.html")