from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import NotificationPerUser, NotificationUser
from ..serializers.notification_serializers import NotificationListSerializers, NotificationRetrieveSerializers, NotificationUserListSerializers, NotificationWriteSerializers
from ..utilities.importbase import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action


class NotificationViewsets(viewsets.ModelViewSet):
    serializer_class = NotificationListSerializers
    queryset = NotificationPerUser.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    def get_queryset(self):
        # Return only NotificationPerUser instances associated with the current user
        return NotificationPerUser.objects.filter(
            notification_users__user=self.request.user
        ).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return NotificationWriteSerializers
        elif self.action == 'retrieve':
            return NotificationRetrieveSerializers
        return super().get_serializer_class()
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page if page is not None else queryset, many=True)

        total_unread = NotificationUser.objects.filter(user=request.user, is_read=False).count()

        if page is not None:
            paginated_response = self.get_paginated_response(serializer.data)
            paginated_response.data['total_unread'] = total_unread  # Add it at top level
            return paginated_response

        return Response({
            "total_unread": total_unread,
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='mark-as-read')
    def mark_as_read(self, request):
        notification_id = request.data.get('id', None)  # expecting a single NotificationPerUser ID
        print("wohoo")
        print(notification_id)
        print("wohoo000")
        if not notification_id:
            return Response({"status": "No ID provided"}, status=400)

        # Filter NotificationUser object for this notification ID and the current user
        try:
            notification_user = NotificationUser.objects.get(notification_id=notification_id, user=request.user)
            print(notification_user)
        except NotificationUser.DoesNotExist:
            return Response({"status": "ID not found"}, status=404)

        notification_user.is_read = True
        notification_user.save()

        return Response({"status": "Notification marked as read"})


    @action(detail=False, methods=['post'], url_path='mark-all-as-read')
    def mark_all_as_read(self, request):
        NotificationUser.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({"status": "All notifications marked as read"})
    


class NotificationUserViewsets(viewsets.ModelViewSet):
    serializer_class = NotificationUserListSerializers
    queryset = NotificationUser.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']