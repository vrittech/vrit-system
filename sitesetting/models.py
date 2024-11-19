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
            ('manage_sitesettings', 'Manage Site Settings'),
        ]
    
class TermAndCondition(models.Model):
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        permissions = [
            ('manage_termsandconditions', 'Manage Terms And Conditions'),
        ]
    
class PrivacyPolicy(models.Model):
    description = models.TextField()
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        permissions = [
            ('manage_privacypolicy', 'Manage Privacy Policy'),
        ]
    
        