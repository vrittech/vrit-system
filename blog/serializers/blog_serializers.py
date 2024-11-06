from rest_framework import serializers
from ..models import Blog, BlogTags, BlogCategory
from django.utils import timezone


class BlogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = ['id', 'name']
        
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
        tags_data = validated_data.pop('tags', None)
        category_data = validated_data.pop('category', None)
        featured_image = validated_data.pop('featured_image', None)

        # Update instance fields if data is provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle tags if provided
        if tags_data is not None:
            instance.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))

        # Handle categories if provided
        if category_data is not None:
            instance.category.set(category_data)

        # Handle featured_image specifically
        if featured_image is not None:
            if featured_image == "null":
                # If image is set to 'null', delete the current image
                instance.featured_image.delete(save=False)
                instance.featured_image = None
            else:
                # If image data is sent, update it
                instance.featured_image = featured_image

        instance.save()
        return instance

