from django.contrib import admin
from .models import Project,ProjectGroup,ProjectLink,ProjectService
# Register your models here.

admin.site.register(Project,ProjectGroup,ProjectLink,ProjectService)
