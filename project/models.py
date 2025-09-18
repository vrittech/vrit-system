from django.db import models
from ordered_model.models import OrderedModel
from django.utils.text import slugify
# Create your models here.

class ProjectCategory(OrderedModel):
    name = models.CharField(max_length = 155)
    color= models.CharField(max_length=255, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self) -> str:
        return self.name
    
class Project(OrderedModel):
    name = models.CharField(max_length=255)
    cover_image = models.CharField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(
        ProjectCategory,
        related_name="project",
        blank=True
    )

    slug = models.SlugField(max_length=255, blank=True)

    link = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.slug:  # FE sent slug
            base_slug = slugify(self.slug)
        else:  # FE didn't send, make from name
            base_slug = slugify(self.name)

        slug = base_slug
        counter = 1
        while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}{counter}"
            counter += 1
        self.slug = slug

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name})"
    

class CaseStudy(OrderedModel):
    project= models.OneToOneField(Project,blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Case Study ({self.id})"


    
