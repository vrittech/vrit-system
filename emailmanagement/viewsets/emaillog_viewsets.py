from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from ..models import EmailLog
from ..serializers.emaillog_serializers import EmailLogListSerializers, EmailLogRetrieveSerializers, EmailLogWriteSerializers
from ..utilities.filters import EmailLogFilter 

class emaillogViewsets(viewsets.ModelViewSet):
    serializer_class = EmailLogListSerializers
    queryset = EmailLog.objects.all().order_by('-created_at')

    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id', 'date', 'time', 'subject', 'purpose', 'recipient']
    ordering_fields = ['id', 'date', 'time', 'subject', 'purpose', 'recipient']
    filterset_class = EmailLogFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return EmailLogWriteSerializers
        elif self.action == 'retrieve':
            return EmailLogRetrieveSerializers
        return super().get_serializer_class()

    @action(detail=False, methods=['get'], url_path='recipient-count', name='Recipient Count')
    def recipient_count(self, request, *args, **kwargs):
        """
        Custom action to return the count of distinct recipients
        along with the filtered queryset.
        """
        # Apply filtering
        queryset = self.filter_queryset(self.get_queryset())
        recipient_count = queryset.values('recipient').distinct().count()

        # Get the usual serialized data
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'count': recipient_count, 'results': serializer.data})

        serializer = self.get_serializer(queryset, many=True)
        return Response({'count': recipient_count, 'results': serializer.data})
    
    @action(detail=True, methods=['post'], url_path='email-action', name='Email Action')
    def email_action(self, request, pk=None):
        """
        Single endpoint to handle sending, scheduling, changing schedule time, and canceling email.
        """
        email_log = self.get_object()
        action_type = request.data.get('action_type')

        if action_type == 'send_now':
            # Handle 'Send Now' action
            success = email_log.send_email()
            if success:
                return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
            return Response({'message': 'Failed to send email.'}, status=status.HTTP_400_BAD_REQUEST)

        elif action_type == 'schedule':
            # Handle 'Schedule Email' action
            serializer = EmailLogScheduleSerializer(data=request.data)
            if serializer.is_valid():
                email_log.scheduled_at = serializer.validated_data['scheduled_at']
                email_log.status = 'scheduled'
                email_log.save()
                return Response({'message': 'Email scheduled successfully!'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action_type == 'change_time':
            # Handle 'Change Schedule Time' action
            serializer = EmailLogScheduleSerializer(data=request.data)
            if serializer.is_valid():
                email_log.scheduled_at = serializer.validated_data['scheduled_at']
                email_log.save()
                return Response({'message': 'Scheduled time updated successfully!'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action_type == 'cancel':
            # Handle 'Cancel Scheduled Email' action
            if email_log.status == 'scheduled':
                email_log.status = 'canceled'
                email_log.scheduled_at = None
                email_log.save()
                return Response({'message': 'Scheduled email canceled successfully!'}, status=status.HTTP_200_OK)
            return Response({'message': 'Email is not scheduled or already canceled.'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'message': 'Invalid action type.'}, status=status.HTTP_400_BAD_REQUEST)
