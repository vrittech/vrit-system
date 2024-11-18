from django.db import models

# Create your models here.

class Gallery(models.Model):
    name = models.CharField(max_length=150,null =  True,blank = True)
    media = models.ImageField(upload_to="gallery")
    
    def __str__(self):
        return self.name
    class Meta:
        permissions = [
            ('manage_gallery', 'Manage Gallery'),
        ]