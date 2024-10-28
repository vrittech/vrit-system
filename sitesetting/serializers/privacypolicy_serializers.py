from rest_framework import serializers
from ..models import PrivacyPolicy

class PrivacyPolicyListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class PrivacyPolicyRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

class PrivacyPolicyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'