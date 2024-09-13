from rest_framework import serializers
from ..models import Inquires

class InquiresListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquires
        fields = '__all__'

class InquiresRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquires
        fields = '__all__'

class InquiresWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Inquires
        fields = '__all__'