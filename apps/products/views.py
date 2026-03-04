from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from apps.products.models import Product, ProductCategory
from apps.products.serializers import ProductSerializer, ProductCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet para productos."""
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['business', 'category']
    search_fields = ['name', 'description']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para categorías."""
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    permission_classes = [AllowAny]
