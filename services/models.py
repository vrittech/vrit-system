from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ordered_model.models import OrderedModel

class ServicesCategory(OrderedModel):
    name = models.CharField(max_length = 155)
    color= models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name})"
class Services(OrderedModel):
    name = models.CharField(max_length = 155)
    description = models.TextField()
    category = models.ManyToManyField(ServicesCategory, related_name='services', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name})"



