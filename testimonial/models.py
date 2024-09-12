from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Testimonial(models.Model):
    full_name = models.CharField(max_length = 155)
    role =  models.CharField(max_length = 155)
    ratings = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    image = models.ImageField(upload_to="testimonial")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
