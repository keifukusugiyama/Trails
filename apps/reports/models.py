from django.db import models
from apps.login_reg_app.models import Users
from apps.trail_app.models import Trails 

class ReportManager(models.Manager):
    def report_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['comment']) < 2:
            errors["comment"] = "Enter at least 2 characters for comment"
        if len(postData['rating']) < 1:
            errors["rating"] = "Enter your rating"
        return errors

class Reports(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    trail_id = models.ForeignKey(Trails, related_name="reports")
    user_id = models.ForeignKey(Users, related_name="reports")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReportManager()