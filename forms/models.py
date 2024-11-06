from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class Forms(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='forms')
    description = models.TextField()
    header_code = models.TextField(blank=True, null=True)
    embedded_code = models.TextField(blank=True, null=True)
    media = models.ImageField(upload_to='forms', blank=True, null=True)
    excerpt = models.CharField(max_length=500, blank=True, null=True)
    auto_expiration = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    auto_expiration_date = models.DateField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically mark as expired if the expiration date has passed
        if self.auto_expiration and self.auto_expiration_date:
            from datetime import date
            if date.today() > self.auto_expiration_date:
                self.is_expired = True
        super().save(*args, **kwargs)
