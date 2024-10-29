from django.urls import path
from .viewsets.email_tags_api import EmailTags

urlpatterns = [
    path('email-tags/<str:tag_type>/',EmailTags.as_view(),name="EmailTags")
]