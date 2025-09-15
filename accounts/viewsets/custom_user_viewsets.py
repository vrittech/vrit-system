from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from ..serializers.custom_user_serializers import CustomUserReadSerializer, CustomUserWriteSerializer, CustomUserRetrieveSerializer,CustomUserChangePasswordSerializers
from rest_framework.response import Response
from accounts.models import CustomUser
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from accounts.utilities.filters import CustomUserFilter
# accounts/utilities/filters.py
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..utilities.permissions import accountsPermission
from collections import defaultdict
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('position')
    # permission_classes = [permissions.IsAuthenticated]
    filterset_class = CustomUserFilter
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    
    search_fields = ['position', 'department', 'email', 'full_name','first_name','last_name']
    ordering_fields =['position', 'department' , 'email', 'full_name','first_name','last_name']

    def get_serializer_class(self):
        if self.action in ['list']:
            return CustomUserReadSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return CustomUserWriteSerializer
        elif self.action in ['retrieve']:
            return CustomUserRetrieveSerializer
        elif self.action in ['changePassword']:
            return CustomUserChangePasswordSerializers
        return CustomUserReadSerializer
    
    @action(detail=False, methods=['post'], name="changePassword", url_path="change-password")
    def changePassword(self, request, *args, **kwargs):
        serializer = CustomUserChangePasswordSerializers(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user  # Get the current authenticated user
            user.set_password(serializer.validated_data['new_password'])  # Hash and set the new password
            user.save()  # Save the updated user instance
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # @action(detail=False, methods=['get'], name="GetSelfDetail", url_path="me")
    # def GetSelfDetail(self, request, *args, **kwargs):
    #     self.object = request.user  # Set the object directly to the current user
    #     serializer = self.get_serializer(self.object)
    #     return Response(serializer.data)
    @action(detail=False, methods=['get'], name="GetSelfDetail", url_path="me")
    def GetSelfDetail(self, request, *args, **kwargs):
        # self.object = request.user  # Set the object directly to the current user
        # serializer = self.get_serializer(self.object)
        # return Response(serializer.data)
        self.object = request.user
        serializer = self.get_serializer(self.object)
        data = serializer.data

        # --- BEGIN models_with_permission logic ---
        ACTION_MAP = {
            'add_': 'Add',
            'change_': 'Edit',
            'delete_': 'Delete',
            'view_': 'View',
        }

        forced_models = {
            
        }
        # Extra forced models for superuser
        superuser_forced_models = {
            "blog","branding","career","certificate",
            "course","faqs","industryallies",
            "journey","mentors","moments","privacypolicy",
            "successstory","termsconditions","testimonial","forms","teammember","custompage", "studentplacement", "popup", "advertisement",
            "payment","invoice","enrollment","branding","templates","student","contactus","requestform","studentplacement","group","custompage", "customgallery", "modelactivitylog" # <-- add your superuser-only models here
        }

        # Gather permissions from all groups the user belongs to
        group_perms = set()
        for group in request.user.groups.all():
            group_perms.update(group.permissions.all())

        model_actions = defaultdict(set)

        for perm in group_perms:
            app_label = perm.content_type.app_label
            codename = perm.codename
            model = perm.content_type.model

            if model in forced_models or perm in group_perms:
                action = next(
                    (label for prefix, label in ACTION_MAP.items() if codename.startswith(prefix)),
                    None
                )
                if action:
                    model_actions[model].add(action)

        # Ensure forced models are present
        for model in forced_models:
            model_actions.setdefault(model, set())

        # Add superuser-only models if user is superuser
        if request.user.is_superuser:
            for model in superuser_forced_models:
                model_actions.setdefault(model, set())

        permissions_data = [
            {"name": model, "actions": sorted(actions)}
            for model, actions in sorted(model_actions.items())
        ]
        # --- END models_with_permission logic ---

        # Merge into final response
        data["models_with_permission"] = permissions_data

        return Response(data)