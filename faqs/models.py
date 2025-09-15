from django.db import models
from ordered_model.models import OrderedModel
# Create your models here.

class FaqsCategory(OrderedModel):
    name = models.CharField(max_length = 155)
    color= models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.name
    
class Faqs(OrderedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    faqs_category = models.ForeignKey(
        FaqsCategory,
        on_delete=models.CASCADE,
        related_name="faqs",
        null=True,
        blank=True
    )
    
    def __str__(self):
        return f"{self.question})"
    



class ContactUs(models.Model):
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=255)
    position= models.BigIntegerField(default=9999)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.email})"
    
    class Meta:
        permissions = [
            ('manage_contact_us', 'Manage Contact Us'),
        ]
