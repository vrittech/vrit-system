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