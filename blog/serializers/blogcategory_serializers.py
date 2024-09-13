from rest_framework import serializers
from ..models import BlogCategory

class BlogCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'