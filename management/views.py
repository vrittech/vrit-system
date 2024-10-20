from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.apps import apps
from rest_framework import status

class MultipleDelete(APIView):
    def post(self, request, model_name):
        # Get the delete_ids from the request data
        delete_ids = request.data.get('delete_ids', [])

        # Ensure delete_ids is a list
        if not isinstance(delete_ids, list):
            return Response({'error': 'delete_ids should be a list of IDs.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the model class dynamically from the string (include the app_label)
        try:
            app_label = 'your_app_name'  # replace with your actual app name
            ModelClass = apps.get_model(app_label=app_label, model_name=model_name)
        except LookupError:
            return Response({'error': f'Model {model_name} not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Perform the deletion
        try:
            objects_to_delete = ModelClass.objects.filter(id__in=delete_ids)
            count, _ = objects_to_delete.delete()
            return Response({'message': f'Successfully deleted {count} records.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
