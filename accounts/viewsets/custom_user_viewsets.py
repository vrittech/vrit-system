from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..serializers.custom_user_serializers import CustomUserReadSerializer, CustomUserWriteSerializer, CustomUserRetrieveSerializer
from rest_framework.response import Response
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list']:
            return CustomUserReadSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomUserWriteSerializer
        elif self.action in ['retrieve']:
            return CustomUserRetrieveSerializer
        return CustomUserReadSerializer


