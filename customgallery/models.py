from django.db import models

# Create your models here.
types = (
        ('homepage', 'Homepage'),
        ('services', 'Services'),
        ('career', 'Career'),
        ('about_us', 'About Us'),
    )


class Position(models.Model):
    type = models.CharField(max_length=10, choices=types, blank=True,null=True)
    position= models.CharField(max_length = 500 , null = True,blank = True)

    def __str__(self) -> str:
        return f"{str(self.type)} : {self.position}"



class CustomGallery(models.Model):
    # name = models.CharField(max_length = 500 , null = True,blank = True)
    is_static=models.BooleanField(default=False, blank=True)
    # static_type = models.CharField(max_length=10, choices=types, blank=True,null=True)
    image = models.FileField(max_length = 500,upload_to = 'gallery/images')
    position = models.ForeignKey(Position,blank=True,null=True, on_delete=models.SET_NULL)
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self) -> str:
        return f"{str(self.created_date)}"

