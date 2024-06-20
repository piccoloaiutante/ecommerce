from ecommerce.models import Product,Order, OrderItem
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()
    
    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        return OrderItemSerializer(order_items, many=True).data

    class Meta:
        model = Order
        fields = ('id', 'created_at', 'order_items')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"





class CreateOrderItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    class Meta:
        model = OrderItem
        fields= ('id', 'quantity')

class CreateOrderSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField()
    items = serializers.ListField(child=CreateOrderItemSerializer())
    class Meta:
        model = Order
        fields= ('number', 'items')