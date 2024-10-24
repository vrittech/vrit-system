from rest_framework import serializers
from ..models import Project, ProjectService, ProjectLink, ProjectGroup
import ast

# Utility function to convert string to list
def str_to_list(data, value_to_convert):
    try:
        mutable_data = data.dict()
    except AttributeError:
        mutable_data = data

    value_to_convert_data = mutable_data.get(value_to_convert)
    if isinstance(value_to_convert_data, list):
        return mutable_data

    try:
        variations = ast.literal_eval(value_to_convert_data)
        if isinstance(variations, list):
            mutable_data[value_to_convert] = variations
        else:
            raise ValueError
        return mutable_data
    except (ValueError, SyntaxError) as e:
        raise serializers.ValidationError({f'{value_to_convert}': 'Expected a list, but got invalid input.'}) from e

# Serializer for ProjectService model
class ServicesSerializers_Project(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = ['id', 'name', 'description', 'image']

# Serializer for ProjectLink model
class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = ['id', 'label', 'url']

# List serializer for Project model
class ProjectListSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    project_link = ProjectLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

# Retrieve serializer for Project model
class ProjectRetrieveSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    project_link = ProjectLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectWriteSerializers(serializers.ModelSerializer):
    project_service = serializers.PrimaryKeyRelatedField(
        queryset=ProjectService.objects.all(),
        many=True,
        required=False
    )
    project_link = ProjectLinkSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = '__all__'

    def to_internal_value(self, data):
        # Convert 'project_service' from string to list if necessary
        data = str_to_list(data, 'project_service')
        
        # Convert 'project_link' from string to list if necessary
        data = str_to_list(data, 'project_link')

        # Ensure project_service contains integers
        project_service_data = data.get('project_service', [])
        if isinstance(project_service_data, list):
            try:
                data['project_service'] = [int(service_id) for service_id in project_service_data]
            except ValueError:
                raise serializers.ValidationError({
                    'project_service': 'Expected a list of integers for project_service.'
                })

        return super().to_internal_value(data)

    def create(self, validated_data):
        project_service_data = validated_data.pop('project_service', [])
        project_link_data = validated_data.pop('project_link', [])

        # Create Project instance
        project = Project.objects.create(**validated_data)

        # Add related ProjectService instances
        if project_service_data:
            project.project_service.set(project_service_data)

        # Add related ProjectLink instances
        for link_data in project_link_data:
            link_id = link_data.pop('id', None)
            if link_id:
                ProjectLink.objects.filter(id=link_id).update(**link_data)
                project_link = ProjectLink.objects.get(id=link_id)
            else:
                project_link = ProjectLink.objects.create(**link_data)

            project.project_link.add(project_link)

        return project

    def update(self, instance, validated_data):
        project_service_data = validated_data.pop('project_service', [])
        project_link_data = validated_data.pop('project_link', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if project_service_data:
            instance.project_service.set(project_service_data)

        if project_link_data:
            instance.project_link.clear()
            for link_data in project_link_data:
                link_id = link_data.pop('id', None)
                if link_id:
                    ProjectLink.objects.filter(id=link_id).update(**link_data)
                    project_link = ProjectLink.objects.get(id=link_id)
                else:
                    project_link = ProjectLink.objects.create(**link_data)

                instance.project_link.add(project_link)

        return instance
    
    def validate(self, data):
        # Check if the position already exists in another collection
        position = data.get('position')
        if Project.objects.filter(position=position).exists():
            raise serializers.ValidationError({"A collection with this position already exists."})
        return data
