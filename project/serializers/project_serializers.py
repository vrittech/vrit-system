from rest_framework import serializers

from project.models import CaseStudy, Project, ProjectCategory


class ProjectCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ProjectCategoryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

class ProjectCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectCategory
        fields = '__all__'

    def validate_name(self, value):
        """
        Ensure that category_name is unique (case-insensitive).
        If updating, exclude the current instance.
        """
        qs = ProjectCategory.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError("This category already exists.")
        return value
    


class ProjectListSerializers(serializers.ModelSerializer):
    category= ProjectCategoryRetrieveSerializers(many=True)
    casestudy_id = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    def get_casestudy_id(self, obj):
        if hasattr(obj, "casestudy"):
            return obj.casestudy.id
        return None

class ProjectRetrieveSerializers(serializers.ModelSerializer):
    category= ProjectCategoryRetrieveSerializers(many=True)
    casestudy_id = serializers.SerializerMethodField()
    class Meta:
        model = Project
        fields = '__all__'
    def get_casestudy_id(self, obj):
        if hasattr(obj, "casestudy"):
            return obj.casestudy.id
        return None

class ProjectWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def update(self, instance, validated_data):
        # For all optional fields, if they are missing, set to None
        optional_fields = ['category']  # list all optional fields here
        for field in optional_fields:
            if field not in validated_data:
                if isinstance(self.fields[field], serializers.ManyRelatedField):
                    getattr(instance, field).clear()  # clear M2M
                else:
                    setattr(instance, field, None)

        # Now update other fields normally
        return super().update(instance, validated_data)


    

class CaseStudyListSerializers(serializers.ModelSerializer):
    project = ProjectListSerializers() 
    class Meta:
        model = CaseStudy
        fields = '__all__'

class CaseStudyRetrieveSerializers(serializers.ModelSerializer):
    project = ProjectListSerializers() 
    class Meta:
        model = CaseStudy
        fields = '__all__'

class CaseStudyWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = '__all__'

   