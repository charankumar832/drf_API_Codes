from rest_framework import serializers
from .models import User, Role, Shipment


class ShipmentSerializer(serializers.ModelSerializer):
    #senderobj=serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())
    sender=serializers.StringRelatedField(source='senderobj', read_only=True)

    class Meta:
        model=Shipment
        exclude=['senderobj']

class UserSerializer(serializers.ModelSerializer):
    #shipment_user=ShipmentSerializer(many=True, read_only=True)
    #roleobj=serializers.PrimaryKeyRelatedField(read_only=False, queryset=Role.objects.all())
    role=serializers.StringRelatedField(source='roleobj', read_only=True)
    class Meta:
        model=User
        exclude=['roleobj']

class RoleSerializer(serializers.ModelSerializer):
    #user_role=UserSerializer(many=True, read_only=True)
    class Meta:
        model=Role
        fields="__all__"




