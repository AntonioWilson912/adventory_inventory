from django.shortcuts import render, HttpResponse

# Create your views here.
def all_products(request):
    return HttpResponse("All Products")

def view_product(request, product_id):
    return HttpResponse(f"View Product {product_id}")

def new_product_form(request):
    return HttpResponse("New Product Form")

def edit_product(request, product_id):
    return HttpResponse(f"Edit product {product_id}")