from rest_framework import serializers
from ..models import Department

class DepartmentListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'