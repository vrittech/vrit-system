from rest_framework import serializers
from ..models import ProjectGroup

class ProjectGroupListSerializers(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = ProjectGroup
        fields = '__all__'  # or specify fields manually if needed, e.g., ['id', 'name', 'project_count', ...]

    def get_project_count(self, obj):
        return obj.projects.count()


class ProjectGroupRetrieveSerializers(serializers.ModelSerializer):
    project_count = serializers.SerializerMethodField()

    class Meta:
        model = ProjectGroup
        fields = '__all__'

    def get_project_count(self, obj):
        return obj.projects.count()


class ProjectGroupWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        fields = '__all__'
