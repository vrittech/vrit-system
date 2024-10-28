from rest_framework import serializers
from ..models import Forms

class FormsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = '__all__'

class FormsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = '__all__'

class FormsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Forms
        fields = '__all__'