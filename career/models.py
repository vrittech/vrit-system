from django.db import models

# Create your models here.

class ExprienceLevel(models.Model):
    level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Career(models.Model):
    title = models.CharField(max_length = 400)
    experience_level = models.ForeignKey(ExprienceLevel,on_delete = models.SET_NULL,related_name = 'careers',null = True)
    description = models.TextField()
    num_of_vacancy = models.PositiveIntegerField(default = 1)
    image = models.ImageField(upload_to='career')
    apply_link = models.URLField(max_length = 500)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

