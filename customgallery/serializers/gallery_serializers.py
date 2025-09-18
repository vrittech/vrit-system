from rest_framework import serializers
from ..models import CustomGallery as Gallery, CustomGalleryCategory, Position



class CustomGalleryCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomGalleryCategory
        fields = '__all__'

class CustomGalleryCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomGalleryCategory
        fields = '__all__'

class CustomGalleryCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomGalleryCategory
        fields = '__all__'

    def validate_name(self, value):
        """
        Ensure that category_name is unique (case-insensitive).
        If updating, exclude the current instance.
        """
        qs = CustomGalleryCategory.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This category already exists.")
        return value




class PositionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'
    def validate(self, attrs):
        type_ = attrs.get("type")
        position = attrs.get("position")

        # exclude self when updating
        qs = Position.objects.filter(
            type=type_,
            position__iexact=position.strip() if position else position
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            # get the human-readable label for the choice
            type_display = dict(Position._meta.get_field("type").choices).get(type_, type_)
            raise serializers.ValidationError(
                {"position": f"For {type_display}, this position already exists."}
            )

        return attrs


class GalleryListSerializers(serializers.ModelSerializer):
    position= PositionListSerializers()
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryRetrieveSerializers(serializers.ModelSerializer):
    position= PositionListSerializers()
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

    def update(self, instance, validated_data):
        # For all optional fields, if they are missing, set to None
        optional_fields = ['category']  # list all optional fields here
        for field in optional_fields:
            if field not in validated_data:
                if isinstance(self.fields[field], serializers.ManyRelatedField):
                    getattr(instance, field).clear()  # clear M2M
                else:
                    setattr(instance, field, None)

        # Now update other fields normally
        return super().update(instance, validated_data)