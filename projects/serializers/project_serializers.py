from rest_framework import serializers
from ..models import Project,ProjectService
import ast

def str_to_list(data,value_to_convert):
    try:
        mutable_data = data.dict()
    except Exception:
        mutable_data = data
    value_to_convert_data = mutable_data[value_to_convert]
    if isinstance(value_to_convert_data,list):# type(value_to_convert_data) == list:

        return mutable_data
    try:
        variations = ast.literal_eval(value_to_convert_data)
        mutable_data[value_to_convert] = variations
        return mutable_data
    except ValueError as e:
        raise serializers.ValidationError({f'{value_to_convert}': str(e)}) from e

class ServicesSerializers_Project(serializers.ModelSerializer):
    class Meta:
        model = ProjectService
        fields = ['name']

class ProjectListSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectRetrieveSerializers(serializers.ModelSerializer):
    project_service = ServicesSerializers_Project(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'

class ProjectWriteSerializers(serializers.ModelSerializer):

    def to_internal_value(self, data):
        if data.get('packages'):
            data = str_to_list(data,'packages')
        return super().to_internal_value(data)

    
    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        instance = super().create(validated_data)
        
    

