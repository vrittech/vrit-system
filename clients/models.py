from django.db import models

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
        return f"{self.client} - {self.section}: {self.loop_type} ({self.delay_time})"

