from rest_framework import serializers
from ..models import Forms, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_at', 'updated_at']


class FormsListSerializers(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Forms
        fields = '__all__'

class FormsRetrieveSerializers(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Forms
        fields = [
            'id',
            'title',
            'category',
            'description',
            'header_code',
            'embedded_code',
            'image',
            'excerpt',
            'auto_expiration',
            'is_expired',
            'auto_expiration_date',
            'position',
            'created_at',
            'updated_at',
        ]


class FormsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = [
            'title',
            'category',
            'description',
            'header_code',
            'embedded_code',
            'image',
            'excerpt',
            'auto_expiration',
            'auto_expiration_date',
            'position',
        ]

    def validate(self, data):
        # Ensure that if 'auto_expiration' is True, 'auto_expiration_date' is provided
        if data.get('auto_expiration') and not data.get('auto_expiration_date'):
            raise serializers.ValidationError(
                "Auto expiration date is required when auto expiration is enabled."
            )
        return data
