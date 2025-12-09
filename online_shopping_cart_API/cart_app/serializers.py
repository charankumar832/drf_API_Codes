from rest_framework import serializers
from .models import Role, User, Product, Cart

class CartSerializer(serializers.ModelSerializer):
    # cart=serializers.StringRelatedField(source='cart_user', read_only=True)
    # product=serializers.StringRelatedField(source='product_cart', read_only=True)
    class Meta:
        model=Cart
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    # product_cart=CartSerializer(many=True, read_only=True)
    class Meta:
        model=Product
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    # cart_user=CartSerializer(many=True, read_only=True)
    # user=serializers.StringRelatedField(source='user_role', read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    # user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"