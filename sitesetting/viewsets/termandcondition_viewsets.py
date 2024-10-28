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
    
            
    @action(detail=False, methods=['post'], name="create-update", url_path="create-terms-and-conditions")
    def action_name(self, request, *args, **kwargs):
            description = request.data.get('description', None)
            
            if description is None:
                return Response({"data": None}, status=status.HTTP_200_OK)
            
            term_and_condition = TermAndCondition.objects.all()
            
            if term_and_condition.exists():
                # Update the existing term and condition
                term_and_condition = term_and_condition.first()
                term_and_condition.description = description
                term_and_condition.save()
                return Response({"message": "Terms and conditions updated successfully."}, status=status.HTTP_200_OK)
            else:
                # Create a new term and condition
                new_term_and_condition = TermAndCondition.objects.create(description=description)
                return Response({"message": "Terms and conditions created successfully.", "id": new_term_and_condition.id}, status=status.HTTP_201_CREATED)
            
    @action(detail=False, methods=['get', 'put'], name="retrieve-update", url_path="detail-terms-and-conditions")
    def retrieve_update_term_and_condition(self, request, *args, **kwargs):
            try:
                # Assuming there's only one term and condition, get the first one.
                term_and_condition = TermAndCondition.objects.first()
                
                if not term_and_condition:
                    return Response({"error": "Term and Condition not found."}, status=status.HTTP_404_NOT_FOUND)
            
            except TermAndCondition.DoesNotExist:
                return Response({"error": "Term and Condition not found."}, status=status.HTTP_404_NOT_FOUND)

            if request.method == 'GET':
                # Retrieve the term and condition
                serializer = TermAndConditionRetrieveSerializers(term_and_condition)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif request.method == 'PUT':
                # Update the term and condition
                description = request.data.get('description', None)
                
                if description is None:
                    return Response({"error": "Description is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                term_and_condition.description = description
                term_and_condition.save()
                return Response({"message": "Term and Condition updated successfully."}, status=status.HTTP_200_OK)



