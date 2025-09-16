from rest_framework import serializers
from ..models import Services, ServicesCategory

class ServicesCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicesCategory
        fields = '__all__'

class ServicesCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicesCategory
        fields = '__all__'

class ServicesCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServicesCategory
        fields = '__all__'

    def validate_name(self, value):
        """
        Ensure that category_name is unique (case-insensitive).
        If updating, exclude the current instance.
        """
        qs = ServicesCategory.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This category already exists.")
        return value



class ServicesListSerializers(serializers.ModelSerializer):
    category= ServicesCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Services
        fields = '__all__'

class ServicesRetrieveSerializers(serializers.ModelSerializer):
    category= ServicesCategoryRetrieveSerializers(many=True)
    class Meta:
        model = Services
        fields = '__all__'

class ServicesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'
        
    
   