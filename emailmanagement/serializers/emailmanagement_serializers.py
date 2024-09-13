from rest_framework import serializers
from ..models import EmailManagement

class EmailManagementListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailManagement
        fields = '__all__'

class EmailManagementRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailManagement
        fields = '__all__'

class EmailManagementWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailManagement
        fields = '__all__'