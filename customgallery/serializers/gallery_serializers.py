from rest_framework import serializers
from ..models import CustomGallery as Gallery, Position

class PositionListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

class PositionWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'


class GalleryListSerializers(serializers.ModelSerializer):
    position= PositionListSerializers()
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryRetrieveSerializers(serializers.ModelSerializer):
    position= PositionListSerializers()
    class Meta:
        model = Gallery
        fields = '__all__'

class GalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'