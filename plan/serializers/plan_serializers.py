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
            'features', 'is_show', 'created_at', 'updated_at'
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
            'features', 'is_show', 'created_at', 'updated_at'
        ]

# Serializer for Plan (Create & Update)

class PlanWriteSerializers(serializers.ModelSerializer):
    features = serializers.PrimaryKeyRelatedField(queryset=Features.objects.all(), many=True)

    class Meta:
        model = Plan
        fields = '__all__'

    def validate(self, data):
        is_show = data.get('is_show', False)  
        is_popular = data.get('is_popular', False)

        # Count the number of visible plans
        visible_plans_count = Plan.objects.filter(is_show=True).count()

        # If creating a new plan, increment the count
        if not self.instance and is_show:
            visible_plans_count += 1

        # Validation: At least 1 plan must be visible
        if not is_show and visible_plans_count <= 1:
            raise serializers.ValidationError("At least 1 plan must be visible at all times.")

        # Validation: No more than 3 plans can be visible
        if is_show and visible_plans_count > 3:
            raise serializers.ValidationError("No more than 3 plans can be visible at the same time.")

        # Validation: Only a visible plan can be popular
        if is_popular and not is_show:
            raise serializers.ValidationError("Only a visible plan can be marked as popular.")

        # Validation: If only one visible plan, it must be marked as popular
        if visible_plans_count == 1 and is_show and not is_popular:
            raise serializers.ValidationError("The only visible plan must be marked as popular.")

        return data

    def create(self, validated_data):
        features_data = validated_data.pop('features', [])
        plan = Plan.objects.create(**validated_data)

        # Add features to the Plan through PlanHaveFeatures
        for feature in features_data:
            PlanHaveFeatures.objects.create(plan=plan, feature=feature)

        return plan

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update PlanHaveFeatures for this Plan
        instance.features.clear()
        for feature in features_data:
            PlanHaveFeatures.objects.create(plan=instance, feature=feature)

        return instance
