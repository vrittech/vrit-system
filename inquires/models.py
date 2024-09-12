from django.db import models
from projects.models import ProjectService
from plan.models import Plan
# Create your models here.

class Inquires(models.Model):
    project_service = models.ManyToManyField(ProjectService,related_name="inquires")
    project_plan = models.ForeignKey(Plan,related_field = "inquires")
    first_name = models.CharField(max_length = 250)
    last_name = models.CharField(max_length = 250)
    email_address = models.EmailField(max_length = 255)
    phone_number = models.CharField(max_length = 15)
    company_name = models.CharField(max_length = 300)
    project_detail = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
