from rest_framework import serializers
from .models import Room,Role, User, Booking


class BookingSerializer(serializers.ModelSerializer):
    # booking_user=serializers.StringRelatedField(read_only=False, queryset=User.objects.all())
    # booking_room=serializers.StringRelatedField(read_only=False, queryset=Room.objects.all())
    # user=serializers.StringRelatedField(source='booking_user', read_only=True)
    # room=serializers.StringRelatedField(source='booking_room', read_only=True)
    class Meta:
        model=Booking
        fields="__all__"

class RoomSerializer(serializers.ModelSerializer):
    # booking_room=BookingSerializer(many=True, read_only=True)
    
    class Meta:
        model=Room
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    # booking_user=BookingSerializer(many=True, read_only=True)
    # user_role=serializers.StringRelatedField(read_only=False, queryset=User.objects.all())
    # user=serializers.StringRelatedField(source='user_role', read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    # user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"
       