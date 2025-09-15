from rest_framework import serializers
from ..models import TeamMemberCategory

class TeamMemberCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = '__all__'

class TeamMemberCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = '__all__'

class TeamMemberCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = '__all__'