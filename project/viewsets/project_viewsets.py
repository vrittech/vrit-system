from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from project.models import CaseStudy, Project, ProjectCategory
from project.serializers.project_serializers import CaseStudyListSerializers, CaseStudyRetrieveSerializers, CaseStudyWriteSerializers, ProjectCategoryListSerializers, ProjectCategoryRetrieveSerializers, ProjectCategoryWriteSerializers, ProjectListSerializers, ProjectRetrieveSerializers, ProjectWriteSerializers
from project.utilities.filter import ProjectFilter
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response

class projectViewsets(viewsets.ModelViewSet):
    serializer_class = ProjectListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = Project.objects.all().order_by('-order').distinct()
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        if str(lookup_value).isdigit():
            return get_object_or_404(Project, pk=lookup_value)
        return get_object_or_404(Project, slug=lookup_value)

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['question']
    ordering_fields = ['question','order']
    # ('title', 'description', 'position', 'created_at', 'updated_at', )
    filterset_class = ProjectFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectWriteSerializers
        elif self.action == 'retrieve':
            return ProjectRetrieveSerializers
        return super().get_serializer_class()


   
class projectCategoryViewsets(viewsets.ModelViewSet):
    serializer_class = ProjectCategoryListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    queryset = ProjectCategory.objects.all().order_by('-order')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    filterset_fields = {
        'id': ['exact'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCategoryWriteSerializers
        elif self.action == 'retrieve':
            return ProjectCategoryRetrieveSerializers
        return super().get_serializer_class()


    
class caseStudyViewsets(viewsets.ModelViewSet):
    serializer_class = CaseStudyListSerializers
    # permission_classes = [faqsPermission]
    # authentication_classes = [JWTAuthentication]
    pagination_class = MyPageNumberPagination
    # queryset = CaseStudy.objects.all().order_by('-order').distinct()
    queryset = CaseStudy.objects.all().order_by('-order')
    lookup_field = "project__slug"

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # search_fields = ['question']
    # ordering_fields = ['question','order']
    # filterset_class = ProjectFilter

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