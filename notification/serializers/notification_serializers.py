from notification.models import NotificationPerUser, NotificationUser
from rest_framework import serializers


class NotificationListSerializers(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = NotificationPerUser
        fields = "__all__"

    def get_is_read(self, obj):
        user = self.context['request'].user
        # get the NotificationUser instance for this user
        try:
            return NotificationUser.objects.get(notification=obj, user=user).is_read
        except NotificationUser.DoesNotExist:
            return False

class NotificationRetrieveSerializers(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = NotificationPerUser
        fields = "__all__"

    def get_is_read(self, obj):
        user = self.context['request'].user
        # get the NotificationUser instance for this user
        try:
            return NotificationUser.objects.get(notification=obj, user=user).is_read
        except NotificationUser.DoesNotExist:
            return False

class NotificationWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationPerUser
        fields = '__all__'

class NotificationUserListSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationUser
        fields = '__all__'