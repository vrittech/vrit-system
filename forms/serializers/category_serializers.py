from rest_framework import serializers
from ..models import Category

class CategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        """
        Ensure that category_name is unique (case-insensitive).
        If updating, exclude the current instance.
        """
        qs = Category.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This category already exists.")
        return value