from rest_framework import serializers
from ..models import Blog, BlogTags, BlogCategory
from django.utils import timezone
from accounts.models import CustomUser
import ast
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from django.utils import timezone
from datetime import datetime



def str_to_list(data, value_to_convert):
    """
    Converts a string representation of a list into an actual list if necessary.
    """
    try:
        mutable_data = data.dict() if hasattr(data, 'dict') else data
        value_to_convert_data = mutable_data.get(value_to_convert, None)
        
        # Skip conversion if data is already a list or contains objects
        if isinstance(value_to_convert_data, list):
            # Check if it's a list of BlogTags objects; if so, skip conversion
            if all(isinstance(item, BlogTags) for item in value_to_convert_data):
                return mutable_data
            # If it's a list of IDs or similar, also skip conversion
            return mutable_data

        # Only parse if value is a string
        if isinstance(value_to_convert_data, str):
            try:
                variations = ast.literal_eval(value_to_convert_data)
                if isinstance(variations, list):
                    mutable_data[value_to_convert] = variations
            except (ValueError, SyntaxError) as e:
                raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e
        return mutable_data
    except KeyError:
        # Return unchanged data if value_to_convert is not in the data
        return data

    

class BlogUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name','professional_image','position','avatar']  


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'
        ref_name = 'blog'
        
class BlogTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTags
        fields = ['id', 'name']
        
class BlogListSerializers(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=True, read_only=True)
    tags = BlogTagsSerializer(many=True, read_only=True)
    user = BlogUserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'


class BlogRetrieveSerializers(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=True, read_only=True)
    tags = BlogTagsSerializer(many=True, read_only=True)
    user = BlogUserSerializer(read_only=True)


    class Meta:
        model = Blog
        fields = '__all__'




class BlogWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['user', 'author']

    def to_internal_value(self, data):
        # If tags and category are already lists, no need to call str_to_list
        if not isinstance(data.get('tags'), list):
            data = str_to_list(data, 'tags')
        if not isinstance(data.get('category'), list):
            data = str_to_list(data, 'category')
        return super().to_internal_value(data)


    def validate(self, data):
        # Ensure unique `position` for the blog
        position = data.get('position')
        if position and Blog.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A blog with this position already exists."})
        return data

    @transaction.atomic
    def create(self, validated_data):
        # Extract `tags` and `category` data from `validated_data`
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', [])
        
        # Get the user context
        user = self.context['request'].user
        full_name = user.full_name or user.username  

        validated_data['author'] = full_name
        validated_data['user'] = user

        # Extract single featured image from request if provided
        featured_image = self.context['request'].FILES.get('featured_image')

        # Create the blog instance
        blog = Blog.objects.create(**validated_data)
        
        # Assign the featured image if it exists
        if featured_image:
            blog.featured_image = featured_image
            blog.save()

        # Set tags and categories if provided
        if tags_data:
            blog.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))
        if category_data:
            blog.category.set(category_data)

        return blog

    @transaction.atomic
    def update(self, instance, validated_data):
        # Extract `tags`, `category`, and `featured_image` from `validated_data`
        tags_data = validated_data.pop('tags', None)
        category_data = validated_data.pop('category', None)
        featured_image = self.context['request'].FILES.get('featured_image')

        # Get the user context
        user = self.context['request'].user
        full_name = user.full_name or user.username  
        validated_data['author'] = full_name
        validated_data['user'] = user

        # Update instance fields if data is provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update tags if provided
        if tags_data is not None:
            instance.tags.set(Blog.tag_manager.get_or_create_tags(tags_data))

        # Update categories if provided
        if category_data is not None:
            instance.category.set(category_data)

        # Handle featured_image specifically
        if featured_image:
            instance.featured_image = featured_image
        elif 'featured_image' in self.context['request'].data and self.context['request'].data['featured_image'] == "null":
            # If featured_image is set to "null" in the data, delete the current image
            instance.featured_image.delete(save=False)
            instance.featured_image = None

        instance.save()
        return instance