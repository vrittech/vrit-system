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
        
    
    def update(self, instance, validated_data):
        # Handle the media field separately
        profile_image = validated_data.pop('profile_image', None)

        if profile_image is not None:
            if profile_image == "null":
                # If media is set to 'null', delete the current media
                instance.profile_image.delete(save=False)
                instance.profile_image = None
            else:
                # If media data is sent, update it
                instance.profile_image = profile_image

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance