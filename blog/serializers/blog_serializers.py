from rest_framework import serializers
from ..models import Blog, BlogTags, BlogCategory
from django.utils import timezone

class BlogListSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'excerpt', 'status', 'publish_date', 
            'created_at', 'updated_at', 'category', 'tags'
        ]


class BlogRetrieveSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'description', 'status', 'publish_date', 
            'meta_description', 'meta_keywords', 'meta_author',
            'created_at', 'updated_at', 'category', 'tags', 
            'header_code', 'embedded_code', 'featured_image'
        ]


class BlogWriteSerializers(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=155), write_only=True
    )
    category = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'description', 'site_title', 'excerpt', 
            'status', 'publish_date', 'meta_description', 'meta_keywords', 
            'meta_author', 'tags', 'category', 'header_code', 'embedded_code', 
            'featured_image'
        ]

    def validate_publish_date(self, value):
        """
        Ensure that publish_date is in the future for scheduled blogs.
        """
        if self.initial_data.get('status') == 'scheduled' and value <= timezone.now().date():
            raise serializers.ValidationError("Publish date must be in the future for scheduled blogs.")
        return value

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', [])
        
        blog = Blog.objects.create(**validated_data)
        blog.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))
        blog.category.set(category_data)

        return blog

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags_data:
            instance.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))
        
        if category_data:
            instance.category.set(category_data)

        instance.save()
        return instance
