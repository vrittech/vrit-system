from rest_framework import serializers
from ..models import *

class SiteSettingListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'

class SiteSettingRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'

class SiteSettingWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = '__all__'

class PrivacyPolicyRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'
class TermAndConditionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = '__all__'