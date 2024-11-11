from rest_framework import serializers
from ..models import Blog, BlogTags, BlogCategory
from django.utils import timezone
from accounts.models import CustomUser


class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name','professional_image']  

class BlogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = ['id', 'name']
        
class BlogListSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    user = BlogUserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogRetrieveSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    user = BlogUserSerializer(read_only=True)


    class Meta:
        model = Blog
        fields = '__all__'



class BlogWriteSerializers(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=155), write_only=True
    )
    category = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = Blog
        fields = '__all__'

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
        
        user = self.context['request'].user
        full_name = user.full_name or user.username  

        validated_data['created_by'] = full_name
        validated_data['user'] = user
        
        blog = Blog.objects.create(**validated_data)
        blog.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))
        blog.category.set(category_data)

        return blog

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        category_data = validated_data.pop('category', None)
        featured_image = validated_data.pop('featured_image', None)
        
        user = self.context['request'].user
        full_name = user.full_name or user.username  
        validated_data['created_by'] = full_name
        validated_data['user'] = user

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

