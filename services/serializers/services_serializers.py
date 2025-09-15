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
        
    
   