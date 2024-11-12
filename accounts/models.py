from django.db import models
from django.contrib.auth.models import AbstractUser
from department.models import Department
from django.contrib.auth.models import Group

# Create your models here.
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='profile',null=True,blank=True)
    professional_image = models.ImageField(upload_to='profile',null=True,blank=True)

    full_name = models.CharField(max_length = 250)
    position = models.CharField(max_length = 250,null = True)
    department = models.ForeignKey(Department,null = True,on_delete = models.SET_NULL)
    position = models.CharField(max_length = 250)
    email = models.EmailField(max_length = 250,unique = True)


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




class CustomGroup(Group):
    position = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        # Call the original save method to get an ID assigned
        super().save(*args, **kwargs)
        
        # Set position to the ID if it hasn't been set
        if self.position == 0:  # or self.position is None, depending on your preference
            self.position = self.id
            # Save again to update the position
            super().save(*args, **kwargs)
    
    def __str__(self):
        return self.position
