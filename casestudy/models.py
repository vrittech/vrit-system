from django.db import models

class CaseStudyTags(models.Model):
    name = models.CharField(max_length = 155)

class CaseStudyCategory(models.Model):
    name = models.CharField(max_length = 155)
    image = models.ImageField(upload_to='blogcategory',null=True)

# Create your models here.
class CaseStudy(models.Model):
    title = models.CharField(max_length = 500)
    description = models.TextField()
    featured_image = models.ImageField(upload_to = 'casestudy/') 

    excerpt = models.CharField(max_length = 300)
    status = models.CharField(choices = (('draft','Draft'),('published','Published'),('scheduled','Scheduled')),max_length = 20,default = 'published')
    publish_date = models.DateField()
    is_publish = models.BooleanField(default = True)
    meta_description = models.CharField(max_length = 1200)
    meta_keywords = models.CharField(max_length = 800)
    meta_author = models.CharField(max_length = 300)
    tags = models.ManyToManyField(CaseStudyTags)
    category = models.ForeignKey(CaseStudyCategory,max_length = 300,null = True,on_delete = models.SET_NULL)
    featured_image = models.ImageField(upload_to='blog',null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

