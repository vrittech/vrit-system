from django.db import models
# from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import CustomUser

# User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    module_name = models.CharField(max_length=100)
    users = models.ManyToManyField(CustomUser, related_name="notifications")
    updated_id = models.CharField(max_length=255, blank=True, null=True)  # New field

    def __str__(self):
        return f"{self.title} - {self.module_name}"
    
    class Meta:
        permissions = [
            ('manage_notification', 'Manage Notification'),
        ]

    