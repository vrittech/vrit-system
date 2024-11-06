from rest_framework import serializers
from ..models import EmailLog

class EmailLogListSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'

class EmailLogRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'

class EmailLogWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = EmailLog
        fields = '__all__'