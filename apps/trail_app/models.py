from django.db import models
from apps.login_reg_app.models import Users
import re

class TrailManager(models.Manager):
    def trail_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 2:
            errors["name"] = "Please enter at lease 2 characters for Name"

        if len(postData['length']) < 1:
            errors["length"] = "Length field required"
        INT_REGEX = re.compile(r'^\d+$')
        if not INT_REGEX.match(postData['length']):
            errors["length"] = "length needs to be in number"

        if len(postData['elevation']) < 1:
            errors["elevation"] = "elevation field required"
        if not INT_REGEX.match(postData['elevation']):
            errors["elevation"] = "elevation needs to be in number"

        if len(postData['level']) < 1:
            errors["level"] = "level field required"

        if len(postData['trail_head']) < 2:
            errors["trail_head"] = "Enter at least 2 characters for Trail Head"
        
        return errors

class Trails(models.Model):
    name = models.CharField(max_length=255)
    length = models.FloatField()
    elevation = models.FloatField()
    level = models.CharField(max_length=45)
    trail_head = models.TextField()
    link = models.CharField(max_length=255)
    user_id = models.ForeignKey(Users, related_name="trails")
    wish_list_users = models.ManyToManyField(Users, related_name="wish_list_trails")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TrailManager()
