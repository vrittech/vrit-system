from rest_framework import serializers
from ..models import CareerGallery,Album

class AlbumListSerializers__CareerGallery(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class CareerGalleryListSerializers(serializers.ModelSerializer):
    album = AlbumListSerializers__CareerGallery()
    class Meta:
        model = CareerGallery
        fields = '__all__'

class CareerGalleryRetrieveSerializers(serializers.ModelSerializer):
    class Meta:
        model = CareerGallery
        fields = '__all__'

class CareerGalleryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = CareerGallery
        fields = '__all__'