from rest_framework import serializers
from ..models import ContactUs

class ContactUsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class ContactUsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'

class ContactUsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'