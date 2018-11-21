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

class ExerciseManager(models.Manager):
    def exercise_validator(self, postData):
        errors = {}
        if len(postData['duration']) < 1:
            errors['duration'] = "Enter duration of your exercise"
        if len(postData['calories']) < 1:
            errors['calories'] = "Enter calories burned from your exercise"
        if len(postData['pace']) < 1:
            errors['pace'] = "Enter how fast you hiked/walked/biked"
        
        return errors

class Reports(models.Model):
    comment = models.TextField()
    rating = models.IntegerField()
    trail_id = models.ForeignKey(Trails, related_name="reports")
    user_id = models.ForeignKey(Users, related_name="reports")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReportManager()

class Exercises(models.Model):
    duration = models.CharField(max_length=255)
    avg_bpm = models.IntegerField(null=True)
    max_bpm = models.IntegerField(null=True)
    calories = models.IntegerField()
    pace = models.CharField(max_length=255)
    steps = models.IntegerField(null=True)
    elevation = models.IntegerField(null=True)
    report_id = models.ForeignKey(Reports, related_name="exercises")
    user_id = models.ForeignKey(Users,  related_name="exercises")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ExerciseManager()