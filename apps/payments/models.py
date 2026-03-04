from django.db import models
from apps.orders.models import Order


class Payment(models.Model):
    """Modelo para pagos."""
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('processing', 'Procesando'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
        ('refunded', 'Reembolsado'),
    )
    
    METHOD_CHOICES = (
        ('credit_card', 'Tarjeta de Crédito'),
        ('debit_card', 'Tarjeta de Débito'),
        ('paypal', 'PayPal'),
        ('cash', 'Efectivo'),
        ('bank_transfer', 'Transferencia Bancaria'),
    )
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Pago #{self.id} - Orden {self.order.id}"
