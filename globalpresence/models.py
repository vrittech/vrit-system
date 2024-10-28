from django.db import models

# Create your models here.
class GlobalPresence(models.Model):
    global_presence = models.CharField(max_length = 350)
    company_name = models.CharField(max_length = 350)
    company_address = models.CharField(max_length=500)
    email_address = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length = 150)
    image = models.ImageField(upload_to="globalpresence")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
