from django.urls import path
from ecommerce_api.views import ProductAPIView, OrderAPIView

urlpatterns = [
    path("product/",
         ProductAPIView.as_view(),
         name="product-list"),
    path("order/",
         OrderAPIView.as_view(),
         name="order-list"),]