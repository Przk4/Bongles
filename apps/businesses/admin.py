from django.contrib import admin
from apps.businesses.models import Business, BusinessCategory, BusinessReview


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'city', 'rating', 'is_verified', 'is_active']
    list_filter = ['city', 'is_verified', 'is_active', 'created_at']
    search_fields = ['name', 'owner__username', 'city']
    readonly_fields = ['created_at', 'updated_at', 'rating', 'total_reviews']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('owner', 'name', 'description', 'logo', 'banner')
        }),
        ('Ubicación', {
            'fields': ('address', 'city', 'postal_code', 'latitude', 'longitude')
        }),
        ('Contacto', {
            'fields': ('phone_number', 'email', 'website')
        }),
        ('Horarios y Estado', {
            'fields': ('opening_time', 'closing_time', 'is_open', 'is_active')
        }),
        ('Ratings', {
            'fields': ('rating', 'total_reviews')
        }),
        ('Verificación', {
            'fields': ('is_verified',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(BusinessReview)
class BusinessReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_username', 'business', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'business']
    search_fields = ['customer__username', 'business__name']
    readonly_fields = ['created_at', 'updated_at']
    
    def customer_username(self, obj):
        return obj.customer.username
    customer_username.short_description = 'Cliente'
