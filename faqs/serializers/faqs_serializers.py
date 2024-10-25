from rest_framework import serializers
from ..models import Faqs

class FaqsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'

class FaqsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'

class FaqsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'
    
    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if Faqs.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data