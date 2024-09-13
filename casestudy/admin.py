from django.contrib import admin
from .models import CaseStudyCategory,CaseStudyTags,CaseStudy
# Register your models here.
admin.site.register([CaseStudy,CaseStudyCategory,CaseStudyTags])
