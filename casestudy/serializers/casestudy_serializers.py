from rest_framework import serializers
from ..models import CaseStudy

class CaseStudyListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'

class CaseStudyRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'

class CaseStudyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'