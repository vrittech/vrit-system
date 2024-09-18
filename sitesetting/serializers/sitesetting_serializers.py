from rest_framework import serializers
from ..models import SiteSetting

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