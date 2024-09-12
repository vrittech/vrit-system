from django.db import models

# Create your models here.

class Gallery(models.Model):
    name = models.CharField(max_length=150,null =  True,blank = True)
    image = models.ImageField(upload_to="gallery")
    