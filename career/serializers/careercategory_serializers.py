from rest_framework import serializers
from ..models import CareerCategory, ExperienceLevel

class CareerCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CareerCategory
        fields = '__all__'

class CareerCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CareerCategory
        fields = '__all__'

class CareerCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CareerCategory
        fields = '__all__'

