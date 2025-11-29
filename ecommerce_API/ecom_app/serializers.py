from rest_framework import serializers
from .models import Order, User, Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    order_user=OrderSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields="__all__"


class ProductSerializer(serializers.ModelSerializer):
    order_product=OrderSerializer(many=True, read_only=True)
    class Meta:
        model=Product
        fields="__all__"

