from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import CustomUser


class Business(models.Model):
    """
    Modelo para negocios (cafeterías, restaurantes, etc).
    """
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='businesses/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='businesses/banners/', blank=True, null=True)
    
    # Ubicación
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    
    # Información
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Horarios
    opening_time = models.TimeField(default='08:00')
    closing_time = models.TimeField(default='18:00')
    is_open = models.BooleanField(default=True)
    
    # Ratings
    rating = models.FloatField(
        default=5.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.IntegerField(default=0)
    
    # Metadata
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Negocio'
        verbose_name_plural = 'Negocios'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class BusinessCategory(models.Model):
    """
    Categorías de negocios.
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.ImageField(upload_to='categories/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Categoría de Negocio'
        verbose_name_plural = 'Categorías de Negocios'
    
    def __str__(self):
        return self.name


class BusinessReview(models.Model):
    """
    Reseñas de negocios.
    """
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Reseña'
        verbose_name_plural = 'Reseñas'
        unique_together = ['business', 'customer']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reseña de {self.customer.username} para {self.business.name}"
