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
        fields = ['id','name','color']

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
        career_categories = validated_data.pop("career_category", None)

        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        # Handle ManyToMany field properly
        if career_categories is not None:
            instance.career_category.set(career_categories)  # ✅ Use set()
        return instance
