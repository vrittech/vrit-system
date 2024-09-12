from django.db import models
from projects.models import ProjectService

# Create your models here.

class NewsLetterSubscription(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    service = models.ManyToManyField(ProjectService,related_name="newslettersubscription")
    date = models.DateField()