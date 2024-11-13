# from rest_framework import viewsets
# from rest_framework.filters import SearchFilter, OrderingFilter
# from django_filters.rest_framework import DjangoFilterBackend
# from ..models import Notification
# from ..serializers.notification_serializers import NotificationListSerializers, NotificationRetrieveSerializers, NotificationWriteSerializers
# from ..utilities.importbase import *
# from rest_framework import viewsets, permissions
# from rest_framework.response import Response
# from rest_framework.decorators import action


# class notificationViewsets(viewsets.ModelViewSet):
#     serializer_class = NotificationListSerializers
#     # permission_classes = [notificationsPermission]
#     # authentication_classes = [JWTAuthentication]
#     #pagination_class = MyPageNumberPagination
#     queryset = Notification.objects.all()

#     filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
#     search_fields = ['id']
#     ordering_fields = ['id']

#     # filterset_fields = {
#     #     'id': ['exact'],
#     # }

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset

#     def get_serializer_class(self):
#         if self.action in ['create', 'update', 'partial_update']:
#             return NotificationWriteSerializers
#         elif self.action == 'retrieve':
#             return NotificationRetrieveSerializers
#         return super().get_serializer_class()

#     # @action(detail=False, methods=['get'], name="action_name", url_path="url_path")
#     # def action_name(self, request, *args, **kwargs):
#     #     return super().list(request, *args, **kwargs)
    
#     @action(detail=False, methods=['post'], url_path='mark-as-read')
#     def mark_as_read(self, request):
#         # Mark specific notifications as read
#         notification_ids = request.data.get('ids', [])
#         self.request.user.notifications.filter(id__in=notification_ids).update(is_read=True)
#         return Response({"status": "Notifications marked as read"})

#     @action(detail=False, methods=['post'], url_path='mark-all-as-read')
#     def mark_all_as_read(self, request):
#         # Mark all unread notifications as read for the user
#         self.request.user.notifications.update(is_read=True)
#         return Response({"status": "All notifications marked as read"})

