from rest_framework.permissions import BasePermission

# Define a mapping between models and their app labels
MODEL_MAP = {
    'project': ('projects', 'Project'),
    'project-service': ('projects', 'ProjectService'),
    'project-group': ('projects', 'ProjectGroup'),
    'blog': ('blog', 'Blog'),
    'blog-tags': ('blog', 'BlogTags'),
    'blog-category': ('blog', 'BlogCategory'),
    'career': ('career', 'Career'),
    'case-study': ('casestudy', 'CaseStudy'),
    'case-study-tags': ('casestudy', 'CaseStudyTags'),
    'case-study-category': ('casestudy', 'CaseStudyCategory'),
    'clients': ('clients', 'Clients'),
    'faqs': ('faqs', 'Faq'),
    'forms': ('forms', 'Form'),
    'forms-category': ('forms', 'Category'),
    'plan': ('plan', 'Plan'),
    'testimonial': ('testimonial', 'Testimonial'),
    'department': ('department', 'Department'),
    'gallery': ('gallery', 'Gallery'),
    'social-media': ('socialmedia', 'SocialMedia'),
    'role': ('accounts', 'Group'),
    # Add or modify mappings as necessary
}

class GenericPermission(BasePermission):
    def has_permission(self, request, view):
        # Allow list action for all users without checking specific permissions
        if view.action == "list":
            return True

        # Determine the model name from the view's model_key or URL/serializer context
        model_key = getattr(view, 'model_key', None)
        if not model_key or model_key not in MODEL_MAP:
            return False  # Deny permission if model_key is not defined or not in MODEL_MAP

        # Retrieve the app label and model name from MODEL_MAP
        app_label, model_name = MODEL_MAP[model_key]

        # Define action to permission suffix mapping
        action_permission_suffix = {
            "retrieve": "view",
            "create": "add",
            "update": "change",
            "partial_update": "change",
            "destroy": "delete",
        }

        # Check if the action has a defined permission suffix
        if view.action in action_permission_suffix:
            permission_suffix = action_permission_suffix[view.action]
            # Construct the permission codename, e.g., 'app_label.view_modelname'
            permission_codename = f"{app_label}.{permission_suffix}_{model_name.lower()}"
            return request.user.has_perm(permission_codename)

        # Default to denying permission if no action matches
        return False


# from rest_framework.viewsets import ModelViewSet
# from .permissions import GenericPermission
# from .models import Project, Blog, BlogTags, BlogCategory
# from .serializers import ProjectSerializer, BlogSerializer, BlogTagsSerializer, BlogCategorySerializer

# class ProjectViewSet(ModelViewSet):
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [GenericPermission]
#     model_key = 'project'  # Set model_key for permission lookup

# class BlogViewSet(ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = [GenericPermission]
#     model_key = 'blog'  # Set model_key for permission lookup

# class BlogTagsViewSet(ModelViewSet):
#     queryset = BlogTags.objects.all()
#     serializer_class = BlogTagsSerializer
#     permission_classes = [GenericPermission]
#     model_key = 'blog-tags'  # Set model_key for permission lookup

# class BlogCategoryViewSet(ModelViewSet):
#     queryset = BlogCategory.objects.all()
#     serializer_class = BlogCategorySerializer
#     permission_classes = [GenericPermission]
#     model_key = 'blog-category'  # Set model_key for permission lookup
