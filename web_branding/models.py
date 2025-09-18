from django.db import models
from ordered_model.models import OrderedModel

# # Create your models here.
class WebBrandingCategory(OrderedModel):
    name = models.CharField(max_length = 155)
    color= models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.name



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



class WebBranding(models.Model):
    name = models.CharField(max_length = 500 , null = True,blank = True)
    # is_static=models.BooleanField(default=False, blank=True)
    type = models.CharField(max_length=10, choices=types, blank=True,null=True)
    image = models.CharField(blank=True, null=True)
    video_thumbnail=models.CharField(blank=True, null=True)
    # video_thumbnail = models.FileField(
    #     max_length=500,
    #     upload_to='gallery/images',
    #     blank=True,
    #     null=True
    # )
    position = models.ForeignKey(Position,blank=True,null=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(
        WebBrandingCategory,
        related_name="CustomGallery",
        blank=True
    )
    created_date = models.DateField(auto_now_add=True, null = True,blank = True)
    created_date_time = models.DateTimeField(auto_now_add=True, null = True,blank = True)
    updated_date_time = models.DateTimeField(auto_now=True, null = True,blank = True)
    
    def __str__(self) -> str:
        return f"{str(self.created_date)}"

