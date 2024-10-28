from django.db import models

# # Create your models here.
# title
# category--> foreignkey
# description
# header_code
# embedded_code
# image
# excerpt
# auto expiration
# auto expiration date
# position 
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

class Forms(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forms')
    description = models.TextField()
    header_code = models.TextField(blank=True, null=True)
    embedded_code = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='forms', blank=True, null=True)
    excerpt = models.CharField(max_length=500, blank=True, null=True)
    auto_expiration = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    auto_expiration_date = models.DateField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


