from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
from django.db import transaction
from django.db.models import F, Max,Min
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class PositionManagementViewSet(viewsets.ViewSet):

    # Mapping of frontend identifiers to actual model names
    MODEL_MAP = {
        'user': ('accounts', 'CustomUser'),
        'group': ('accounts', 'GroupExtension'),
        # 'project': ('projects', 'Project'),
        # 'project-service': ('projects', 'ProjectService'),
        'services':("services",'Services'),
        'services-category':("services",'ServicesCategory'),
        # 'project-category': ('projects', 'ProjectGroup'),
        
        'career': ('career', 'Career'),
        'career-category': ('career', 'CareerCategory'),
        'experience-level':('career', 'ExperienceLevel'),
        'case-study': ('casestudy', 'CaseStudy'),
        'clients': ('clients', 'Clients'),
        'faqs': ('faqs', 'Faqs'),
        'faqs-category': ('faqs', 'FaqsCategory'),
        'contact-us': ('faqs', 'ContactUs'),
        'forms': ('forms', 'Form'),
        'forms-category': ('forms', 'Category'),
        'plan': ('plan', 'Plan'),
        'testimonial': ('testimonial', 'Testimonial'),
        'department': ('department', 'Department'),
        'gallery': ('gallery', 'Gallery'),
        'social-media': ('socialmedia', 'SocialMedia'),
        'role': ('accounts', 'Group'),

        'custom-gallery': ('customgallery','CustomGallery'),
        'custom-gallery-position': ('customgallery','Position'),
        'custom-gallery-category': ('customgallery','CustomGalleryCategory'),

        'project':('project','Project'),
        'project-category':('project','ProjectCategory'),

        'blog': ('blogs', 'Blog'),
        'blog-category': ('blogs','BlogCategory'),

        'web-branding': ('web_branding', 'WebBranding'),
        'web-branding-category': ('web_branding','WebBrandingCategory')
        # Add or modify mappings as necessary
    }

    BREATH_HOLD = 10  # Maximum distance for small moves
    def _get_model(self, model_key):
        """
        Retrieve model class based on model key.
        """
        model_info = self.MODEL_MAP.get(model_key)
        if model_info:
            app_label, model_name = model_info
            try:
                return apps.get_model(app_label, model_name)
            except LookupError:
                return None
        return None
    
    @swagger_auto_schema(
    method='get',
    operation_summary="Move an item to a new position",
    operation_description=(
        "Moves an item from `target` position to `goal` position within the specified `model`.\n\n"
        "**Keys:**\n"
        "- `duration`\n"
        "- `event-gallery`\n"
        "- `event`\n"
    ),
    manual_parameters=[
        openapi.Parameter('model', openapi.IN_QUERY, description="Name of the model", type=openapi.TYPE_STRING, required=True),
        openapi.Parameter('target', openapi.IN_QUERY, description="Current ID of the item", type=openapi.TYPE_INTEGER, required=True),
        openapi.Parameter('goal', openapi.IN_QUERY, description="Target ORDER for the item", type=openapi.TYPE_INTEGER, required=True),
    ],
    responses={
        200: openapi.Response("Item moved successfully"),
        400: openapi.Response("Invalid request"),
        404: openapi.Response("Target object not found"),
    }
)

    @action(detail=False, methods=['get'], url_path='drag-item')
    def draggable(self, request, *args, **kwargs):
        model_name = request.GET.get('model')
        target_position = request.GET.get('target')
        goal_position = request.GET.get('goal')
        breath_hold = self.BREATH_HOLD

        if not model_name or target_position is None or goal_position is None:
            return Response({"error": "Model name, target, or goal position not provided"}, status=400)

        # Load the model
        Model = self._get_model(model_name)
        if Model is None:
            return Response({"error": f"Model '{model_name}' not found"}, status=400)

        # Convert positions to integers
        try:
            target_position = int(target_position)
            goal_position = int(goal_position)
        except ValueError:
            return Response({"error": "Invalid target or goal position"}, status=400)

        # Fetch the target object
        try:
            target_obj = Model.objects.get(id=target_position)
        except Model.DoesNotExist:
            return Response({"error": "Target object not found"}, status=400)
        except:
            return Response({"error": "multiple records detected"}, status=400)
        
  
        of_object = Model.objects.get(id=target_position)
        of_object.to(int(goal_position))
        return Response({"success": "Position updated successfully"}, status=200)