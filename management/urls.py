from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import MultipleDelete

urlpatterns =[
    path('multiple-delete/<str:model_name>/', MultipleDelete.as_view()),
]

