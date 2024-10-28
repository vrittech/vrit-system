from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Blog
from ..serializers.blog_serializers import BlogListSerializers, BlogRetrieveSerializers, BlogWriteSerializers
from ..utilities.importbase import *
from rest_framework.response import Response
from blog.utilities.permissions import blogPermission
from rest_framework.decorators import action


class blogViewsets(viewsets.ModelViewSet):
    serializer_class = BlogListSerializers
    # permission_classes = [blogPermission]
    pagination_class = MyPageNumberPagination
    queryset = Blog.objects.all().order_by('position')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title','description','site_title','excerpt','meta_keywords','tags__tag_names']
    ordering_fields = ['id','title', 'description', 'site_title', 'excerpt', 'status','tags__tag_names']
    # ('title', 'description', 'site_title', 'excerpt', 'status', ',('published','Published'),('scheduled','Scheduled')),max_length', 'meta_description', 'meta_keywords', 'meta_author', 'tags', )

    filterset_fields = {
        'title':['exact'],
        'status':['exact'],
        'publish_date':['exact','gte','lte'],
        'category':['exact'],
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

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
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

