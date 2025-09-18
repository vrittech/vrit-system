from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# from blog.models import Blog
from blogs.models import Blog, BlogCategory
from customgallery.models import CustomGallery
from career.models import Career, CareerCategory, ExperienceLevel
from careergallery.models import CareerGallery, Album
from clients.models import Clients
from faqs.models import Faqs, FaqsCategory
from project.models import Project, ProjectCategory
from services.models import Services, ServicesCategory
from testimonial.models import Testimonial
from casestudy.models import CaseStudy
from newslettersubscription.models import NewsLetterSubscription
from inquires.models import Inquires
from plan.models import Plan
from forms.models import Forms, Category as FormsCategory
from web_branding.models import Position, WebBranding, WebBrandingCategory

VALID_TYPES = {
    "services": Services,
    "services-category": ServicesCategory,
    "career": Career,
    "career-category": CareerCategory,
    "experience-level": ExperienceLevel,
    "careergallery": CareerGallery,
    "album": Album,
    "clients": Clients,
    "faqs": Faqs,
    "faqs-category": FaqsCategory,
    "testimonial": Testimonial,
    "casestudy": CaseStudy,
    "newsletter-subscription": NewsLetterSubscription,
    "inquiries": Inquires,
    "plan": Plan,
    "forms": Forms,
    "forms-category": FormsCategory,
    "custom-gallery": CustomGallery,
    "project": Project,
    "project-category": ProjectCategory,
    "blog": Blog,
    "blog-category": BlogCategory,
    "web-branding": WebBranding,
    "web-branding-category": WebBrandingCategory,
    "web-branding-position": Position

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
                    description='Type of model to delete from. Options: blog, project, project_service, career, clients, faqs, testimonial, case_study.'
                ),
            },
            required=['delete_ids', 'type'],
        ),
        operation_summary="Bulk Delete Records",
        operation_description="Deletes records in bulk based on the provided IDs and type.",
        responses={
            200: openapi.Response(description="Data successfully deleted in bulk"),
            400: openapi.Response(description="Invalid request parameters or unknown data type"),
        }
    )
    def post(self, request, *args, **kwargs):
        # Extract 'delete_ids' and 'type' from request data
        delete_ids = request.data.get('delete_ids')
        delete_type = request.data.get('type')

        # Validate input: Check for missing or invalid input
        if not delete_ids or not isinstance(delete_ids, list) or not all(isinstance(id, int) for id in delete_ids):
            return Response(
                {"error": "Invalid 'delete_ids'. Provide a list of integers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not delete_type or delete_type not in VALID_TYPES:
            return Response(
                {"error": "Invalid or missing 'type'. Provide a valid type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get the model based on delete_type
        model = VALID_TYPES[delete_type]
        
        # Fetch the queryset based on the provided IDs
        queryset = model.objects.filter(id__in=delete_ids)

        # Check if any of the delete_ids do not exist
        existing_ids = list(queryset.values_list('id', flat=True))
        missing_ids = set(delete_ids) - set(existing_ids)

        if missing_ids:
            return Response(
                {"error": f"IDs not found: {list(missing_ids)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Perform the bulk deletion
        # deleted_count, _ = queryset.delete()
        deleted_count = queryset.count()
        queryset.delete()
        return Response(
            {"message": f"Successfully deleted {deleted_count} items of type '{delete_type}'."},
            status=status.HTTP_200_OK
        )
