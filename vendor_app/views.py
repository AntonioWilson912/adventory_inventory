from django.shortcuts import render, HttpResponse

# Create your views here.
def all_vendors(request):
    return HttpResponse("All vendors")

def view_vendor(request, vendor_id):
    return HttpResponse(f"View vendor {vendor_id}")

def new_vendor_form(request):
    return HttpResponse("New vendor form")

def edit_vendor(request, vendor_id):
    return HttpResponse(f"Edit vendor {vendor_id}")