from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import ClientSettings
from ..serializers.clientsettings_serializers import (
    ClientSettingsListSerializers, 
    ClientSettingsRetrieveSerializers, 
    ClientSettingsWriteSerializers, 
    BulkClientSettingsSerializer
)
from ..utilities.importbase import *


class clientsettingsViewsets(viewsets.ModelViewSet):
    queryset = ClientSettings.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Add any custom filtering logic here if needed
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return BulkClientSettingsSerializer
        elif self.action in ['update', 'partial_update']:
            return ClientSettingsWriteSerializers
        elif self.action == 'retrieve':
            return ClientSettingsRetrieveSerializers
        return ClientSettingsListSerializers

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to handle bulk creation of client settings.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Settings saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
