from rest_framework import serializers
from ..models import Clients

class ClientsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class ClientsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

class ClientsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'