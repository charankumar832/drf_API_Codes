from rest_framework import serializers
from .models import User, Role, Ticket

class TicketSerializer(serializers.ModelSerializer):
    # customerId=serializers.StringRelatedField(read_only=False, queryset=User.objects.all())
    customer=serializers.StringRelatedField(source='customerId', read_only=True)
    class Meta:
        model=Ticket
        exclude=['customerId',]

class UserSerializer(serializers.ModelSerializer):
    # ticket_user=TicketSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields="__all__"

class RoleSerializer(serializers.ModelSerializer):
    # user_role=UserSerializer(many=True, read_only=True)
    # role=serializers.StringRelatedField(read_only=False, queryset=Role.objects.all())
    # role=serializers.StringRelatedField(source='role', read_only=True)
    class Meta:
        model=Role
        fields="__all__"