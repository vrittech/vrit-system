from django.db import models
from projects.models import ProjectService
from plan.models import Plan
from ordered_model.models import OrderedModel

from services.models import Services

class Inquires(OrderedModel):
    services = models.ManyToManyField(Services,related_name="inquires")
    project_plan = models.ForeignKey(Plan,related_name = "inquires",on_delete=models.SET_NULL,null=True)
    full_name = models.CharField(max_length = 250)
    email_address = models.EmailField(max_length = 255)
    phone_number = models.CharField(max_length = 15)
    company_name = models.CharField(max_length = 300)
    project_detail = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    created_date= models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.full_name
    

    
