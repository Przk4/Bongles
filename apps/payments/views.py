from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime

from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer, PaymentCreateSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet para pagos."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo pago."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()
        
        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def process(self, request, pk=None):
        """Procesar/confirmar un pago."""
        payment = self.get_object()
        
        if payment.status != 'pending':
            return Response(
                {'detail': 'El pago ya ha sido procesado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'completed'
        payment.completed_at = datetime.now()
        payment.transaction_id = f"TXN-{payment.id}-{datetime.now().timestamp()}"
        payment.save()
        
        # Actualizar estado de la orden
        order = payment.order
        order.status = 'confirmed'
        order.save()
        
        return Response(PaymentSerializer(payment).data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def refund(self, request, pk=None):
        """Reembolsar un pago."""
        payment = self.get_object()
        
        if payment.status != 'completed':
            return Response(
                {'detail': 'Solo se pueden reembolsar pagos completados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'refunded'
        payment.save()
        
        # Actualizar estado de la orden
        order = payment.order
        order.status = 'cancelled'
        order.save()
        
        return Response(PaymentSerializer(payment).data)
