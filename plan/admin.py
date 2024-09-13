from django.contrib import admin
from .models import Features,Plan,PlanHaveFeatures
# Register your models here.
admin.site.register([Features,Plan,PlanHaveFeatures])