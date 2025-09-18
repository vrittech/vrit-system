from rest_framework import serializers
from ..models import TeamMember, TeamMemberCategory
from accounts.models import CustomUser   # adjust import path if needed
from django.contrib.auth.models import Group


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMemberCategory
        fields = ['id', 'name']
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]

class TeamMemberListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    is_superuser= serializers.BooleanField(source="user.is_superuser",read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    professional_image = serializers.CharField(source="user.professional_image", read_only=True)
    
    category= CategorySerializer()
    groups = GroupSerializer(source="user.groups", many=True, read_only=True)

    class Meta:
        model = TeamMember
        fields = ["id", "email", "is_superuser","full_name","professional_image", "joined_at", "category","position","groups"]


class TeamMemberRetrieveSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    is_superuser= serializers.BooleanField(source="user.is_superuser",read_only=True)
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    professional_image = serializers.CharField(source="user.professional_image", read_only=True)
    category= CategorySerializer()
    groups = GroupSerializer(source="user.groups", many=True, read_only=True)


    class Meta:
        model = TeamMember
        fields = ["id", "email", "is_superuser","full_name","professional_image", "joined_at","category","position","groups"]


class TeamMemberWriteSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True, required=False)
    professional_image = serializers.CharField(write_only=True, required=False)
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False, source="user.groups"
    )

    class Meta:
        model = TeamMember
        fields = ["id", "full_name", "professional_image","category","groups"]

    def update(self, instance, validated_data):
        user = instance.user

        # --- Update CustomUser ---
        full_name = validated_data.pop("full_name", None)
        if full_name:
            name_parts = full_name.strip().split()
            if len(name_parts) == 1:
                user.first_name = name_parts[0]
                user.last_name = ""
            else:
                user.first_name = " ".join(name_parts[:-1])
                user.last_name = name_parts[-1]

        professional_image = validated_data.pop("professional_image", None)
        if professional_image is not None:
            user.professional_image = professional_image

        # Handle groups update
        groups_data = validated_data.pop("user", {}).get("groups", None)
        if groups_data is not None:
            user.groups.set(groups_data)

        user.save(update_fields=["first_name", "last_name", "professional_image"])

        # --- Update TeamMember ---
        category = validated_data.get("category")
        if category is not None:
            instance.category = category

        position = validated_data.get("position")
        if position is not None:
            instance.position = position

        instance.save()
        return instance