from django.db import models

from accounts.models import CustomUser

class NotificationPerUser(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    module_name = models.CharField(max_length=100)
    updated_id = models.CharField(max_length=255, blank=True, null=True)  # new field

    def __str__(self):
        return f"{self.title} - {self.module_name}"

    class Meta:
        permissions = [
            ('manage_notification', 'Manage Notification'),
        ]

class NotificationUser(models.Model):
    notification = models.ForeignKey(NotificationPerUser, on_delete=models.CASCADE, related_name='notification_users')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('notification', 'user')