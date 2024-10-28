from rest_framework import serializers
from ..models import Category

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'