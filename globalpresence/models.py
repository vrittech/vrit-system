from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class GlobalPresence(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="global_presences")
    company_name = models.CharField(max_length=350)
    company_address = models.CharField(max_length=500)
    email_address = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=150)
    media = models.ImageField(upload_to="globalpresence")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.company_name
    
    class Meta:
        permissions = [
            ('manage_global_presence', 'Manage Global Presence'),
        ]
