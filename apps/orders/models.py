from django.db import models
from apps.users.models import CustomUser
from apps.businesses.models import Business
from apps.products.models import Product


class Order(models.Model):
    """Modelo para órdenes."""
    STATUS_CHOICES = (
        ('pending', 'Pendiente'),
        ('confirmed', 'Confirmada'),
        ('preparing', 'Preparando'),
        ('ready', 'Lista para recoger'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    )
    
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)
    
    estimated_time = models.IntegerField(default=20)  # minutos
    pickup_time = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Orden #{self.id} - {self.customer.username}"


class OrderItem(models.Model):
    """Items dentro de una orden."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
