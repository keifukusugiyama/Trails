from django.db import models
from apps.login_reg_app.models import Users

class TrailManager(models.Manager):
    def trail_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 2:
            errors["name"] = "Please enter at lease 2 characters for Name"
        if len(postData['length']) < 1:
            errors["length"] = "Length field required"
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
