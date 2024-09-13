from django.contrib import admin
from .models import EmailManagement,EmailSetup
# Register your models here.

admin.site.register([EmailManagement,EmailSetup])
