from rest_framework import serializers
from ..models import ExprienceLevel

class ExprienceLevelListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExprienceLevel
        fields = '__all__'

class ExprienceLevelRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExprienceLevel
        fields = '__all__'

class ExprienceLevelWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ExprienceLevel
        fields = '__all__'