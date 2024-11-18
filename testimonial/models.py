from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Testimonial(models.Model):
    full_name = models.CharField(max_length = 155)
    role =  models.CharField(max_length = 155)
    position = models.PositiveIntegerField(default = 9999)
    ratings = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    testimonial = models.TextField()
    media = models.ImageField(upload_to="testimonial")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name})"
    class Meta:
        permissions = [
                ('manage_testimonial', 'Manage Testimonial'),
            ]


