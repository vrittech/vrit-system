from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    experience_number = models.PositiveIntegerField()
    success_stories_number =  models.PositiveIntegerField()
    team_member_number = models.PositiveIntegerField()
    project_completed_number = models.PositiveIntegerField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ('manage_site_settings', 'Manage Site Settings'),
        ]
    
class TermAndCondition(models.Model):
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ('manage_terms_conditions', 'Manage Terms Conditions'),
        ]
    
class PrivacyPolicy(models.Model):
    description = models.TextField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = [
            ('manage_privacy_policy', 'Manage Privacy Policy'),
        ]
    
        