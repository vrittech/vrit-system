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