from .models import User, Reservation, Role, Movie
from rest_framework import serializers

class ReservationSerializer(serializers.ModelSerializer):
    # reservation_user=serializers.StringRelatedField(read_only=False,queryset=User.objects.all())
    # reservation_movie=serializers.StringRelatedField(read_only=False,queryset=Movie.objects.all())
    # reservation=serializers.StringRelatedField(source='reservation_user',read_only=True)
    # reservation=serializers.StringRelatedField(source='reservation_movie',read_only=True)
    class Meta:
        model=Reservation
        fields="__all__"

class MovieSerializer(serializers.ModelSerializer):
    # reservation_movie=ReservationSerializer(many=True, read_only=True)
    class Meta:
        model=Movie
        fields="__all__"

class UserSerializer(serializers.ModelSerializer):
    # reservation_user=ReservationSerializer(many=True, read_only=True)
    # user_role=serializers.StringRelatedField(read_only=False,queryset=Role.objects.all())
    # user=serializers.StringRelatedField(source='user_role',read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    # user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"
