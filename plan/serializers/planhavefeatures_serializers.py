from rest_framework import serializers
from ..models import PlanHaveFeatures

class PlanHaveFeaturesListSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlanHaveFeatures
        fields = '__all__'

class PlanHaveFeaturesRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlanHaveFeatures
        fields = '__all__'

class PlanHaveFeaturesWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlanHaveFeatures
        fields = '__all__'