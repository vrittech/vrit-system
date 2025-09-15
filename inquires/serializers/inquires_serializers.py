from rest_framework import serializers

from services.models import Services
from ..models import Inquires
from projects.models import ProjectService
from plan.models import Plan

# Serializer for ProjectService
class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__' 
# Serializer for Plan
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__' 

# List Serializer
class InquiresListSerializers(serializers.ModelSerializer):
    services = ServicesSerializer(many=True, read_only=True)
    project_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Inquires
        fields = [
            'id', 'full_name', 'email_address', 
            'phone_number', 'company_name', 'created_at', 'updated_at', 'created_date',
            'services', 'project_plan'
        ]

# Retrieve Serializer
class InquiresRetrieveSerializers(serializers.ModelSerializer):
    services = ServicesSerializer(many=True, read_only=True)
    project_plan = PlanSerializer(read_only=True)

    class Meta:
        model = Inquires
        fields = [
            'id', 'full_name', 'email_address', 
            'phone_number', 'company_name', 'project_detail',
            'created_at', 'updated_at', 'created_date', 'services', 'project_plan'
        ]

# Write Serializer
class InquiresWriteSerializers(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Services.objects.all(), many=True
    )
    project_plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), allow_null=True
    )

    class Meta:
        model = Inquires
        fields = [
            'id', 'full_name', 'email_address', 
            'phone_number', 'company_name', 'project_detail', 
            'services', 'project_plan'
        ]

    def create(self, validated_data):
        services = validated_data.pop('services', [])
        inquires = Inquires.objects.create(**validated_data)
        inquires.services.set(services)
        return inquires

    def update(self, instance, validated_data):
        services = validated_data.pop('services', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.services.set(services)
        return services
