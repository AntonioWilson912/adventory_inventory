from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_new_user(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data["first_name"]) < 3:
            errors["first_name"] = "First name must be at least 3 characters."
        if len(post_data["last_name"]) < 3:
            errors["last_name"] = "Last name must be at least 3 characters."
        if not EMAIL_REGEX.match(post_data["email"]):
            errors["email"] = "Invalid email."
        elif User.objects.filter(email=post_data["email"]):
            errors["email"] = "Invalid email."
        if "is_admin" in post_data and "is_admin" == -1:
            errors["is_admin"] = "Must choose whether user is an admin."
        if len(post_data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        else:
            if not re.findall("[0-9]", post_data["password"]):
                errors["password_digit"] = "Password must have at least 1 digit."
            if not re.findall("[^\w\s]", post_data["password"]):
                errors["password_special"] = "Password must have at least 1 special character."
            if post_data["password"] != post_data["confirm_password"]:
                errors["confirm_password"] = "Passwords must match."
        return errors

    def validate_new_password(self, post_data):
        errors = {}
        if not User.objects.filter(email=post_data["email"]):
            errors["email"] = "No account is registered under that email."
        if len(post_data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        else:
            if not re.findall("[0-9]", post_data["password"]):
                errors["password_digit"] = "Password must have at least 1 digit."
            if not re.findall("[^\w\s]", post_data["password"]):
                errors["password_special"] = "Password must have at least 1 special character."
            if post_data["password"] != post_data["confirm_password"]:
                errors["confirm_password"] = "Passwords must match."
        return errors

    def validate_existing_user(self, post_data):
        errors = {}
        if len(post_data["email"]) == 0:
            errors["email"] = "Email required."
        elif len(post_data["password"]) == 0:
            errors["password"] = "Password required."
        else:
            existing_user = User.objects.filter(email=post_data["email"])
            if not existing_user:
                errors["email"] = "Invalid email/password."
            else:
                the_user = existing_user[0]
                if not bcrypt.checkpw(post_data["password"].encode(), the_user.password.encode()):
                    errors["password"] = "Invalid email/password"
        return errors

    def validate_update_user(self, post_data):
        errors = {}
        if len(post_data["first_name"]) < 3:
            errors["first_name"] = "First name must be at least 3 characters."
        if len(post_data["last_name"]) < 3:
            errors["last_name"] = "Last name must be at least 3 characters."
        if not "is_admin" in post_data:
            errors["is_admin"] = "It must be decided whether user is admin or not."
        if len(post_data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters."
        else:
            if not re.findall("[0-9]", post_data["password"]):
                errors["password_digit"] = "Password must have at least 1 digit."
            if not re.findall("[^\w\s]", post_data["password"]):
                errors["password_special"] = "Password must have at least 1 special character."
            if post_data["password"] != post_data["confirm_password"]:
                errors["confirm_password"] = "Passwords must match."
        return errors

    def validate_new_password(self, post_data):
        errors = {}
        if len(post_data["email"]) == 0:
            errors["email"] = "Email required."
        elif len(post_data["password"]) == 0:
            errors["password"] = "New password required."
        else:
            existing_user = User.objects.filter(email=post_data["email"])
            if not existing_user:
                errors["email"] = "Invalid email."
            else:
                if not re.findall("[0-9]", post_data["password"]):
                    errors["password_digit"] = "Password must have at least 1 digit."
                if not re.findall("[^\w\s]"):
                    errors["password_special"] = "Password must have at least 1 special character."
                if post_data["password"] != post_data["confirm_password"]:
                    errors["confirm_password"] = "Passwords must match."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_admin = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()