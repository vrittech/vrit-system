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
        image = validated_data.pop('image', None)

        # Update instance fields if data is provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle the image field specifically
        if image is not None:
            if image == "null":
                # If image is set to 'null', delete the current image
                instance.image.delete(save=False)
                instance.image = None
            else:
                # If image data is sent, update it
                instance.image = image

        instance.save()
        return instance