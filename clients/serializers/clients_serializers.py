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

    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if Clients.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data
        
    