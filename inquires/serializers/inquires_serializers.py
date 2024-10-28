from rest_framework import serializers
from ..models import Inquires
from projects.models import ProjectService
from plan.models import Plan

# Serializer for ProjectService
class ProjectServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = '__all__' 
# Serializer for Plan
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__' 

# List Serializer
class InquiresListSerializers(serializers.ModelSerializer):
    project_service = ProjectServiceSerializer(many=True, read_only=True)
    project_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Inquires
        fields = [
            'id', 'first_name', 'last_name', 'email_address', 
            'phone_number', 'company_name', 'created_at', 'updated_at', 
            'project_service', 'project_plan'
        ]

# Retrieve Serializer
class InquiresRetrieveSerializers(serializers.ModelSerializer):
    project_service = ProjectServiceSerializer(many=True, read_only=True)
    project_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Inquires
        fields = [
            'id', 'first_name', 'last_name', 'email_address', 
            'phone_number', 'company_name', 'project_detail',
            'created_at', 'updated_at', 'project_service', 'project_plan'
        ]

# Write Serializer
class InquiresWriteSerializers(serializers.ModelSerializer):
    project_service = serializers.PrimaryKeyRelatedField(
        queryset=ProjectService.objects.all(), many=True
    )
    project_plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), allow_null=True
    )

    class Meta:
        model = Inquires
        fields = [
            'id', 'first_name', 'last_name', 'email_address', 
            'phone_number', 'company_name', 'project_detail', 
            'project_service', 'project_plan'
        ]

    def create(self, validated_data):
        project_services = validated_data.pop('project_service', [])
        inquires = Inquires.objects.create(**validated_data)
        inquires.project_service.set(project_services)
        return inquires

    def update(self, instance, validated_data):
        project_services = validated_data.pop('project_service', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.project_service.set(project_services)
        return instance
