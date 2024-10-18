from rest_framework import serializers
from ..models import Project,ProjectService

class ServicesSerializers_Project(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = ['name']

class ProjectListSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectRetrieveSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'