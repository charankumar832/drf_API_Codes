from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .models import User, Role, Shipment
from .serializers import UserSerializer, RoleSerializer, ShipmentSerializer
from django.contrib.auth import authenticate


@api_view(['POST',])
@authentication_classes([])
@permission_classes([])

def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        # user=authenticate(request,email=email, password=password)
        # if user is None:
        #     return Response("Invalid Credentials", status=400)

        try:
            # user=User.objects.get(email=email)
            user=User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # if not user.check_password(password):
        #     return Response("Invalid Credentials", status=400)

        refresh=RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token),"username": user.username})
    

@api_view(['POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def shipmentAdd(request):
    if request.method=='POST':
        if request.user.roleobj.role.lower()!='admin':
            return Response("you dont have permission", status=403)
        
        data=request.data.copy()
        
        serializer=ShipmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(senderobj=request.user)
            return Response(serializer.data, status=201)
        else: 
            return Response(serializer.errors, status=400)


@api_view(['GET','PUT','PATCH',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def shipmentRetrieveUpdateDestroy(request,pk):

    try:
        shipment=Shipment.objects.get(pk=pk)
    except Shipment.DoesNotExist:
        return Response("shipment not found", status=400)
    
    if request.method=='GET':
        if request.user.roleobj.role.lower() != 'admin' and request.user!=shipment.senderobj:
            return Response("you dont have permission", status=403)
        serializer=ShipmentSerializer(shipment)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT','PATCH']:
        if request.user!=shipment.senderobj:
            return Response("you dont have permission", status=403)
        partial=request.method=='PATCH'

        serializer=ShipmentSerializer(shipment, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':
        if request.user!=shipment.senderobj:
            return Response("Unauthorized to delete this shipment", status=403)
        shipment.delete()
        return Response("shipment deleted successfully", status=204)


@api_view(['GET',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def shipmentList(request):
    if request.method=='GET': 
        tracking_number=request.query_params.get('tracking_number',None)

        shipmentlist = Shipment.objects.all()

        if request.user.roleobj.role.lower() == 'customer':
            shipmentlist = shipmentlist.filter(senderobj=request.user)
        
        if tracking_number:
            
            shipmentlist=shipmentlist.filter(tracking_number=tracking_number)
        
        serializer=ShipmentSerializer(shipmentlist, many=True)
        return Response(serializer.data, status=200)

 
