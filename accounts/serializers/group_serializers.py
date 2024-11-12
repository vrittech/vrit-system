from rest_framework import serializers
from django.contrib.auth.models import Permission
from ..models import CustomGroup

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "group"
        model = Permission
        fields = ['id', 'name', 'codename']

class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    position = serializers.IntegerField(required=False)

    class Meta:
        model = CustomGroup  # Updated to use CustomGroup
        fields = ['id', 'name', 'permissions', 'permission_ids', 'position']

    def create(self, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        group = CustomGroup.objects.create(**validated_data)
        group.permissions.set(permission_ids)
        return group

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', [])
        instance.name = validated_data.get('name', instance.name)
        instance.position = validated_data.get('position', instance.position)
        instance.save()
        instance.permissions.set(permission_ids)
        return instance
