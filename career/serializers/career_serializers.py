from rest_framework import serializers
from ..models import Career,ExprienceLevel

class ExprienceLevelSerializers_Career(serializers.ModelSerializer):
    class Meta:
        model = ExprienceLevel
        fields = ['level_name']

class CareerListSerializers(serializers.ModelSerializer):
    experience_level = ExprienceLevelSerializers_Career()
    class Meta:
        model = Career
        fields = '__all__'

class CareerRetrieveSerializers(serializers.ModelSerializer):
    experience_level = ExprienceLevelSerializers_Career()
    class Meta:
        model = Career
        fields = '__all__'

class CareerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'