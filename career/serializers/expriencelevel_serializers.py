from rest_framework import serializers
from ..models import ExperienceLevel

class ExperienceLevelListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = '__all__'

class ExperienceLevelRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = '__all__'

class ExperienceLevelWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = '__all__'