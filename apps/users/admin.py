from django.contrib import admin
from apps.users.models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone_number')
        }),
        ('Role y Estado', {
            'fields': ('role', 'is_verified', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Perfil', {
            'fields': ('profile_image',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at', 'last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'date_joined']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['get_username', 'city', 'country']
    list_filter = ['country', 'city']
    search_fields = ['user__username', 'address', 'city']
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Usuario'
