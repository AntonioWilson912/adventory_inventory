from django.shortcuts import render, HttpResponse, redirect
from user_app.models import User
import vendor_app
from .models import *
from vendor_app.models import Vendor

# Create your views here.
def all_products(request):
    if not "user_id" in request.session:
        return redirect("/")

    all_products = Product.objects.all()
    for this_product in all_products:
        this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1)

    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_products": all_products
    }
    return render(request, context=context, template_name="all_products.html")

def view_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="view_product.html")

def new_product_form(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_categories": Category.objects.all(),
        "all_vendors": Vendor.objects.all()
    }
    return render(request, context=context, template_name="new_product.html")

def edit_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    return render(request, context=context, template_name="edit_product.html")