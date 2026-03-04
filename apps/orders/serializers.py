from rest_framework import serializers
from apps.orders.models import Order, OrderItem
from apps.products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']


class OrderListSerializer(serializers.ModelSerializer):
    business_name = serializers.CharField(source='business.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'business_name', 'status', 'total_price',
            'estimated_time', 'created_at'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    business_name = serializers.CharField(source='business.name', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'business', 'business_name', 'status',
            'total_price', 'notes', 'estimated_time', 'pickup_time',
            'created_at', 'updated_at', 'completed_at', 'items'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'completed_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = ['business', 'notes', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        total_price = 0
        for item_data in items_data:
            item = OrderItem.objects.create(order=order, **item_data)
            total_price += item.price * item.quantity
        
        order.total_price = total_price
        order.save()
        
        return order
