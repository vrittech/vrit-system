from django.db import models
from accounts.models import CustomUser

class BlogTags(models.Model):
    name = models.CharField(max_length = 155)

class BlogCategory(models.Model):
    name = models.CharField(max_length = 155)

# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(CustomUser,related_name = 'blogs',on_delete=models.CASCADE)
    title = models.CharField(max_length = 300)
    description = models.TextField()
    site_title = models.CharField(max_length = 300)
    excerpt = models.CharField(max_length = 300)
    is_publish = models.BooleanField(default = True)
    meta_description = models.CharField(max_length = 1200)
    meta_keywords = models.CharField(max_length = 800)
    meta_author = models.CharField(max_length = 300)
    tags = models.ManyToManyField(BlogCategory)
    category = models.ForeignKey(BlogCategory,max_length = 300,null = True,on_delete = models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

