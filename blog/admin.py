from django.contrib import admin
from blog.models import Blog,BlogTags,BlogCategory

# Register your models here.
admin.site.register([Blog,BlogTags,BlogCategory])
