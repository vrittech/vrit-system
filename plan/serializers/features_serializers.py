from rest_framework import serializers
from ..models import Features

class FeaturesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'

class FeaturesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'

class FeaturesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = '__all__'