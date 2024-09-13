from rest_framework import serializers
from ..models import BlogTags

class BlogTagsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = '__all__'

class BlogTagsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = '__all__'

class BlogTagsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = '__all__'