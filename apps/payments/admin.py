from django.contrib import admin
from apps.payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status', 'method', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['order__id', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
