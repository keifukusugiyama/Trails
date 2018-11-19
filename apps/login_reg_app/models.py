from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field

        # check first_name and last_name fields have values
        if len(postData['fname']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        #check if email has str@str.str format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address format"

        # check if any user object has same email, if there is a match, put error
        user = Users.objects.filter(email = postData['email'])
        if len(user) > 0:
            errors["email"] = "This email is already registered"
        
        # check password is at least 8 char
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        # check if confirm password matches
        if postData['c_password'] != postData['password']:
            errors["c_password"] = "Confirm Password: Passwords do not match"

        return errors

    def edit_validator(self, postData, id):
        errors = {}
        if len(postData['fname']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"

        #check if email has str@str.str format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid email address format"

        this_user_email = Users.objects.get(id= id).email
        emails = Users.objects.filter(email = postData['email'])
        if len(emails) > 0:
            for each_email in emails:
                if each_email.email != this_user_email:
                    errors["email"] = "This email is already registered"

        return errors

# create users table
class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"< Users object: id: {self.id} {self.first_name}>"

        