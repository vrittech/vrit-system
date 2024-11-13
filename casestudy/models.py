from django.db import models
from accounts.models import CustomUser
import ast
from django.utils import timezone
from django.utils.text import slugify
import uuid
class CaseStudyTags(models.Model):
    name = models.CharField(max_length = 155)
    
    def __str__(self):
        return self.name

    

class CaseStudyCategory(models.Model):
    name = models.CharField(max_length = 155)
    media = models.ImageField(upload_to='case_studycategory',null=True)
    is_show = models.BooleanField(default = True)
    
    def __str__(self):
        return self.name


class TagManager(models.Manager):
    def get_or_create_tags(self, tag_names):
        """
        Create or retrieve Tag objects based on tag names.
        Accepts a list of tag names or a string representation of a list.
        """
        # Check if tag_names is a string and parse it if needed
        if isinstance(tag_names, str):
            try:
                tag_names = ast.literal_eval(tag_names)
            except (ValueError, SyntaxError) as e:
                raise ValueError(f"Invalid format for tag names: {tag_names}") from e
        
        # Now, tag_names should be a list. If it's not, raise an error
        if not isinstance(tag_names, list):
            raise ValueError("tag_names must be a list of strings")

        # Create or retrieve Tag objects
        tags = [CaseStudyTags.objects.get_or_create(name=tag)[0] for tag in tag_names]
        return tags

# 27.67304441065, 85.33306299012784

class CaseStudy(models.Model):
    user = models.ForeignKey(CustomUser,related_name = 'case_study',on_delete=models.CASCADE,null=True)
    author =models.CharField(max_length=150, blank=True)
    read_time =models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length = 300)
    description = models.TextField()
    site_title = models.CharField(max_length = 300,null=True,blank=True)
    excerpt = models.CharField(max_length = 300)
    status = models.CharField(choices = (('draft','Draft'),('published','Published'),('scheduled','Scheduled'),('deleted','Deleted')),max_length = 20,default = 'draft')
    publish_date = models.DateField(null=True,blank=True)
    meta_description = models.CharField(max_length = 1200)
    meta_keywords = models.CharField(max_length = 800)
    meta_author = models.CharField(max_length = 300)
    tags = models.ManyToManyField(CaseStudyTags)
    position = models.PositiveIntegerField(default= 9999)
    
    
    header_code =  models.TextField(default = "")
    embedded_code =  models.TextField(default = "")

    objects = models.Manager()
    tag_manager = TagManager()

    category = models.ManyToManyField(CaseStudyCategory,blank= True)
    featured_image = models.ImageField(upload_to='case_study',null = True)
    
    is_deleted = models.BooleanField(default= False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title
    
    def publish_if_scheduled(self):
        if self.status == 'scheduled' and self.publish_date <= timezone.now().date():
            self.status = 'published'
            self.save()

    @classmethod
    def publish_scheduled_case_study(cls):
        scheduled_case_study = cls.objects.filter(status='scheduled', publish_date__lte=timezone.now().date())
        for case_study in scheduled_case_study:
            case_study.publish_if_scheduled()

