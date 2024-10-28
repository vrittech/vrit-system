from rest_framework import serializers
from blog.models import BlogCategory
from ..models import NewsLetterSubscription

# Serializer for BlogCategory
class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name']


# Serializer for NewsLetterSubscription List
class NewsLetterSubscriptionListSerializers(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=True, read_only=True)

    class Meta:
        model = NewsLetterSubscription
        fields = [
            'id', 'name', 'email', 'is_subscribed', 'category', 
            'date', 'created_at', 'updated_at'
        ]


# Serializer for NewsLetterSubscription Retrieve
class NewsLetterSubscriptionRetrieveSerializers(serializers.ModelSerializer):
    category = BlogCategorySerializer(many=True, read_only=True)

    class Meta:
        model = NewsLetterSubscription
        fields = [
            'id', 'name', 'email', 'is_subscribed', 'category', 
            'date', 'created_at', 'updated_at'
        ]


# Serializer for NewsLetterSubscription Create/Update
class NewsLetterSubscriptionWriteSerializers(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=BlogCategory.objects.all(), many=True, required=False
    )

    class Meta:
        model = NewsLetterSubscription
        fields = [
            'id', 'name', 'email', 'is_subscribed', 'category', 'date'
        ]

    def validate_email(self, value):
        # Ensure the email is unique when creating a new subscription
        if self.instance is None and NewsLetterSubscription.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        newsletter_subscription = NewsLetterSubscription.objects.create(**validated_data)
        newsletter_subscription.category.set(categories)
        return newsletter_subscription

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the categories if provided
        if categories is not None:
            instance.category.set(categories)

        return instance
