from django.db import models
from accounts.models import CustomUser


# Create your models here.
class SocialMedia(models.Model):
    name = models.CharField(max_length = 255,unique =  True)
    url = models.URLField(max_length = 255,unique =  True)
    media = models.ImageField(upload_to="social_media")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    position = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
    
    permissions = [
            ('manage_social_media', 'Manage Social Media'),
        ]

class StaffHaveSocialMedia(models.Model):
    staff = models.ForeignKey(CustomUser,related_name ="user"  , on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    social_media_url = models.URLField(max_length = 350)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.social_media_url

    class Meta:
        unique_together = ('staff', 'social_media')
        
        permissions = [
            ('manage_staff_social_media', 'Manage Staff Soial Media'),
        ]


        
class SiteSocialMedia(models.Model):
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    social_media_url = models.URLField(max_length = 350)
    
    permissions = [
            ('manage_site_social_media', 'Manage Site Social Media'),
        ]



