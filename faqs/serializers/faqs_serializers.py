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

    def validate_name(self, value):
        """
        Ensure that category_name is unique (case-insensitive).
        If updating, exclude the current instance.
        """
        qs = FaqsCategory.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This category already exists.")
        return value
    


class FaqsListSerializers(serializers.ModelSerializer):
    faqs_category= FaqsCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Faqs
        fields = '__all__'

class FaqsRetrieveSerializers(serializers.ModelSerializer):
    faqs_category= FaqsCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Faqs
        fields = '__all__'

class FaqsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Faqs
        fields = '__all__'


    
