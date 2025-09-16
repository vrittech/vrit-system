from django.db import models
from django.utils.text import slugify
from ordered_model.models import OrderedModel

from accounts.models import CustomUser

# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length = 155)
    color= models.CharField(max_length=155,blank=True,null=True)
    # is_show = models.BooleanField(default = True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name
    

class Blog(OrderedModel):
    user = models.ForeignKey(CustomUser,related_name = 'blog',on_delete=models.CASCADE)
    # author =models.CharField(max_length=150, blank=True,null=True)
    # read_time =models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length = 300,unique= True)
    description = models.TextField(blank=True,null=True)
    # site_title = models.CharField(max_length = 300, blank=True,null=True)
    # excerpt = models.CharField(max_length = 300, blank=True,null=True)
    status = models.CharField(choices = (('draft','Draft'),('published','Published'),('scheduled','Scheduled'),('deleted','Deleted')),max_length = 20,default = 'draft')
    publish_date = models.DateTimeField(null = True,blank=True)
    # meta_description = models.CharField(max_length = 1200, blank=True,null=True)
    # meta_title = models.CharField(max_length = 800, blank=True,null=True)
    # meta_keywords = models.CharField(max_length = 800, blank=True,null=True)
    # meta_author = models.CharField(max_length = 300, blank=True,null=True)
    # tags = models.ManyToManyField(BlogTags, blank=True)
    
    
    # header_code =  models.TextField(default = "", blank=True,null=True)
    # embedded_code =  models.TextField(default = "", blank=True,null=True)

    # objects = models.Manager()
    # tag_manager = TagManager()

    category = models.ManyToManyField(BlogCategory, blank= True,)
    cover_image = models.CharField(max_length=255, blank=True, null=True)
    
    # is_deleted = models.BooleanField(default= False,blank=True)

    created_at = models.DateField(auto_now_add=True)
    created_date_time=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    # public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title