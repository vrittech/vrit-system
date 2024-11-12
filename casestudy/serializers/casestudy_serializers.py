# from rest_framework import serializers
# from ..models import CaseStudy

# class CaseStudyListSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = CaseStudy
#         fields = '__all__'

# class CaseStudyRetrieveSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = CaseStudy
#         fields = '__all__'

# class CaseStudyWriteSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = CaseStudy
#         fields = '__all__'

from rest_framework import serializers
from ..models import CaseStudy, CaseStudyTags, CaseStudyCategory
from django.utils import timezone
from accounts.models import CustomUser

class CaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name','professional_image']

class CaseStudyTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTags
        fields = ['id', 'name']
        
class CaseStudyListSerializers(serializers.ModelSerializer):
    user = CaseUserSerializer(read_only=True)
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = CaseStudy
        fields = '__all__'


class CaseStudyRetrieveSerializers(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    tags = serializers.StringRelatedField(many=True)
    user = CaseUserSerializer(read_only=True)

    class Meta:
        model = CaseStudy
        fields = '__all__'


class CaseStudyWriteSerializers(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(max_length=155), write_only=True
    )
    category = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model = CaseStudy
        fields = '__all__'

    def validate_publish_date(self, value):
        """
        Ensure that publish_date is in the future for scheduled blogs.
        """
        if self.initial_data.get('status') == 'scheduled' and value <= timezone.now().date():
            raise serializers.ValidationError("Publish date must be in the future for scheduled blogs.")
        return value
    def validate(self, data):
        # Check if the position already exists in another Career
        position = data.get('position')
        if position and CaseStudy.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A case-study with this position already exists."})
        return data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', [])
        
        user = self.context['request'].user
        full_name = user.full_name or user.username  
        validated_data['created_by'] = full_name
        validated_data['user'] = user
        
        blog = CaseStudy.objects.create(**validated_data)
        blog.tags.set(CaseStudy.tag_manager.get_or_create_tags(tags_data))
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
            instance.tags.set(CaseStudy.tag_manager.get_or_create_tags(tags_data))

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
