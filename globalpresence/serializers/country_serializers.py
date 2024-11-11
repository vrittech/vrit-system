from rest_framework import serializers
from ..models import Country

class CountryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CountryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CountryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'