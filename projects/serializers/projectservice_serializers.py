from rest_framework import serializers
from ..models import ProjectService

class ProjectServiceListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = '__all__'

class ProjectServiceRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = '__all__'

class ProjectServiceWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = '__all__'