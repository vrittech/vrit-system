from rest_framework import serializers
from ..models import Forms, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name','color', 'created_at', 'updated_at']


class FormsListSerializers(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Forms
        fields = '__all__'

class FormsRetrieveSerializers(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Forms
        fields ='__all__'


class FormsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields ='__all__'

    def validate(self, data):
        # Ensure that if 'auto_expiration' is True, 'auto_expiration_date' is provided
        if data.get('auto_expiration') and not data.get('auto_expiration_date'):
            raise serializers.ValidationError(
                "Auto expiration date is required when auto expiration is enabled."
            )
        return data

    def update(self, instance, validated_data):
        # Handle the media field separately
        media = validated_data.pop('media', None)

        if media is not None:
            if media == "null":
                # If media is set to 'null', delete the current media
                instance.media.delete(save=False)
                instance.media = None
            else:
                # If media data is sent, update it
                instance.media = media

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
