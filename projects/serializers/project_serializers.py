from rest_framework import serializers
from ..models import Project

class ProjectListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'