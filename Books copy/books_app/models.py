from django.db import models
import re
import bcrypt
from .models import *

class UserManager(models.Manager):
    def validator(self,post_data):
        errors = {}
        if len(post_data['fname']) < 2:
            errors['fname'] = "First name must be atleast 2 characters"
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last name must be atleast 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email format invalid"
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be atleast 8 characters"
        if post_data['password'] != post_data['confirm']:
            errors['confirm'] = "Passwords don't match"
        if len(User.objects.filter(email = post_data['email'])) > 0:
            errors['email'] = "Email already exists"
        return errors
    def edit_validator(self, post_data):
        errors = {}
        if len(post_data['fname']) < 2:
            errors['fname'] = "First name must be atleast 2 characters"
        if len(post_data['lname']) < 2:
            errors['lname'] = "Last name must be atleast 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Email format invalid"
        return errors
    def login_validator(self, post_data):
        errors={}
        LoginUser = User.objects.filter(email = post_data['logemail'])
        if len(LoginUser) > 0:
            if bcrypt.checkpw(post_data['logpassword'].encode(), LoginUser[0].password.encode()):
                print('match')
            else:
                errors['logpassword'] = "Password is incorrect"
        else:
            errors['logemail'] = "Email does not exitst"
        return errors


class QuoteManager(models.Manager):
    def validator(self, post_data):
        errors= {}
        if len(post_data['author']) < 3:
            errors['author'] = "Author must be atleast 5 characters"
        if len(post_data['quote']) < 10:
            errors['quote'] = "Quote must be atleast 5 characters"
        return errors

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Quote(models.Model):
    quote = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey('User', related_name="quotes_uploaded", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField('User', related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuoteManager()


# Create your models here.
