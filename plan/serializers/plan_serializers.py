from rest_framework import serializers
from ..models import Plan, Features, PlanHaveFeatures

# Serializer for Features
class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Features
        fields = ['id', 'title', 'is_feature_checked']

# Serializer for PlanHaveFeatures
class PlanHaveFeaturesSerializer(serializers.ModelSerializer):
    feature = FeaturesSerializer(read_only=True)

    class Meta:
        model = PlanHaveFeatures
        fields = ['id', 'feature', 'status']

# Serializer for Plan (List)
class PlanListSerializers(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'pricing', 'duration', 'description',
            'features', 'is_show', 'position', 'created_at', 'updated_at'
        ]

    def get_features(self, obj):
        features = PlanHaveFeatures.objects.filter(plan=obj, status=True)
        return PlanHaveFeaturesSerializer(features, many=True).data

# Serializer for Plan (Retrieve)
class PlanRetrieveSerializers(serializers.ModelSerializer):
    features = PlanHaveFeaturesSerializer(source='planhavefeatures_set', many=True, read_only=True)

    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'pricing', 'duration', 'description',
            'features', 'is_show', 'position', 'created_at', 'updated_at'
        ]

# Serializer for Plan (Create & Update)
class PlanWriteSerializers(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(queryset=Features.objects.all(), many=True)

    class Meta:
        model = Plan
        fields = [
            'id', 'title', 'pricing', 'duration', 'description',
            'features', 'is_show', 'position'
        ]

    def validate_is_show(self, value):
        # Validate that at least 3 plans remain visible
        if not value:
            visible_plans_count = Plan.objects.filter(is_show=True).count()
            if visible_plans_count <= 3:
                raise serializers.ValidationError("At least 3 plans must be visible at all times.")
        return value

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        plan = Plan.objects.create(**validated_data)

        # Add features to the Plan through PlanHaveFeatures
        for feature in features_data:
            PlanHaveFeatures.objects.create(plan=plan, feature=feature)

        return plan

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', [])

        # Validate the `is_show` field when updating
        if 'is_show' in validated_data:
            new_is_show = validated_data['is_show']
            if not new_is_show and Plan.objects.filter(is_show=True).count() <= 3:
                raise serializers.ValidationError(
                    "At least 3 plans must be visible at all times."
                )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update PlanHaveFeatures for this Plan
        instance.features.clear()
        for feature in features_data:
            PlanHaveFeatures.objects.create(plan=instance, feature=feature)

        return instance