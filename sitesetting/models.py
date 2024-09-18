from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    exprience_number = models.PositiveIntegerField()
    success_stories_number =  models.PositiveIntegerField()
    team_member_number = models.PositiveIntegerField()
    project_completed_number = models.PositiveIntegerField()
    privacy_policy = models.TextField()
    terms_and_condition = models.TextField()
        