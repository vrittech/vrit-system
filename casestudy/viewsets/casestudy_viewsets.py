# from rest_framework import viewsets
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from ..models import CaseStudy
# from ..serializers.casestudy_serializers import CaseStudyListSerializers, CaseStudyRetrieveSerializers, CaseStudyWriteSerializers
# from ..utilities.importbase import *

# class casestudyViewsets(viewsets.ModelViewSet):
#     serializer_class = CaseStudyListSerializers
#     # permission_classes = [casestudyPermission]
#     # authentication_classes = [JWTAuthentication]
#     pagination_class = MyPageNumberPagination
#     queryset = CaseStudy.objects.all()

#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     search_fields = ['id']
#     ordering_fields = ['id']

#     # filterset_fields = {
#     #     'id': ['exact'],
#     # }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset
#         #return queryset.filter(user_id=self.request.user.id)

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return CaseStudyWriteSerializers
#         elif self.action == 'retrieve':
#             return CaseStudyRetrieveSerializers
#         return super().get_serializer_class()

#     # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
#     # def action_name(self, request, *args, **kwargs):
#     #     return super().list(request, *args, **kwargs)

from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import CaseStudy, CaseStudyTags
from ..serializers.casestudy_serializers import CaseStudyListSerializers, CaseStudyRetrieveSerializers, CaseStudyWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from casestudy.utilities.permissions import casestudyPermission
from rest_framework.decorators import action
from ..utilities.filter import CaseStudyFilter
from django.db.models import Count


class casestudyViewsets(viewsets.ModelViewSet):
    serializer_class = CaseStudyListSerializers
    # permission_classes = [casestudyPermission]
    pagination_class = MyPageNumberPagination
    queryset = CaseStudy.objects.all().order_by('position')
    lookup_field = "slug"
    filterset_class = CaseStudyFilter
     
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title','description','site_title','excerpt','meta_keywords','tags__tag_names']
    ordering_fields = ['id','title', 'description', 'site_title', 'excerpt', 'status','tags__tag_names']
    # ('title', 'description', 'site_title', 'excerpt', 'status', ',('published','Published'),('scheduled','Scheduled')),max_length', 'meta_description', 'meta_keywords', 'meta_author', 'tags', )

    # filterset_fields = {
    #     'title':['exact'],
    #     'status':['exact'],
    #     'publish_date':['exact','gte','lte'],
    #     'category':['exact'],
    #     'is_deleted':['exact'],
    #     'user':['exact']
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CaseStudyWriteSerializers
        elif self.action == 'retrieve':
            return CaseStudyRetrieveSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'], url_path='authors')
    def authors(self, request):
        # Get a distinct list of authors from the Blog model
        authors = CaseStudy.objects.values_list('author', flat=True).distinct()
        
        # Convert the QuerySet to a list and return it in the response
        return Response(list(authors))

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='status-counts')
    def status_counts(self, request):
        # All possible statuses
        all_statuses = dict(CaseStudy._meta.get_field('status').choices)

        # Get the counts for each status from the database
        status_counts = CaseStudy.objects.values('status').annotate(count=Count('id'))

        # Convert the QuerySet result into a dictionary with counts
        status_count_dict = {item['status']: item['count'] for item in status_counts}

        complete_status_counts = [
            {"name": all_statuses[status], "count": status_count_dict.get(status, 0)}
            for status in all_statuses.keys()
        ]

        # Get the count of blogs where `is_deleted` is True
        # deleted_count = CaseStudy.objects.filter(is_deleted=True).count()

        # Prepare the response data
        response_data = {
            'status_counts': complete_status_counts,
            # 'deleted_count': deleted_count,
            'total_count': CaseStudy.objects.count(),  # Total number of blogs
        }
        
        return Response(response_data)

    @action(detail=False, methods=['get'], name="recent_tags", url_path="recent-tags")
    def recent_tags(self, request, *args, **kwargs):
        # Fetch recent case studies without slicing to avoid the distinct() limitation
        recent_case_studies = CaseStudy.objects.filter(tags__isnull=False).order_by('-created_at')
        
        # If no recent case studies with tags, return an appropriate message
        if not recent_case_studies.exists():
            return Response({"message": "No recent tags used"})

        # Get distinct tag IDs from recent case studies (without slicing)
        recent_tag_ids = recent_case_studies.values_list('tags', flat=True).distinct()
        
        # Fetch tags with annotation for case study usage frequency
        recent_tags = CaseStudyTags.objects.filter(id__in=recent_tag_ids).annotate(case_study_count=Count('casestudy')).order_by('-case_study_count')

        # Serialize tags or create a simple response
        tag_data = [{"id": tag.id, "name": tag.name, "case_study_count": tag.case_study_count} for tag in recent_tags]
        
        return Response(tag_data)
    
    @action(detail=False, methods=['get'], name="draggableCaseStudy", url_path="drag-case_study")
    def Draggable(self, request, *args, **kwargs):
        target_position = request.GET.get('target')  # Position of the target object
        goal_position = request.GET.get('goal')  # Position of the goal object

        from rest_framework.response import Response

        if not target_position or not goal_position:
            return Response({"error": "Target or Goal position not provided"}, status=400)

        # Convert to integers
        try:
            target_position = int(target_position)
            goal_position = int(goal_position)
        except ValueError:
            return Response({"error": "Invalid target or goal position"}, status=400)

        # Fetch the target and goal objects based on position
        try:
            target_obj = CaseStudy.objects.get(position=target_position)
            goal_obj = CaseStudy.objects.get(position=goal_position)
        except CaseStudy.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = CaseStudy.objects.filter(
                position__gt=target_position, position__lte=goal_position
            ).order_by('position')
            
            # Decrement position of all affected objects
            for obj in affected_objs:
                obj.position -= 1
                obj.save()

            # Set target object's new position
            target_obj.position = goal_position
            target_obj.save()

        else:
            # Moving target up (target goes before goal)
            affected_objs = CaseStudy.objects.filter(
                position__lt=target_position, position__gte=goal_position
            ).order_by('-position')

            # Increment position of all affected objects by 1
            for obj in affected_objs:
                obj.position += 1
                obj.save()

            # Set target object's new position (exact position of the goal)
            target_obj.position = goal_position
            target_obj.save()

        return Response({"status": "success"})


