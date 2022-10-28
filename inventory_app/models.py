from django.db import models
from user_app.models import User
from vendor_app.models import Vendor

def is_float(num):
    try:
        float(num) 
        return True # The num is in fact a floating-point number
    except ValueError:
        return False # bad data

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductManager(models.Manager):
    def validate_product(self, post_data):
        errors = {}
        if len(post_data["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters long."
        if len(post_data["barcode"]) == 0:
            errors["barcode"] = "Barcode/item number must be present."
        elif Product.objects.filter(barcode=post_data["barcode"]):
            errors["barcode"] = "Barcode/item nunmber must be unique."
        if post_data["category_id"] == -1: # -1 indicates category not chosen
            errors["category"] = "Category must be chosen."
        if post_data["vendor_id"] == -1: # -1 indicates vendor not chosen
            errors["vendor"] = "Vendor must be chosen."
        if not post_data["price"] or not is_float(post_data["price"]) or float(post_data["price"]) <= 0.00:
            errors["price"] = "Price must be a valid decimal number greater than 0.00"
        return errors

class Product(models.Model):
    barcode = models.CharField(max_length=12)
    name = models.CharField(max_length=255)
    description = models.TextField()
    qty_available = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    product_updates = models.ManyToManyField(User, through="ProductUpdate")
    product_vendors = models.ManyToManyField(Vendor, through="ProductVendor")

class ProductUpdate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ProductVendor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_primary_vendor = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)