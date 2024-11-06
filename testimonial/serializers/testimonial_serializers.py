from rest_framework import serializers
from ..models import Testimonial

class TestimonialListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class TestimonialRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class TestimonialWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'
        
    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if Testimonial.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A Testimonial with this position already exists."})
        return data
    
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