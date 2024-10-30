from rest_framework import serializers
from ..models import Career, ExperienceLevel

class ExperienceLevelSerializers_Career(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = ['level_name']

class CareerListSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()

    class Meta:
        model = Career
        fields = '__all__'

class CareerRetrieveSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()

    class Meta:
        model = Career
        fields = '__all__'

class CareerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = '__all__'
    
    def validate(self, data):
        # Check if the position already exists in another Career
        position = data.get('position')
        if position and Career.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A career with this position already exists."})
        return data

    def update(self, instance, validated_data):
        # Handle the image field separately
        image = validated_data.pop('image', None)

        if image is not None:
            if image == "null":
                # If image is set to 'null', delete the current image
                instance.image.delete(save=False)
                instance.image = None
            else:
                # If image data is sent, update it
                instance.image = image

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
