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
import ast
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone


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
            if all(isinstance(item, CaseStudyTags) for item in value_to_convert_data):
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


class CaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyCategory
        fields = '__all__'
        
class CaseTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTags
        fields = ['id', 'name']
        
class CaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name','professional_image','position','avatar']
        
class CaseStudyListSerializers(serializers.ModelSerializer):
    category = CaseCategorySerializer(many=True, read_only=True)
    tags = CaseTagsSerializer(many=True, read_only=True)
    user = CaseUserSerializer(read_only=True)
    class Meta:
        model = CaseStudy
        fields = '__all__'


class CaseStudyRetrieveSerializers(serializers.ModelSerializer):
    category = CaseCategorySerializer(many=True, read_only=True)
    tags = CaseTagsSerializer(many=True, read_only=True)
    user = CaseUserSerializer(read_only=True)

    class Meta:
        model = CaseStudy
        fields = '__all__'

class CaseStudyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'
        read_only_fields = ['user', 'author']

    def to_internal_value(self, data):
        # If tags and category are already lists, no need to call str_to_list
        if not isinstance(data.get('tags'), list):
            data = str_to_list(data, 'tags')
        if not isinstance(data.get('category'), list):
            data = str_to_list(data, 'category')
        return super().to_internal_value(data)

    def validate_publish_date(self, value):
        """
        Ensure that publish_date is in the future for scheduled case_studys.
        """
        if self.initial_data.get('status') == 'scheduled' and value <= timezone.now().date():
            raise serializers.ValidationError("Publish date must be in the future for scheduled case_studys.")
        return value
    
    def validate(self, data):
        # Ensure unique `position` for the case_study
        position = data.get('position')
        if position and CaseStudy.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A case_study with this position already exists."})
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

        # Create the case_study instance
        case_study = CaseStudy.objects.create(**validated_data)
        
        # Assign the featured image if it exists
        if featured_image:
            case_study.featured_image = featured_image
            case_study.save()

        # Set tags and categories if provided
        if tags_data:
            case_study.tags.set(CaseStudy.tag_manager.get_or_create_tags(tags_data))
        if category_data:
            case_study.category.set(category_data)

        return case_study

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
            instance.tags.set(CaseStudy.tag_manager.get_or_create_tags(tags_data))

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
