from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import TermAndCondition
from ..serializers.termandcondition_serializers import TermAndConditionListSerializers, TermAndConditionRetrieveSerializers, TermAndConditionWriteSerializers
from ..utilities.importbase import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

class termandconditionViewsets(viewsets.ModelViewSet):
    serializer_class = TermAndConditionListSerializers
    # permission_classes = [sitesettingPermission]
    # authentication_classes = [JWTAuthentication]
    #pagination_class = MyPageNumberPagination
    queryset = TermAndCondition.objects.all()

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    # filterset_fields = {
    #     'id': ['exact'],
    # }

    def get_queryset(self):
        queryset = super().get_queryset()
        #return queryset.filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TermAndConditionWriteSerializers
        elif self.action == 'retrieve':
            return TermAndConditionRetrieveSerializers
        return super().get_serializer_class()

    # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
    # def action_name(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    
            
    @action(detail=False, methods=['get', 'post', 'put', 'patch'], name="manage-terms-and-conditions", url_path="terms-and-conditions")
    def manage_terms_and_conditions(self, request, *args, **kwargs):
        """
        Handles creating, retrieving, updating, and partially updating the Terms and Conditions.
        """
        # Fetch the first terms and conditions, assuming there's only one
        term_and_condition = TermAndCondition.objects.first()

        if request.method == 'GET':
            # Retrieve the existing terms and conditions
            if not term_and_condition:
                return Response({"data": None}, status=status.HTTP_200_OK)
            serializer = TermAndConditionRetrieveSerializers(term_and_condition)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method in ['POST', 'PUT', 'PATCH']:
            description = request.data.get('description', None)

            if description is None:
                return Response({"error": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)

            if term_and_condition:
                # Update the existing terms and conditions
                term_and_condition.description = description
                term_and_condition.save()
                return Response({"message": "Terms and conditions updated successfully."}, status=status.HTTP_200_OK)
            else:
                # Create new terms and conditions
                new_term_and_condition = TermAndCondition.objects.create(description=description)
                return Response({"message": "Terms and conditions created successfully.", "id": new_term_and_condition.id}, status=status.HTTP_201_CREATED)