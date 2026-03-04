from django.contrib import admin
from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'business', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'business', 'created_at']
    search_fields = ['customer__username', 'business__name']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    inlines = [OrderItemInline]
