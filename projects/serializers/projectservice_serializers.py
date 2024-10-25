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
    
    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if ProjectService.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data