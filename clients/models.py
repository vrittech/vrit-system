from django.db import models
from django.utils.text import slugify
import uuid

class Clients(models.Model):
    SECTION_CHOICES = [
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('fourth', 'Fourth'),
    ]

    name = models.CharField(max_length=100)
    section = models.CharField(choices=SECTION_CHOICES, max_length=20, default='first')
    media = models.ImageField(upload_to="clients",null=True,blank=True)
    position= models.PositiveIntegerField(default = 9999)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.name)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ClientSettings(models.Model):
    SECTION_CHOICES = [
        ('first', 'First'),
        ('second', 'Second'),
        ('third', 'Third'),
        ('fourth', 'Fourth'),
    ]
     
    LOOP_TYPE_CHOICES = [
        ('forward', 'Forward'),
        ('reverse', 'Reverse'),
    ]

    # client = models.ManyToManyField(Clients, related_name='ClientSettings')
    section = models.CharField(choices= SECTION_CHOICES, max_length=20)
    loop_type = models.CharField(choices=LOOP_TYPE_CHOICES, max_length=20)
    delay_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.section}: {self.loop_type} ({self.delay_time})"

