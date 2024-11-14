from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, GroupExtension

class CustomUserAdmin(BaseUserAdmin):
    exclude = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'avatar', 'professional_image', 'full_name', 'position', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'role')}),
    )
    list_display = ['username', 'email', 'full_name', 'position', 'department', 'is_active', 'is_staff','professional_image','avatar']
    search_fields = ['username', 'email', 'full_name']

admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(GroupExtension)
class GroupExtensionAdmin(admin.ModelAdmin):
    list_display = ['group', 'position']
    search_fields = ['group__name']
    list_filter = ['position']
    ordering = ['position']

    def save_model(self, request, obj, form, change):
        # Override save_model to handle custom position saving logic if needed
        super().save_model(request, obj, form, change)

# Unregister and register Group to customize admin panel if necessary
admin.site.unregister(Group)
admin.site.register(Group)
