from rest_framework import serializers
from ..models import ClientSettings

class ClientSettingsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientSettings
        fields = '__all__'

class ClientSettingsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientSettings
        fields = '__all__'

class ClientSettingsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClientSettings
        fields = '__all__'

class ClientSettingsArraySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientSettings
        fields = '__all__'


class BulkClientSettingsSerializer(serializers.Serializer):
    settings = ClientSettingsArraySerializer(many=True)

    def create(self, validated_data):
        settings_data = validated_data['settings']
        client_settings_objects = [
            ClientSettings(
                section=setting['section'],
                loop_type=setting['loop_type'],
                delay_time=setting['delay_time']
            )
            for setting in settings_data
        ]
        return ClientSettings.objects.bulk_create(client_settings_objects)
    
#     {
#   "settings": [
#     {"section": "first", "loop_type": "reverse", "delay_time": "00:01:00"},
#     {"section": "second", "loop_type": "forward", "delay_time": "00:00:30"}
#   ]
# }
