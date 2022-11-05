from django.shortcuts import render, redirect
from user_app.models import User
from .models import *
from vendor_app.models import Vendor

# Create your views here.
def all_products(request):
    if not "user_id" in request.session:
        return redirect("/")

    all_products = Product.objects.all()
    for this_product in all_products:
        this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first().sku

    request.session["last_page"] = "all_products"

    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_products": all_products,
        "all_categories": Category.objects.all().order_by("name"),
        "all_vendors": Vendor.objects.all().order_by("name")
    }
    return render(request, context=context, template_name="all_products.html")

def view_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")

    this_product = Product.objects.get(id=product_id)
    last_update = ProductUpdate.objects.filter(product=this_product).first()
    this_product.last_update = last_update

    # get vendors not associated with the product
    all_vendors = Vendor.objects.all()

    all_product_vendors = ProductVendor.objects.filter(product=this_product)
    all_product_vendor_vendors = []
    for product_vendor in all_product_vendors:
        all_product_vendor_vendors.append(product_vendor.vendor)

    not_product_vendors = list(set(all_vendors) - set(all_product_vendor_vendors))

    print(not_product_vendors)
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "this_product": this_product,
        "all_product_vendors": all_product_vendors,
        "not_product_vendors": not_product_vendors
    }

    request.session["last_page"] = "view_product"
    request.session["product_id"] = product_id
    return render(request, context=context, template_name="view_product.html")

def add_product_to_db(request):
    if not "user_id" in request.session:
        return redirect("/")

    data = {
        "name": request.POST["name"],
        "barcode": request.POST["barcode"],
        "category_id": request.POST["category_id"],
        "vendor_id": request.POST["vendor_id"],
        "sku": request.POST["sku"],
        "description": request.POST["description"],
        "cost": request.POST["cost"],
        "price": request.POST["price"]
    }

    errors = Product.objects.validate_product(data)
    if len(errors) > 0:
        return redirect("/products/new") # TODO: AJAX response

    product_creator = User.objects.filter(id=request.session["user_id"]).first()
    product_category = Category.objects.get(id=data["category_id"])
    product_vendor = Vendor.objects.get(id=data["vendor_id"])

    new_product = Product.objects.create(barcode=data["barcode"], name=data["name"], description=data["description"], qty_available=0, price=data["price"], category=product_category, creator=product_creator)
    ProductVendor.objects.create(product=new_product, vendor=product_vendor, sku=data["sku"], cost=data["cost"], is_primary_vendor=1)
    ProductUpdate.objects.create(product=new_product, user=product_creator)

    return redirect("/products")

def add_product_vendor(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")

    data = {
        "vendor_id": request.POST["vendor_id"],
        "sku": request.POST["sku"],
        "cost": request.POST["cost"]
    }

    errors = Product.objects.validate_product_vendor(data)

    print(errors)
    if len(errors) > 0:
        # return JsonResponse(errors)
        return redirect(f"/products/{product_id}")

    # otherwise, create the product vendor, set the primary to not primary and set the new one to primary
    this_product = Product.objects.get(id=product_id)
    previous_primary_vendor = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first()
    previous_primary_vendor.is_primary_vendor = 0
    previous_primary_vendor.save()

    product_vendor = Vendor.objects.get(id=data["vendor_id"])
    ProductVendor.objects.create(product=this_product, vendor=product_vendor, sku=data["sku"], cost=data["cost"], is_primary_vendor=1)

    return redirect(f"/products/{product_id}")

def new_product_form(request):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_categories": Category.objects.all().order_by("name"),
        "all_vendors": Vendor.objects.all().order_by("name")
    }
    request.session["last_page"] = "new_product"
    return render(request, context=context, template_name="new_product.html")

def edit_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "this_product": Product.objects.get(id=product_id),
        "all_categories": Category.objects.all().order_by("name")
    }
    request.session["last_page"] = "edit_product"
    return render(request, context=context, template_name="edit_product.html")

def update_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")

    data = {
        "name": request.POST["name"],
        "barcode": request.POST["barcode"],
        "category_id": request.POST["category_id"],
        "description": request.POST["description"],
        "qty_available": request.POST["qty_available"],
        "price": request.POST["price"]
    }

    errors = Product.objects.validate_update_product(data)
    print(errors)
    if len(errors) > 0:
        return redirect(f"/products/{product_id}/edit") # TODO: AJAX response

    updated_product = Product.objects.get(id=product_id)
    product_updater = User.objects.filter(id=request.session["user_id"]).first()
    product_category = Category.objects.get(id=data["category_id"])

    updated_product.name = data["name"]
    updated_product.barcode = data["barcode"]
    updated_product.category = product_category
    updated_product.qty_available = data["qty_available"]
    updated_product.save()

    product_update = ProductUpdate.objects.filter(product=updated_product).first()
    product_update.user = product_updater
    product_update.save()

    return redirect("/products")

def delete_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    product_to_delete = Product.objects.get(id=product_id)
    product_to_delete.delete()
    return redirect("/products")