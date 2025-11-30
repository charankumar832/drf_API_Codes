from rest_framework import serializers
from .models import User, Role, Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Booking
        fields="__all__"
    
class UserSerializer(serializers.ModelSerializer):
    booking_customer=BookingSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    user_rolename=BookingSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"
