from django.shortcuts import render, redirect
from django.http import JsonResponse
from user_app.models import User
from .models import *
from vendor_app.models import Vendor

# Create your views here.

# Converts the given product (with SKU and category name) to a dictionary to be used for JSON
def convert_product_to_dict(product):
    product_dict = {}
    product_dict["id"] = product.id
    product_dict["barcode"] = product.barcode
    product_dict["name"] = product.name
    product_dict["description"] = product.description
    product_dict["qty_available"] = product.qty_available
    product_dict["price"] = product.price
    product_dict["sku"] = product.sku
    product_dict["category"] = product.category.name

    return product_dict

# Renders the form for creating a new product
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

# Extracts form data to create a new product upon successful validation.
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
    # print(data)
    errors = Product.objects.validate_new_product(data)
    if len(errors) > 0:
        return JsonResponse(errors)

    product_creator = User.objects.filter(id=request.session["user_id"]).first()
    product_category = Category.objects.get(id=data["category_id"])
    product_vendor = Vendor.objects.get(id=data["vendor_id"])

    new_product = Product.objects.create(barcode=data["barcode"], name=data["name"], description=data["description"], qty_available=0, price=data["price"], category=product_category, creator=product_creator)
    ProductVendor.objects.create(product=new_product, vendor=product_vendor, sku=data["sku"], cost=data["cost"], is_primary_vendor=1)
    ProductUpdate.objects.create(product=new_product, user=product_creator)

    return JsonResponse({ 'message': 'All good!' })

# Creates a new product vendor for the specified product upon successful validation.
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
        return JsonResponse(errors)

    # otherwise, create the product vendor, set the primary to not primary and set the new one to primary
    this_product = Product.objects.get(id=product_id)
    previous_primary_vendor = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first()
    if previous_primary_vendor:
        previous_primary_vendor.is_primary_vendor = 0
        previous_primary_vendor.save()

    product_vendor = Vendor.objects.get(id=data["vendor_id"])
    ProductVendor.objects.create(product=this_product, vendor=product_vendor, sku=data["sku"], cost=data["cost"], is_primary_vendor=1)
    product_update = ProductUpdate.objects.filter(product=this_product).first()
    product_update.user = User.objects.filter(id=request.session["user_id"]).first()
    product_update.save()

    return JsonResponse({ 'product': product_id})

# Delivers a list of all the products in the database with SKU and category name.
def all_products(request):
    if not "user_id" in request.session:
        return redirect("/")

    request.session["last_page"] = "all_products"

    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "all_categories": Category.objects.all().order_by("name"),
        "all_vendors": Vendor.objects.all().order_by("name")
    }
    return render(request, context=context, template_name="all_products.html")

# Performs a search in the product database according to a user-specified category, vendor, and/or product name.
def search_products(request):
    if not "user_id" in request.session:
        return redirect("/")

    all_products = []
    all_products_dict = {}

    if len(request.POST["search_term"]) == 0:
        if request.POST["search_category"] == "all":
            if request.POST["search_vendor"] == "all":
                all_products_models = Product.objects.all()
                for this_product in all_products_models:
                    this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first().sku if ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first() else None
                    all_products.append(convert_product_to_dict(this_product))
            else:
                search_vendor = Vendor.objects.get(id=int(request.POST["search_vendor"]))
                all_products_by_vendor = ProductVendor.objects.filter(vendor=search_vendor)
                all_product_vendor_products = []
                for product_vendor in all_products_by_vendor:
                    all_product_vendor_products.append(product_vendor.product)

                for this_product in all_product_vendor_products:
                    this_product.sku = ProductVendor.objects.filter(product=this_product, vendor=search_vendor).first().sku
                    all_products.append(convert_product_to_dict(this_product))
        else:
            search_category = Category.objects.get(id=int(request.POST["search_category"]))
            all_products_models = Product.objects.filter(category=search_category)
            if request.POST["search_vendor"] == "all":
                for this_product in all_products_models:
                    this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first().sku
                    all_products.append(convert_product_to_dict(this_product))
            else:
                search_vendor = Vendor.objects.get(id=int(request.POST["search_vendor"]))
                all_products_by_vendor = ProductVendor.objects.filter(vendor=search_vendor)
                all_product_vendor_products = []
                for product_vendor in all_products_by_vendor:
                    all_product_vendor_products.append(product_vendor.product)

                for this_product in all_product_vendor_products:
                    if this_product.category.id == search_category.id:
                        this_product.sku = ProductVendor.objects.filter(product=this_product, vendor=search_vendor).first().sku
                        all_products.append(convert_product_to_dict(this_product))
    else:
        search_products = Product.objects.filter(name__contains=request.POST["search_term"])
        if request.POST["search_category"] == "all":
            if request.POST["search_vendor"] == "all":
                for this_product in search_products:
                    this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first().sku
                    all_products.append(convert_product_to_dict(this_product))
            else:
                search_vendor = Vendor.objects.get(id=int(request.POST["search_vendor"]))
                all_products_by_vendor = ProductVendor.objects.filter(vendor=search_vendor)
                all_product_vendor_products = []
                for product_vendor in all_products_by_vendor:
                    all_product_vendor_products.append(product_vendor.product)

                for this_product in all_product_vendor_products:
                    if this_product in search_products:
                        this_product.sku = ProductVendor.objects.filter(product=this_product, vendor=search_vendor).first().sku
                        all_products.append(convert_product_to_dict(this_product))
        else:
            search_category = Category.objects.get(id=int(request.POST["search_category"]))
            all_products_models = Product.objects.filter(name__contains=request.POST["search_term"], category=search_category)
            if request.POST["search_vendor"] == "all":
                for this_product in all_products_models:
                    this_product.sku = ProductVendor.objects.filter(product=this_product, is_primary_vendor=1).first().sku
                    all_products.append(convert_product_to_dict(this_product))
            else:
                search_vendor = Vendor.objects.get(id=int(request.POST["search_vendor"]))
                all_products_by_vendor = ProductVendor.objects.filter(vendor=search_vendor)
                all_product_vendor_products = []
                for product_vendor in all_products_by_vendor:
                    all_product_vendor_products.append(product_vendor.product)

                for this_product in all_product_vendor_products:
                    if this_product in search_products and this_product.category.id == search_category.id:
                        this_product.sku = ProductVendor.objects.filter(product=this_product, vendor=search_vendor).first().sku
                        all_products.append(convert_product_to_dict(this_product))

    all_products_dict["all_products"] = all_products

    return JsonResponse(all_products_dict)

# Delivers all the information about the requested product including product vendor and product update information.
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

    # print(not_product_vendors)
        
    context = {
        "this_user": User.objects.filter(id=request.session["user_id"]).first(),
        "this_product": this_product,
        "all_product_vendors": all_product_vendors,
        "not_product_vendors": not_product_vendors
    }

    request.session["last_page"] = "view_product"
    request.session["product_id"] = product_id
    return render(request, context=context, template_name="view_product.html")

# Generates a pre-filled form so that the user can edit information about the current product.
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

# Updates the product information in the database with the new product information.
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
        return JsonResponse(errors)

    updated_product = Product.objects.get(id=product_id)
    product_updater = User.objects.filter(id=request.session["user_id"]).first()
    product_category = Category.objects.get(id=data["category_id"])

    updated_product.name = data["name"]
    updated_product.barcode = data["barcode"]
    updated_product.category = product_category
    updated_product.price = data["price"]
    updated_product.qty_available = data["qty_available"]
    updated_product.save()

    product_update = ProductUpdate.objects.filter(product=updated_product).first()
    product_update.user = product_updater
    product_update.save()

    return JsonResponse({ 'message': 'All good!' })

# Updates the current primary vendor for the product according to the selected primary vendor in the form.
def update_primary_vendor(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")

    new_primary_vendor = Vendor.objects.get(id=request.POST["vendor_id"])
    current_product = Product.objects.get(id=product_id)

    current_product_vendors = ProductVendor.objects.filter(product=current_product)
    for current_product_vendor in current_product_vendors:
        if current_product_vendor.vendor.id == new_primary_vendor.id:
            current_product_vendor.is_primary_vendor = 1
            current_product_vendor.save()
        else:
            current_product_vendor.is_primary_vendor = 0
            current_product_vendor.save()

    product_update = ProductUpdate.objects.filter(product=current_product).first()
    product_update.user = User.objects.filter(id=request.session["user_id"]).first()
    product_update.save()

    return JsonResponse({ 'message': 'All good!' })

# Removes the product from the database.
def delete_product(request, product_id):
    if not "user_id" in request.session:
        return redirect("/")
        
    product_to_delete = Product.objects.get(id=product_id)
    product_update = ProductUpdate.objects.filter(product=product_to_delete).first()
    product_update.delete()
    product_to_delete.delete()
    
    return JsonResponse({ 'message': 'All good!' })