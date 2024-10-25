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


class BulkExperienceLevelSerializer(serializers.Serializer):
    experience_levels = ExperienceLevelWriteSerializers(many=True)

    def create(self, validated_data):
        experience_levels_data = validated_data['experience_levels']
        experience_levels_objects = [
            ExperienceLevel(level_name=exp['level_name'])
            for exp in experience_levels_data
        ]
        return ExperienceLevel.objects.bulk_create(experience_levels_objects)

    def validate_experience_levels(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Expected a list of experience levels")
        return value