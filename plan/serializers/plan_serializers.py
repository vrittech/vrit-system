from rest_framework import serializers
from ..models import Plan

class PlanListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PlanRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class PlanWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'