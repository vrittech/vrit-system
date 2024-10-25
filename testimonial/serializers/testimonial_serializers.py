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
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data