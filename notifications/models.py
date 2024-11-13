from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name="notifications")
    module_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.module_name}"
