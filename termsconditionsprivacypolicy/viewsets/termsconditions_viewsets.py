import random
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from termsconditionsprivacypolicy.models import TermsConditions
from termsconditionsprivacypolicy.serializers.termsconditions_serializers import TermsConditionsListSerializers, TermsConditionsRetrieveSerializers, TermsConditionsWriteSerializers
from termsconditionsprivacypolicy.utilities.permissions import termsConditionsPermission

# from studentplacement.utilities.filter import StudentPlacementFilter
# from studentplacement.utilities.permissions import studentplacementPermission
from ..utilities.importbase import *
from rest_framework.response import Response
from django.db.models import F, Value
from django.db.models.functions import Concat
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import DjangoModelPermissions


class TermsConditionsAPIView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_classes = [termsConditionsPermission]

    def get(self, request):
        instance = TermsConditions.objects.first()
        if not instance:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        serializer = TermsConditionsListSerializers(instance)
        return Response(serializer.data)

    def post(self, request):
        existing_instance = TermsConditions.objects.first()
        if existing_instance:
            existing_instance.delete()
        serializer = TermsConditionsWriteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



