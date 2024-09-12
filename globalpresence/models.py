from django.db import models

# Create your models here.
class GlobalPresence(models.Model):
    world_location = models.URLField(max_length = 2000)
    company_name = models.CharField(max_length = 350)
    company_address = models.CharField(max_length=500)
    email_address = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length = 150)
    image = models.ImageField(upload_to="globalpresence")
