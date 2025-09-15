from rest_framework import serializers
from ..models import Blog, BlogCategory


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


class BlogsListSerializers(serializers.ModelSerializer):
    category= BlogCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Blog
        fields = '__all__'

class BlogsRetrieveSerializers(serializers.ModelSerializer):
    category= BlogCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Blog
        fields = '__all__'

class BlogsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


    
