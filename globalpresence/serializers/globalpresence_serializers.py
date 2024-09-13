from rest_framework import serializers
from ..models import GlobalPresence

class GlobalPresenceListSerializers(serializers.ModelSerializer):
    class Meta:
        model = GlobalPresence
        fields = '__all__'

class GlobalPresenceRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = GlobalPresence
        fields = '__all__'

class GlobalPresenceWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = GlobalPresence
        fields = '__all__'