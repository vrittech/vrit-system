from rest_framework import serializers
from ..models import ProjectLink

class ProjectLinkListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = '__all__'

class ProjectLinkRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = '__all__'

class ProjectLinkWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = '__all__'