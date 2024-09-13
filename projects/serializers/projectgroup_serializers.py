from rest_framework import serializers
from ..models import ProjectGroup

class ProjectGroupListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = '__all__'

class ProjectGroupRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = '__all__'

class ProjectGroupWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = '__all__'