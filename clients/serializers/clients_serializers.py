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
        # Check if the position already exists in another client
        position = data.get('position')
        if position and Clients.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A client with this position already exists."})
        return data
    def validate_slug(self, value):
        if value:  # Only check if provided
            # Case-insensitive match (if needed)
            qs = Clients.objects.filter(slug=value)
            if self.instance:  # When updating, exclude the current record
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("The given slug already exists.")
        return value
    
    def create(self, validated_data):
        print("this is line 27")
        instance =  super().create(validated_data)
        print(instance.id)
        return instance

    def update(self, instance, validated_data):
        media = validated_data.pop('media', None)

        # Update instance fields if data is provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Handle the media field specifically
        if media is not None:
            if media == "null":
                # If media is set to 'null', delete the current image
                instance.media.delete(save=False)
                instance.media = None
            else:
                # If media data is sent, update it
                instance.media = media

        instance.save()
        return instance
        
    