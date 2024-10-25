from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import ExperienceLevel
from ..serializers.expriencelevel_serializers import ExperienceLevelListSerializers, ExperienceLevelRetrieveSerializers, ExperienceLevelWriteSerializers
from ..utilities.importbase import *
from ..utilities.carrer_filter import CareerFilter

class expriencelevelViewsets(viewsets.ModelViewSet):
    serializer_class = ExperienceLevelListSerializers
    # permission_classes = [careerPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ExperienceLevel.objects.all().order_by('created_at')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id','title','expiration_date','created_at']
    # ('title', 'experience_level', 'description', 'position', 'num_of_vacancy', 'apply_link', 'image', 'is_show', 'enable_auto_expiration', 'expiration_date', 'created_at', 'updated_at', )

    filterset_class = CareerFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ExperienceLevelWriteSerializers
        elif self.action == 'retrieve':
            return ExperienceLevelRetrieveSerializers
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        """
        Override the default create method to handle bulk creation of experience levels.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Experience levels saved successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

