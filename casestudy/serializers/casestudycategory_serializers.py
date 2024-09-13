from rest_framework import serializers
from ..models import CaseStudyCategory

class CaseStudyCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyCategory
        fields = '__all__'

class CaseStudyCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyCategory
        fields = '__all__'

class CaseStudyCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyCategory
        fields = '__all__'