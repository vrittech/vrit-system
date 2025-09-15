from rest_framework.routers import DefaultRouter

from notification.viewsets.notificationviewset import NotificationUserViewsets, NotificationViewsets

router = DefaultRouter()


router.register('notification', NotificationViewsets, basename="notificationViewsetsTest")
router.register('notification_test_user', NotificationUserViewsets, basename="NotificationUserViewsets")