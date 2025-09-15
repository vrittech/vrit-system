from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ordered_model.models import OrderedModel

# Create your models here.

class Testimonial(OrderedModel):
    full_name = models.CharField(max_length = 155)
    position =  models.CharField(max_length = 155)
    description = models.TextField()
    profile_image = models.CharField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name})"
    # class Meta:
    #     permissions = [
    #             ('manage_testimonial', 'Manage Testimonial'),
    #         ]


