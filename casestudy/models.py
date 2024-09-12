from django.db import models

class CaseStudyTags(models.Model):
    name = models.CharField(max_length = 155)

class CaseStudyCategory(models.Model):
    name = models.CharField(max_length = 155)

# Create your models here.
class CaseStudy(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField()
    featured_image = models.ImageField(upload_to = 'casestudy/') 

    excerpt = models.CharField(max_length = 300)
    is_publish = models.BooleanField(default = True)
    meta_description = models.CharField(max_length = 1200)
    meta_keywords = models.CharField(max_length = 800)
    meta_author = models.CharField(max_length = 300)
    tags = models.ManyToManyField(CaseStudyTags)
    category = models.ForeignKey(CaseStudyCategory,max_length = 300,null = True,on_delete = models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

