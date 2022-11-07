from django.db import models
from user_app.models import User

# Create your models here.

# Responsible for managing the Vendor model, contains validation methods
class VendorManager(models.Manager):
    def validate_new_vendor(self, post_data):
        errors = {}
        if len(post_data["name"]) < 3:
            errors["name"] = "Name must be at least 3 characters."
        if len(post_data["address"]) < 3:
            errors["address"] = "Address must be at least 3 characters."
        if len(post_data["city"]) < 3:
            errors["city"] = "City must be at least 3 characters."
        if len(post_data["state"]) != 2:
            errors["state"] = "State must be exactly 2 characters long."
        if len(post_data["zip_code"]) != 5 or not post_data["zip_code"].isdigit():
            errors["zip_code"] = "Zip code must be exactly 5 digits long."
        return errors

# Model used to hold information about the address of a vendor.
class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Model used to hold information about a vendor.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.ForeignKey(Address, related_name="addresses", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    objects = VendorManager()