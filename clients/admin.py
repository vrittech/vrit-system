from django.contrib import admin
from .models import Clients,ClientSettings
# Register your models here.
admin.site.register([Clients,ClientSettings])
