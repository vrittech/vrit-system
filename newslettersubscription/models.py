from django.db import models
# from projects.models import ProjectService
from blog.models import BlogCategory

# Create your models here.

class NewsLetterSubscription(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    is_subscribed = models.BooleanField(default = False)
    category = models.ManyToManyField(BlogCategory, related_name='blogcategory_newsletter')
    
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name