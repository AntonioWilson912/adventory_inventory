from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from user_app.models import User
from .models import Vendor, Address
from inventory_app.models import ProductVendor

# Create your views here.
def all_vendors(request):
    if not "user_id" in request.session:
        return redirect("/")

    all_vendors = Vendor.objects.all()
    for this_vendor in all_vendors:
        this_vendor.product_count = len(ProductVendor.objects.filter(vendor=this_vendor))
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_vendors": all_vendors
    }
    request.session["last_page"] = "all_vendors"
    return render(request, context=context, template_name="all_vendors.html")

def view_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")

    this_vendor = Vendor.objects.get(id=vendor_id)
    all_vendor_products = ProductVendor.objects.filter(vendor=this_vendor)
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "this_vendor": this_vendor,
        "all_vendor_products": all_vendor_products
    }
    request.session["last_page"] = "view_vendor"
    return render(request, context=context, template_name="view_vendor.html")

def new_vendor_form(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first()
    }
    request.session["last_page"] = "new_vendor"
    return render(request, context=context, template_name="new_vendor.html")

def add_vendor_to_db(request):
    if not "user_id" in request.session:
        return redirect("/")

    data = {
        "name": request.POST["name"],
        "description": request.POST["description"],
        "address": request.POST["address"],
        "city": request.POST["city"],
        "state": request.POST["state"].upper(),
        "zip_code": request.POST["zip_code"],
    }

    errors = Vendor.objects.validate_new_vendor(data)  # For later - verify an exact replica of the vendor does not exist elsewhere
    if len(errors) > 0:
        return JsonResponse(errors)

    vendor_creator = User.objects.filter(id=request.session["user_id"]).first()

    vendor_address = Address.objects.create(address=data["address"], city=data["city"], state=data["state"], zip_code=data["zip_code"])
    Vendor.objects.create(name=data["name"], description=data["description"], address=vendor_address, creator=vendor_creator)
    if "last_page" in request.session:
        if request.session["last_page"] == "view_product":
            return JsonResponse({ 'last_page': request.session["last_page"], 'product_id': request.session["product_id"] })
        elif request.session["last_page"] == "new_product":
            return JsonResponse({ 'last_page': request.session["last_page"] })
    return JsonResponse({ 'message': 'All good!' })

def edit_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "this_vendor": Vendor.objects.filter(id=vendor_id).first()
    }
    request.session["last_page"] = "edit_vendor"
    return render(request, context=context, template_name="edit_vendor.html")

def update_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")

    data = {
        "name": request.POST["name"],
        "description": request.POST["description"],
        "address": request.POST["address"],
        "city": request.POST["city"],
        "state": request.POST["state"],
        "zip_code": request.POST["zip_code"]
    }

    errors = Vendor.objects.validate_new_vendor(data) # For later - verify an exact replica of the vendor does not exist elsewhere
    if len(errors) > 0:
        return JsonResponse(errors)

    this_vendor = Vendor.objects.filter(id=vendor_id).first()
    
    this_vendor.name = data["name"]
    this_vendor.description = data["description"]

    if this_vendor.address.address != data["address"]: # If the addresses are NOT the same, create a new address and link it to the vendor
        new_address = Address.objects.create(address=data["address"], city=data["city"], state=data["state"], zip_code=data["zip_code"])
        this_vendor.address = new_address
    
    this_vendor.save()

    return JsonResponse({ 'message': 'All good!' })

def delete_vendor(request, vendor_id):
    if not "user_id" in request.session:
        return redirect("/")

    this_vendor = Vendor.objects.filter(id=vendor_id).first()
    this_vendor.delete()

    return redirect("/vendors")