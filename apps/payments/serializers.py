from rest_framework import serializers
from apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'order', 'amount', 'status', 'method',
            'transaction_id', 'reference', 'created_at', 'completed_at'
        ]
        read_only_fields = ['id', 'created_at', 'completed_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'method']
    
    def create(self, validated_data):
        order = validated_data['order']
        validated_data['amount'] = order.total_price
        return super().create(validated_data)
