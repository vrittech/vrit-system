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