from rest_framework import serializers
from ..models import NewsLetterSubscription

class NewsLetterSubscriptionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscription
        fields = '__all__'

class NewsLetterSubscriptionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscription
        fields = '__all__'

class NewsLetterSubscriptionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewsLetterSubscription
        fields = '__all__'