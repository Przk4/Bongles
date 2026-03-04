from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.orders.models import Order
from apps.orders.serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet para órdenes."""
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderDetailSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderListSerializer
    
    def get_queryset(self):
        # Clientes ven sus órdenes, negocios ven sus órdenes
        user = self.request.user
        if hasattr(user, 'business'):
            return Order.objects.filter(business=user.business)
        return Order.objects.filter(customer=user)
    
    def create(self, request, *args, **kwargs):
        """Crear nueva orden."""
        data = request.data
        data['customer'] = request.user.id
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(customer=request.user)
        
        return Response(
            OrderDetailSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_status(self, request, pk=None):
        """Cambiar el estado de la orden."""
        order = self.get_object()
        
        # Solo el negocio puede cambiar el estado
        if not hasattr(request.user, 'business') or request.user.business != order.business:
            return Response(
                {'detail': 'No tienes permiso para cambiar este estado'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'detail': 'Estado inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        return Response(OrderDetailSerializer(order).data)
