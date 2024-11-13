from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Blog, BlogTags
from ..serializers.blog_serializers import BlogListSerializers, BlogRetrieveSerializers, BlogWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from blog.utilities.permissions import blogPermission
from rest_framework.decorators import action
from ..utilities.filter import BlogFilter
from django.db.models import Count


class blogViewsets(viewsets.ModelViewSet):
    serializer_class = BlogListSerializers
    # permission_classes = [blogPermission]
    pagination_class = MyPageNumberPagination
    queryset = Blog.objects.all().order_by('position')
    lookup_field = "slug"
    filterset_class = BlogFilter
    
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title','description','site_title','excerpt','meta_keywords','tags__tag_names']
    ordering_fields = ['id','title', 'description', 'site_title', 'excerpt', 'status','tags__tag_names']
    # ('title', 'description', 'site_title', 'excerpt', 'status', ',('published','Published'),('scheduled','Scheduled')),max_length', 'meta_description', 'meta_keywords', 'meta_author', 'tags', )

    filterset_fields = {
        'title':['exact'],
        'status':['exact'],
        'publish_date':['exact','gte','lte'],
        'category':['exact'],
        'is_deleted':['exact'],
        'user':['exact']
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BlogWriteSerializers
        elif self.action == 'retrieve':
            return BlogRetrieveSerializers
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='authors')
    def authors(self, request):
        # Get a distinct list of authors from the Blog model
        authors = Blog.objects.values_list('author', flat=True).distinct()
        
        # Convert the QuerySet to a list and return it in the response
        return Response(list(authors))
    
    @action(detail=False, methods=['get'], url_path='status-counts')
    def status_counts(self, request):
        # All possible statuses
        all_statuses = dict(Blog._meta.get_field('status').choices)

        # Get the counts for each status from the database
        status_counts = Blog.objects.values('status').annotate(count=Count('id'))

        # Convert the QuerySet result into a dictionary with counts
        status_count_dict = {item['status']: item['count'] for item in status_counts}

        # Ensure all statuses are represented, even if count is 0
        complete_status_counts = [
            {"name": all_statuses[status], "count": status_count_dict.get(status, 0)}
            for status in all_statuses.keys()
        ]

        # # Get the count of blogs where `is_deleted` is True
        # deleted_count = Blog.objects.filter(is_deleted=True).count()

        # Prepare the response data
        response_data = {
            'status_counts': complete_status_counts,
            # 'deleted_count': deleted_count,
            'total_count': Blog.objects.count(),  # Total number of blogs
        }
        
        return Response(response_data)
    
    @action(detail=False, methods=['get'], name="draggableBlog", url_path="drag-blog")
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
            target_obj = Blog.objects.get(position=target_position)
            goal_obj = Blog.objects.get(position=goal_position)
        except Blog.DoesNotExist:
            return Response({"error": "Target or Goal object not found"}, status=400)

        if target_position < goal_position:
            # Moving target down (target goes after goal)
            affected_objs = Blog.objects.filter(
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
            affected_objs = Blog.objects.filter(
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
    
    @action(detail=False, methods=['get'], name="recent_tags", url_path="recent-tags")
    def recent_tags(self, request, *args, **kwargs):
        # Fetch recent blogs without slicing to avoid the distinct() limitation
        recent_blogs = Blog.objects.filter(tags__isnull=False).order_by('-created_at')
        
        # If no recent blogs with tags, return an appropriate message
        if not recent_blogs.exists():
            return Response({"message": "No recent tags used"})

        # Get distinct tag IDs from recent blogs (without slicing)
        recent_tag_ids = recent_blogs.values_list('tags', flat=True).distinct()
        
        # Fetch tags with annotation for blog usage frequency
        recent_tags = BlogTags.objects.filter(id__in=recent_tag_ids).annotate(blog_count=Count('blog')).order_by('-blog_count')

        # Serialize tags or create a simple response
        tag_data = [{"id": tag.id, "name": tag.name, "blog_count": tag.blog_count} for tag in recent_tags]
        
        return Response(tag_data)