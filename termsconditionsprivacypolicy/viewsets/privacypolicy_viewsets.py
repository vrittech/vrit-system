import random
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from termsconditionsprivacypolicy.models import PrivacyPolicy
from termsconditionsprivacypolicy.serializers.privacypolicy_serializers import PrivacyListSerializers, PrivacyRetrieveSerializers, PrivacyWriteSerializers
from termsconditionsprivacypolicy.utilities.permissions import privacyPolicyPermission

# from studentplacement.utilities.filter import StudentPlacementFilter
# from studentplacement.utilities.permissions import studentplacementPermission
from ..utilities.importbase import *
from rest_framework.response import Response
from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions

class PrivacyPolicyAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [privacyPolicyPermission]
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [privacyPolicyPermission()]
    #     return [DjangoModelPermissions()]

    def get(self, request):
        instance = PrivacyPolicy.objects.first()
        if not instance:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = PrivacyListSerializers(instance)
        return Response(serializer.data)

    def post(self, request):
        existing_instance = PrivacyPolicy.objects.first()
        if existing_instance:
            existing_instance.delete()
        serializer = PrivacyWriteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self, request):
        deleted_count, _ = PrivacyPolicy.objects.all().delete()
        if deleted_count == 0:
            return Response({'detail': 'No Privacy Policy found to delete.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': f'{deleted_count} Privacy Policy instance(s) deleted.'}, status=status.HTTP_200_OK)
