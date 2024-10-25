from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from blog.models import Blog
from projects.models import Project,ProjectService
from career.models import Career
from clients.models import Clients
from faqs.models import Faqs
from testimonial.models import Testimonial
from casestudy.models import CaseStudy

VALID_TYPES = {
    "blog": Blog,
    "project": Project,
    "project_service": ProjectService,
    "career": Career,
    "clients": Clients,
    "faqs": Faqs,
    "testimonial": Testimonial,
    "case_study": CaseStudy,
}

class BulkDelete(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'delete_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='List of IDs to be deleted'
                ),
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Type of model to delete from. Options: blog, destination, package, queries, booking, activities, collection.'
                ),
            },
            required=['delete_ids', 'type'],
        ),
        operation_summary="Bulk Delete records",
        operation_description="Deletes records in bulk based on the provided IDs and type.",
        responses={
            200: openapi.Response(description="Data successfully deleted in bulk"),
            400: openapi.Response(description="Invalid request parameters or unknown data type"),
        }
    )
    def post(self, request, *args, **kwargs):
        delete_ids = request.data.get('delete_ids')
        delete_type = request.data.get('type')

        if not delete_ids or not delete_type:
            return Response({"error": "Missing delete_ids or type in the request"}, status=status.HTTP_400_BAD_REQUEST)

        if delete_type not in VALID_TYPES:
            return Response({"error": 'Unknown data type'}, status=status.HTTP_400_BAD_REQUEST)
        
        model = VALID_TYPES[delete_type]
        query = model.objects.filter(id__in=delete_ids)

        # Check if any of the delete_ids do not exist
        if query.count() != len(delete_ids):
            return Response({"error": "Some IDs do not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the deletion
        query.delete()

        return Response({"message": "Data successfully deleted in bulk"}, status=status.HTTP_200_OK)
