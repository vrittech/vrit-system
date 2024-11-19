from django.db import models
from django.contrib.auth.models import AbstractUser
from department.models import Department
# from socialmedia.models import SocialMedia
from django.contrib.auth.models import Group

# Create your models here.
class CustomUser(AbstractUser):
    position = models.CharField(max_length = 250,null = True)
    department = models.ForeignKey(Department,null = True,on_delete = models.SET_NULL)
    email = models.EmailField(max_length = 250,unique = True)
    full_name = models.CharField(max_length = 250,null = True)
    # social_links = models.ManyToManyField(SocialMedia,blank=True)
    position = models.PositiveIntegerField(default=9999)

    avatar = models.ImageField(upload_to='profile',null=True,blank=True)
    professional_image = models.ImageField(upload_to='profile',null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username
    
    class Meta:
        permissions = [
            ('can_verify_user', 'Can verify user'),
        ]
    
    @property
    def full_name(self):
        try:
            return self.first_name + " " + self.last_name
        except:
            return self.username


class GroupExtension(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='extension')
    position = models.PositiveIntegerField(default=9999)
    
    def __int__(self):
        return self.position

    def save(self, *args, **kwargs):
        # Set position to the Group ID if position is 0 (or could be None)
        if self.position == 0:
            super().save(*args, **kwargs)  # Save initially to get the group ID
            self.position = self.group.id
            super().save(*args, **kwargs)  # Save again to update position with group ID
        else:
            super().save(*args, **kwargs)
