from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import models
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from apps.businesses.models import Business, BusinessCategory, BusinessReview
from apps.businesses.serializers import (
    BusinessListSerializer, BusinessDetailSerializer,
    BusinessCreateUpdateSerializer, BusinessCategorySerializer,
    BusinessReviewSerializer
)


class BusinessViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar negocios.
    """
    queryset = Business.objects.filter(is_active=True)
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'is_open']
    search_fields = ['name', 'description', 'city']
    ordering_fields = ['rating', 'created_at', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BusinessDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BusinessCreateUpdateSerializer
        return BusinessListSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo negocio."""
        if hasattr(request.user, 'business'):
            return Response(
                {'detail': 'El usuario ya tiene un negocio registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        business = serializer.save(owner=request.user)
        
        return Response(
            BusinessDetailSerializer(business).data,
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Actualizar negocio (solo el propietario)."""
        business = self.get_object()
        if business.owner != request.user:
            return Response(
                {'detail': 'No tienes permiso para editar este negocio'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, pk=None):
        """Agregar una reseña al negocio."""
        business = self.get_object()
        
        # Verificar si el usuario ya hizo una reseña
        if BusinessReview.objects.filter(business=business, customer=request.user).exists():
            return Response(
                {'detail': 'Ya has reseñado este negocio'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = BusinessReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = serializer.save(business=business, customer=request.user)
        
        # Actualizar rating del negocio
        avg_rating = business.reviews.aggregate(
            avg=models.Avg('rating')
        )['avg'] or 5.0
        business.rating = avg_rating
        business.total_reviews = business.reviews.count()
        business.save()
        
        return Response(
            BusinessReviewSerializer(review).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def my_business(self, request):
        """Obtener el negocio del usuario autenticado."""
        try:
            business = Business.objects.get(owner=request.user)
            serializer = BusinessDetailSerializer(business)
            return Response(serializer.data)
        except Business.DoesNotExist:
            return Response(
                {'detail': 'No tienes un negocio registrado'},
                status=status.HTTP_404_NOT_FOUND
            )


class BusinessCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para categorías de negocios.
    """
    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer
    permission_classes = [AllowAny]
    pagination_class = None
