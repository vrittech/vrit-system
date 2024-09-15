from django.db import models
from accounts.models import CustomUser
import ast

class BlogTags(models.Model):
    name = models.CharField(max_length = 155)

class BlogCategory(models.Model):
    name = models.CharField(max_length = 155)

class TagManager(models.Manager):
    def get_or_create_tags(self, tag_names):
        # Create or retrieve Tag objects based on tag names
        # tag_names = tag_names.split(',')
        tag_names = ast.literal_eval(tag_names)
        tags = [BlogTags.objects.get_or_create(name=tag)[0] for tag in tag_names]
        return tags

# 27.67304441065, 85.33306299012784
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
    tags = models.ManyToManyField(BlogTags)

    objects = models.Manager()
    tag_manager = TagManager()

    category = models.ManyToManyField(BlogCategory,related_name="blogs")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

