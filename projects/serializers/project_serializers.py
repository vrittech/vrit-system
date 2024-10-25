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

class ProjectGroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProjectGroup
        # fields = ['id', 'name', 'description', 'image']
        fields = ['id', 'name','created_at']

# Serializer for ProjectLink model
class ProjectLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectLink
        fields = ['id', 'label', 'url']

# List serializer for Project model
class ProjectListSerializers(serializers.ModelSerializer):
    group = ProjectGroupSerializers(read_only=True)
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    project_link = ProjectLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

# Retrieve serializer for Project model
class ProjectRetrieveSerializers(serializers.ModelSerializer):
    group = ProjectGroupSerializers(read_only=True)
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
        if 'project_service' in data:
            data = str_to_list(data, 'project_service')
        
        # Convert 'project_link' from string to list if necessary
        if 'project_link' in data:
            data = str_to_list(data, 'project_link')

        # Ensure project_service contains integers if present
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
        # Update only the fields that are present in validated_data
        project_service_data = validated_data.pop('project_service', None)
        project_link_data = validated_data.pop('project_link', None)
        media_data = validated_data.pop('media', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update project_service only if provided in the request data
        if project_service_data is not None:
            instance.project_service.set(project_service_data)

        # Update project_link only if provided in the request data
        if project_link_data is not None:
            instance.project_link.clear()
            for link_data in project_link_data:
                link_id = link_data.pop('id', None)
                if link_id:
                    ProjectLink.objects.filter(id=link_id).update(**link_data)
                    project_link = ProjectLink.objects.get(id=link_id)
                else:
                    project_link = ProjectLink.objects.create(**link_data)
                instance.project_link.add(project_link)

        # Update media data if provided
        if media_data is not None:
            instance.media.set(media_data)

        return instance

    def validate(self, data):
        # Validate 'position' only if it is provided in the request data
        position = data.get('position', None)
        if position is not None and Project.objects.filter(position=position).exists():
            raise serializers.ValidationError({"position": "A project with this position already exists."})

        # Ensure that the validate() method returns the validated data
        return data
