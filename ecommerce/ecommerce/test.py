from django.test import TestCase, Client
from rest_framework import status
from ecommerce.models import Product, Order
from ecommerce.api.serializers import ProductSerializer, OrderSerializer

class ProductViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(name='Product 1', price=10, quantity_in_stocks=10)
        self.product2 = Product.objects.create(name='Product 2', price=20, quantity_in_stocks=20)

    def test_get_products(self):
        response = self.client.get('/api/product/')
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.order1 = Order.objects.create()
        self.product1 = Product.objects.create(name='Product 1', price=10, quantity_in_stocks=10)
        self.order1.orderitem_set.create(product=self.product1, quantity=1)

    def test_get_orders(self):
        response = self.client.get('/api/order/')
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_order(self):    
        response = self.client.post('/api/order/', {"number": 1, "items": [{"id": self.product1.id, "quantity": 1}]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Product.objects.get(id=self.product1.id).quantity_in_stocks, 9)
    
    def test_create_order_has_not_enough_quantity(self):
        response = self.client.post('/api/order/', {"number": 1, "items": [{"id": self.product1.id, "quantity": 11}]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Product.objects.get(id=self.product1.id).quantity_in_stocks, 10)
    
    def test_create_order_with_invalid_product(self):
        response = self.client.post('/api/order/', {"number": 1, "items": [{"id": 100, "quantity": 1}]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Product.objects.get(id=self.product1.id).quantity_in_stocks, 10)
    
    def test_create_order_with_invalid_data(self):
        response = self.client.post('/api/order/', {"number": 1, "items": [{"id": self.product1.id, "quantity": "a"}]}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Product.objects.get(id=self.product1.id).quantity_in_stocks, 10)