from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import SiteSetting
from ..serializers.sitesetting_serializers import (
    SiteSettingListSerializers,
    SiteSettingRetrieveSerializers,
    SiteSettingWriteSerializers
)
from django_filters.rest_framework import DjangoFilterBackend

class sitesettingViewsets(viewsets.ViewSet):
    """
    This ViewSet is designed to manage a single instance of SiteSetting.
    """
    def get_object(self):
        # Retrieve the single SiteSetting instance or return 404 if not found
        obj = SiteSetting.objects.first()
        if obj is None:
            self.create_initial_object()
            obj = SiteSetting.objects.first()
        return obj

    def create_initial_object(self):
        # Create an initial object if none exists
        if SiteSetting.objects.count() == 0:
            SiteSetting.objects.create(
                experience_number=0,
                success_stories_number=0,
                team_member_number=0,
                project_completed_number=0
            )

    def list(self, request):
        obj = self.get_object()
        serializer = SiteSettingListSerializers(obj)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        obj = self.get_object()
        serializer = SiteSettingRetrieveSerializers(obj)
        return Response(serializer.data)

    def create(self, request):
        if SiteSetting.objects.exists():
            return Response(
                {"detail": "SiteSetting already exists. Use PUT or PATCH to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SiteSettingWriteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        obj = self.get_object()
        serializer = SiteSettingWriteSerializers(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        obj = self.get_object()
        serializer = SiteSettingWriteSerializers(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
