from django.db import models
from apps.businesses.models import Business


class ProductCategory(models.Model):
    """Categorías de productos."""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Productos del menú."""
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.business.name}"
