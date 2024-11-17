from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    media = models.ImageField(upload_to="gallery",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

