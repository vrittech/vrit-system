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
        
    def update(self, instance, validated_data):
        # Handle the media field separately
        media = validated_data.pop('media', None)

        if media is not None:
            if media == "null":
                # If media is set to 'null', delete the current media
                instance.media.delete(save=False)
                instance.media = None
            else:
                # If media data is sent, update it
                instance.media = media

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance