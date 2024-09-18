from django.db import models
from accounts.models import CustomUser


# Create your models here.
class SocialMedia(models.Model):
    name = models.CharField(max_length = 255,unique =  True)
    url = models.URLField(max_length = 255,unique =  True)

class StaffHaveSocialMedia(models.Model):
    staff = models.ForeignKey(CustomUser,related_name ="user"  , on_delete=models.CASCADE)
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    social_media_url = models.URLField(max_length = 350)

    class Meta:
        unique_together = ('staff', 'social_media')

class SiteSocialMedia(models.Model):
    social_media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    social_media_url = models.URLField(max_length = 350)


