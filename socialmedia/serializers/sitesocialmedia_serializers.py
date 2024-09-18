from rest_framework import serializers
from ..models import SiteSocialMedia

class SiteSocialMediaListSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSocialMedia
        fields = '__all__'

class SiteSocialMediaRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSocialMedia
        fields = '__all__'

class SiteSocialMediaWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SiteSocialMedia
        fields = '__all__'