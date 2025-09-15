from rest_framework import serializers

class PositionManagementSerializers(serializers.Serializer):
    model = serializers.CharField()
    target = serializers.IntegerField() #it is target like from, it means 11 position id is goining to drag to goal
    goal = serializers.IntegerField() #target to switch goal

