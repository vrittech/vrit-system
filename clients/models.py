from django.db import models

# Create your models here.

class Clients(models.Model):
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default = 33)
    media = models.ImageField(upload_to="clients")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ClientSettings(models.Model):
    client = models.ManyToManyField(Clients)
    section = models.CharField(choices = (('first','First'),('second','Second'),('third','Third'),('fourth','Fourth')),max_length = 20)
    loop_type = models.CharField(choices = (('forward','Forward'),('reverse','Fourth')),max_length = 20)
    delay_time =  models.TimeField()



