from django.db import models

# Create your models here.


class Faqs(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    position= models.BigIntegerField(default=9999)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title})"

