from rest_framework import serializers
from ..models import CaseStudyTags

class CaseStudyTagsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTags
        fields = '__all__'

class CaseStudyTagsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTags
        fields = '__all__'

class CaseStudyTagsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudyTags
        fields = '__all__'