from django.db import models


class ProjectGroup(models.Model):
    name = models.CharField(max_length = 155)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class ProjectService(models.Model):
    name = models.CharField(max_length = 155)
    description = models.TextField()
    image = models.ImageField(upload_to="service",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 


# Create your models here.
class Project(models.Model):
    image = models.ImageField(upload_to='project',null=True,blank=True)
    name = models.CharField(max_length = 600)
    description = models.TextField()
    group = models.ForeignKey(ProjectGroup,on_delete = models.SET_NULL ,null = True,related_name="projects")
    project_service = models.ManyToManyField(ProjectService,related_name="projects")

    media = models.ImageField(upload_to="project",null=True,blank=True)
 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __self__(self):
        return self.name

class ProjectLink(models.Model):
    project = models.ForeignKey(Project,on_delete = models.CASCADE,related_name = 'project')
    name = models.CharField(max_length = 155)
    url = models.URLField(max_length = 2000)

    def __str__(self):
        return self.name

    
