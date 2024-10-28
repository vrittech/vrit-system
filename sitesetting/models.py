from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    experience_number = models.PositiveIntegerField()
    success_stories_number =  models.PositiveIntegerField()
    team_member_number = models.PositiveIntegerField()
    project_completed_number = models.PositiveIntegerField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class TermAndCondition(models.Model):
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class PrivacyPolicy(models.Model):
    description = models.TextField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
        