from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ecommerce.models import Product, Order
from ecommerce_api.serializers import ProductSerializer, OrderSerializer, CreateOrderSerializer

class ProductAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class OrderAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            order = Order.objects.create()
            enugh_quantity = True
            for item in serializer.validated_data['items']:
                product = get_object_or_404(Product, pk=item['id'])
                if(product.quantity_in_stocks < item['quantity']):
                    enugh_quantity = False
                    break
                order.orderitem_set.create(product=product, quantity=item['quantity'])
            if(enugh_quantity):
                order.save()
                for product in order.orderitem_set.all():
                    product.product.quantity_in_stocks -= product.quantity
                    product.product.save()
            else:
                order.delete()
                return Response({"message": "Not enough quantity in stock"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        orders = Order.objects.filter()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    
    