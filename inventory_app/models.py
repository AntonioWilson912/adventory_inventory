from django.db import models
from user_app.models import User
from vendor_app.models import Vendor

# Returns True if the user input is a floating-point number; returns False otherwise.
def is_float(num):
    try:
        float(num) 
        return True # The num is in fact a floating-point number
    except ValueError:
        return False # bad data

# Returns True if the user input is an integer number; returns False otherwise.
def is_int(num):
    try:
        int(num)
        return True # The num is in fact an integer
    except ValueError:
        return False # bad data

# Create your models here.

# Holds information about a category
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Responsible for managing the Product model, contains validation methods
class ProductManager(models.Manager):
    def validate_new_product(self, post_data):
        errors = {}
        if len(post_data["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters long."
        if len(post_data["barcode"]) == 0:
            errors["barcode"] = "Barcode/item number must be present."
        elif Product.objects.filter(barcode=post_data["barcode"]):
            errors["barcode"] = "Barcode/item nunmber must be unique."
        if len(post_data["sku"]) == 0:
            errors["sku"] = "SKU/vendor number must be present."
        if int(post_data["category_id"]) == -1: # -1 indicates category not chosen
            errors["category"] = "Category must be chosen."
        if int(post_data["vendor_id"]) == -1: # -1 indicates vendor not chosen
            errors["vendor"] = "Vendor must be chosen."
        if not post_data["cost"] or not is_float(post_data["cost"]) or float(post_data["cost"]) <= 0.00:
            errors["cost"] = "Cost must be a valid decimal number greater than 0.00"
        if not post_data["price"] or not is_float(post_data["price"]) or float(post_data["price"]) <= 0.00:
            errors["price"] = "Price must be a valid decimal number greater than 0.00"
        
        return errors

    def validate_update_product(self, post_data):
        errors = {}
        if len(post_data["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters long."
        if len(post_data["barcode"]) == 0:
            errors["barcode"] = "Barcode/item number must be present."
        elif len(Product.objects.filter(barcode=post_data["barcode"])) > 1:
            errors["barcode"] = "Barcode/item nunmber must be unique."
        if int(post_data["category_id"]) == -1: # -1 indicates category not chosen
            errors["category"] = "Category must be chosen."
        if not post_data["qty_available"] or not is_int(post_data["qty_available"]) or int(post_data["qty_available"]) < 0:
            errors["qty_available"] = "Quantity available must be a valid whole number of at least 0"
        if not post_data["price"] or not is_float(post_data["price"]) or float(post_data["price"]) <= 0.00:
            errors["price"] = "Price must be a valid decimal number greater than 0.00"
        
        return errors

    def validate_product_vendor(self, post_data):
        errors = {}
        if int(post_data["vendor_id"]) == -1:
            errors["vendor_id"] = "Vendor must be chosen."
        if len(post_data["sku"]) == 0:
            errors["sku"] = "SKU/vendor number must be present."
        if not post_data["cost"] or not is_float(post_data["cost"]) or float(post_data["cost"]) <= 0.00:
            errors["cost"] = "Cost must be a valid decimal number greater than 0.00"
        return errors

# Model used to hold information about a product
class Product(models.Model):
    barcode = models.CharField(max_length=12)
    name = models.CharField(max_length=255)
    description = models.TextField()
    qty_available = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="product_creators", on_delete=models.CASCADE)
    product_updates = models.ManyToManyField(User, through="ProductUpdate")
    product_vendors = models.ManyToManyField(Vendor, through="ProductVendor")
    objects = ProductManager()

# Model used to contain information about when a product is updated and who updates it.
class ProductUpdate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Model used to contain information about all the vendors that distribute a particular product.
class ProductVendor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    is_primary_vendor = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)