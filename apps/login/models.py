from __future__ import unicode_literals

from django.db import models

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

# Create your models here.
class RegistrationManager(models.Manager):
    def add_user(self, data):
        errors = []
        pw_hash = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
        if not data['first_name']:
            errors.append("Enter a name")
        elif not len (data['first_name']) > 2:
            errors.append("Name has to be longer than 2 letters")
        if not data['last_name']:
            errors.append("Enter a name")
        elif not len (data['last_name']) > 2:
            errors.append("Name has to be longer than 2 letters")
        if not data['email']:
            errors.append("Enter an email")
        elif not EMAIL_REGEX.match(data['email']):
            errors.append("Email is not valid")
        if not data['password']:
            errors.append("Enter password")
        elif not len (data['password']) < 8:
            errors.append("Password has to be less than 8 letters")
        elif not data['password'] == data['confirm']:
            errors.append("Passwords do not match")

        response={}

        if not errors:
            new_user = self.create(first_name = data['first_name'], last_name = data['last_name'], email = data['email'], password=pw_hash)
            response['added'] = True
            response['new_user'] = new_user
        else:
            response['added'] = False
            response['errors'] = errors

        return response

    def validate(self, data):
        try:
            user = self.get(email = data['email'])
            password = data['password'].encode()
            if bcrypt.hashpw(password, user.password.encode()) == user.password.encode():
                return(True, user)
        except Registration.DoesNotExist:
            user = None



class Registration(models.Model):
    first_name= models.CharField(max_length = 255)
    last_name= models.CharField(max_length = 255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()
