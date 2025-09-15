from rest_framework import serializers
from termsconditionsprivacypolicy.models import PrivacyPolicy

class PrivacyListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['description']


class PrivacyRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['description']


class PrivacyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = ['description']

