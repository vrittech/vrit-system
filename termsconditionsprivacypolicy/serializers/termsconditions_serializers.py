from rest_framework import serializers
from termsconditionsprivacypolicy.models import TermsConditions

class TermsConditionsListSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsConditions
        fields = ['description']


class TermsConditionsRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsConditions
        fields = ['description']


class TermsConditionsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = TermsConditions
        fields = ['description']

