from django.contrib import admin
from .models import Project,ProjectGroup,ProjectLink,ProjectService
# Register your models here.

admin.site.register([ProjectGroup,ProjectService,ProjectLink,Project])


# class ProjectLink(admin.TabularInline):
#     model = ProjectLink

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     inlines = [ProjectLink]
#     list_display = ['name']
 