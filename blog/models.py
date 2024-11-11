from django.db import models
from accounts.models import CustomUser
import ast
from django.utils import timezone
import uuid
from django.utils.text import slugify

class BlogTags(models.Model):
    name = models.CharField(max_length = 155)
    
    def __str__(self):
        return self.name

    

class BlogCategory(models.Model):
    name = models.CharField(max_length = 155)
    media = models.ImageField(upload_to='blogcategory',null=True)
    is_show = models.BooleanField(default = True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return self.name


class TagManager(models.Manager):
    def get_or_create_tags(self, tag_names):
        # Create or retrieve Tag objects based on tag names
        # tag_names = tag_names.split(',')
        tag_names = ast.literal_eval(tag_names)
        tags = [BlogTags.objects.get_or_create(name=tag)[0] for tag in tag_names]
        return tags

# 27.67304441065, 85.33306299012784

class Blog(models.Model):
    user = models.ForeignKey(CustomUser,related_name = 'blogs',on_delete=models.CASCADE)
    title = models.CharField(max_length = 300,unique= True)
    description = models.TextField()
    site_title = models.CharField(max_length = 300)
    excerpt = models.CharField(max_length = 300)
    status = models.CharField(choices = (('draft','Draft'),('published','Published'),('scheduled','Scheduled')),max_length = 20,default = 'published')
    publish_date = models.DateField()
    meta_description = models.CharField(max_length = 1200)
    meta_keywords = models.CharField(max_length = 800)
    meta_author = models.CharField(max_length = 300)
    tags = models.ManyToManyField(BlogTags)
    position = models.PositiveIntegerField(default= 9999)
    
    
    header_code =  models.TextField(default = "")
    embedded_code =  models.TextField(default = "")

    objects = models.Manager()
    tag_manager = TagManager()

    category = models.ManyToManyField(BlogCategory)
    featured_image = models.ImageField(upload_to='blog',null = True)
    
    is_deleted = models.BooleanField(default= False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}'
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    
    def publish_if_scheduled(self):
        if self.status == 'scheduled' and self.publish_date <= timezone.now().date():
            self.status = 'published'
            self.save()

    @classmethod
    def publish_scheduled_blogs(cls):
        scheduled_blogs = cls.objects.filter(status='scheduled', publish_date__lte=timezone.now().date())
        for blog in scheduled_blogs:
            blog.publish_if_scheduled()

