from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from ..models import Career, CareerCategory, ExperienceLevel

class ExperienceLevelSerializers_Career(serializers.ModelSerializer):
    class Meta:
        model = ExperienceLevel
        fields = ['id','level_name']
class CareerCategorySerializers_Career(serializers.ModelSerializer):
    class Meta:
        model = CareerCategory
        fields = ['id','name']

class CareerListSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()
    career_category= CareerCategorySerializers_Career(many=True)
    duration_status = serializers.SerializerMethodField() 

    class Meta:
        model = Career
        fields = '__all__'

    def get_duration_status(self, obj):
        if not obj.expiration_date:
            return "not_expired"
        now = timezone.now()
        soon = now + timedelta(days=7)

        if obj.expiration_date <= now:
            return "expired"
        elif now < obj.expiration_date <= soon:
            return "expiring_soon"
        return "not_expired"

class CareerRetrieveSerializers(serializers.ModelSerializer):
    experience_level = ExperienceLevelSerializers_Career()
    career_category= CareerCategorySerializers_Career(many=True)
    duration_status = serializers.SerializerMethodField() 

    class Meta:
        model = Career
        fields = '__all__'

    def get_duration_status(self, obj):
        if not obj.expiration_date:
            return "not_expired"
        now = timezone.now()
        soon = now + timedelta(days=7)

        if obj.expiration_date <= now:
            return "expired"
        elif now < obj.expiration_date <= soon:
            return "expiring_soon"
        return "not_expired"

class CareerWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Career
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
