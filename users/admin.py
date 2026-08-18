from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__email', 'department']
    list_filter = ['role', 'is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']