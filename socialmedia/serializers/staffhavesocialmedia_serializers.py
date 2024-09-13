from rest_framework import serializers
from ..models import StaffHaveSocialMedia

class StaffHaveSocialMediaListSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffHaveSocialMedia
        fields = '__all__'

class StaffHaveSocialMediaRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffHaveSocialMedia
        fields = '__all__'

class StaffHaveSocialMediaWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = StaffHaveSocialMedia
        fields = '__all__'