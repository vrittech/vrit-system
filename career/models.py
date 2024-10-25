from django.db import models

# Create your models here.

class ExperienceLevel(models.Model):
    level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Career(models.Model):
    title = models.CharField(max_length = 400)
    experience_level = models.ForeignKey(ExperienceLevel,on_delete = models.SET_NULL,related_name = 'careers',null = True)
    description = models.TextField()
    position = models.PositiveIntegerField(default=9999)
    num_of_vacancy = models.PositiveIntegerField(default = 1)
    apply_link = models.URLField(max_length = 500)
    image = models.ImageField(upload_to='career')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    enable_auto_expiration = models.BooleanField(default = True)
    expiration_date = models.DateTimeField()
    
    

