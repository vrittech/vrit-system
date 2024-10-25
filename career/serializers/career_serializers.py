from rest_framework import serializers
from ..models import Career,ExperienceLevel

class ExperienceLevelSerializers_Career(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = ['level_name']

class CareerListSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()
    class Meta:
        model = Career
        fields = '__all__'

class CareerRetrieveSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()
    class Meta:
        model = Career
        fields = '__all__'

class CareerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'
    
    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if Career.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data