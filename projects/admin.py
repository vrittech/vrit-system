from django.contrib import admin
from .models import Project,ProjectGroup,ProjectLink,ProjectService
# Register your models here.

admin.site.register([ProjectGroup,ProjectService])


class ProjectHaveLink(admin.TabularInline):
    model = ProjectLink

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectHaveLink]
    list_display = ['name']
 