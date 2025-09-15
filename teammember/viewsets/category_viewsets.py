from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from teammember.serializers.category_serializers import TeamMemberCategoryListSerializers, TeamMemberCategoryRetrieveSerializers, TeamMemberCategoryWriteSerializers

from ..models import TeamMember
from ..serializers.teammember_serializers import (
    TeamMemberListSerializer,
    TeamMemberRetrieveSerializer,
    TeamMemberWriteSerializer,
)
from ..utilities.importbase import *
from rest_framework import permissions


class TeamMemberCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberCategoryListSerializers
    pagination_class = MyPageNumberPagination
    # permission_classes = [permissions.IsAuthenticated]

    queryset = TeamMember.objects.all().order_by("joined_at")

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = [
        "user__email",
        "user__full_name",
    ]
    ordering_fields = ["id", "joined_at"]

    filterset_fields = {
        "id": ["exact"],
        "joined_at": ["exact", "gte", "lte"],
        "user__is_superuser": ["exact"],
    }

    def get_queryset(self):
        queryset = super().get_queryset().distinct().order_by("joined_at")
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return TeamMemberCategoryWriteSerializers
        elif self.action == "retrieve":
            return TeamMemberCategoryRetrieveSerializers
        return TeamMemberListSerializer
    
