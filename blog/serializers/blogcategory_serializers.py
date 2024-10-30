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
        
    def update(self, instance, validated_data):
        # Remove 'media' from validated_data if not provided
        media = validated_data.pop('media', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Only update media if provided
        if media:
            instance.media = media
        
        instance.save()
        return instance