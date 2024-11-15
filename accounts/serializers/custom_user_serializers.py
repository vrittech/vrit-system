from rest_framework import serializers
from django.contrib.auth import get_user_model
from department.models import Department
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import check_password, make_password


User = get_user_model()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "group"
        model = Permission
        fields = ['id', 'name', 'codename']
        
class GroupSerializer(serializers.ModelSerializer):
    # permissions = PermissionSerializer(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ['id', 'name']
        ref_name='user_groups'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']

class CustomUserReadSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only = True)
    groups = GroupSerializer(many=True,read_only = True)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)
        
    

class CustomUserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password','department']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True,read_only = True)
    department = DepartmentSerializer(read_only = True)
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password',)


class CustomUserChangePasswordSerializers(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        # Check if current password is correct
        if not check_password(data['current_password'], user.password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect"})
        return data

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value

   