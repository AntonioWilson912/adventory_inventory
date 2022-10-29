from django.shortcuts import render, HttpResponse, redirect
from user_app.models import User

# Create your views here.
def all_products(request):
    if not "user_id" in request.session:
        return redirect("/")

    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="all_products.html")

def view_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="view_product.html")

def new_product_form(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="new_product.html")

def edit_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"])[0]
    }
    return render(request, context=context, template_name="edit_product.html")