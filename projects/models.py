from django.db import models
from casestudy.models import CaseStudy


class ProjectGroup(models.Model):
    name = models.CharField(max_length = 155)
    position = models.PositiveIntegerField(default=9999)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProjectService(models.Model):
    name = models.CharField(max_length = 155)
    description = models.TextField()
    media = models.ImageField(upload_to="service",null=True,blank=True)
    position = models.PositiveIntegerField(default=9999)
    is_feature= models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 

class ProjectLink(models.Model):
    # project_link = models.ForeignKey(Project,on_delete = models.CASCADE,related_name = 'project')
    label = models.CharField(max_length = 155)
    url = models.URLField(max_length = 2000)

    def __str__(self):
        return self.label



# Create your models here.
class Project(models.Model):
    # image = models.ImageField(upload_to='project',null=True,blank=True)
    name = models.CharField(max_length = 600)
    position = models.PositiveIntegerField(default=9999)
    description = models.TextField()
    group = models.ForeignKey(ProjectGroup,on_delete = models.SET_NULL ,null = True,related_name="projects")
    project_service = models.ManyToManyField(ProjectService,related_name="project_services")
    project_link = models.ManyToManyField(ProjectLink,related_name="project_link")
    case_study = models.ForeignKey(CaseStudy,on_delete = models.SET_NULL ,null = True,related_name="project_case")

    media = models.ImageField(upload_to="project",null=True,blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __self__(self):
        return self.name


    
