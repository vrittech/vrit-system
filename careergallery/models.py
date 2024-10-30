from django.db import models

class Album(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

# Create your models here.
class CareerGallery(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(
        Album, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="career_galleries"
    )
    position = models.PositiveIntegerField(default=9999)
    media = models.ImageField(upload_to='career_gallery')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.album}"