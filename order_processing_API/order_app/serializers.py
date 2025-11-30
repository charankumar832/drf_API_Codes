from rest_framework import serializers
from .models import Role, User, Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    order_user=OrderSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields="__all__"


class RoleSerializer(serializers.ModelSerializer):
    user_rolename=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"

