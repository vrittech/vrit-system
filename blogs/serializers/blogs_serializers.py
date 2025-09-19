from rest_framework import serializers

from accounts.models import CustomUser
from teammember.models import TeamMember
from ..models import Blog, BlogCategory, BlogSEOSettings

class AuthorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.EmailField(source="user.email")
    professional_image = serializers.CharField(source="user.professional_image")

    class Meta:
        model = TeamMember
        fields = ['id','full_name', 'email', 'professional_image','position']



class BlogCategoryListSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogCategoryRetrieveSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = BlogCategory
        fields = '__all__'

class BlogCategoryWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = '__all__'


class BlogsListSerializers(serializers.ModelSerializer):
    author=AuthorSerializer()
    category= BlogCategoryRetrieveSerializers(many=True)
    blogSEOSettings_id = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = '__all__'

    def get_blogSEOSettings_id(self, obj):
        if hasattr(obj, "blogSEOSettings"):
            return obj.blogSEOSettings.id
        return None

class BlogsRetrieveSerializers(serializers.ModelSerializer):
    author=AuthorSerializer()
    category= BlogCategoryRetrieveSerializers(many=True)
    blogSEOSettings_id = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = '__all__'
    def get_blogSEOSettings_id(self, obj):
        if hasattr(obj, "blogSEOSettings"):
            return obj.blogSEOSettings.id
        return None

class BlogsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['author'] 


    


class BlogSEOSettingsListSerializers(serializers.ModelSerializer):
    blog = BlogsListSerializers() 
    class Meta:
        model = BlogSEOSettings
        fields = '__all__'

class BlogSEOSettingsRetrieveSerializers(serializers.ModelSerializer):
    blog = BlogsListSerializers() 
    class Meta:
        model = BlogSEOSettings
        fields = '__all__'

class BlogSEOSettingsWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = BlogSEOSettings
        fields = '__all__'
