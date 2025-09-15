from rest_framework import serializers
from ..models import Faqs, FaqsCategory


class FaqsCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = FaqsCategory
        fields = '__all__'

class FaqsCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = FaqsCategory
        fields = '__all__'

class FaqsCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = FaqsCategory
        fields = '__all__'


class FaqsListSerializers(serializers.ModelSerializer):
    faqs_category= FaqsCategoryRetrieveSerializers()
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


    
