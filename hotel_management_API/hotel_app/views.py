from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import User, Role, Booking
from .serializers import UserSerializer, RoleSerializer,BookingSerializer

@api_view(['POST',])
@authentication_classes([])

def login(request):

    if request.method=='POST':

        email=request.data.get('email')
        password=request.data.get('password')

        try:
            user=User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)

        return Response({"access":str(refresh.access_token), "refresh":str(refresh), "status":200}, status=200)
    
@api_view(['POST',])
@authentication_classes([JWTAuthentication])

def bookingCreate(request):
    if request.method=='POST':

        if request.user.role.rolename.lower()!='customer':
            return Response("You dont have permission", status=403)
        
        roomType=request.data.get('roomType')
        nights=request.data.get('nights')
        discount=request.data.get('discount')
        data=request.data.copy()

        if not roomType or not  nights or  not discount:
            return Response("roomType, discount and no of nights are mandatory", status=400)
        
        
        if roomType=='Delux':
            basePrice=4000
        elif roomType=='Suite':
            basePrice=7000

        elif roomType=='Standard':
            basePrice=2500
        else: 
            return Response("we have only Delux, Suite and Standard roomType. Please select accordingly" ,status=400)
        
        try:
            nights=int(nights)
            discount=float(discount)
        except ValueError:
            return Response("no of nights and discount should be in number")
        
        totalPrice=(basePrice*nights)-discount

        data['customerID']=request.user.id
        data['basePrice']=basePrice
        data['totalPrice']=totalPrice

        serializer=BookingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
             return Response(serializer.errors, status=400)
        
    
@api_view(['GET', ])
@authentication_classes([JWTAuthentication])

def bookingList(request):

    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['customer', 'manager']:
            return Response("you dont have permission", status=400)
        
        roomType=request.query_params.get('roomType',None)
        minNights=request.query_params.get('minNights',None)
        maxPrice=request.query_params.get('maxPrice',None)

        bookinglist=Booking.objects.all()

        if roomType:
            bookinglist=bookinglist.filter(roomType=roomType)
        
        if minNights:
            try:
                minNights=int(minNights)
            except ValueError:
                return Response("minNights should be number")
            
            bookinglist=bookinglist.filter(nights__gt=minNights)

        if maxPrice:
            try:
                maxPrice=float(maxPrice)
            except ValueError:
                return Response("MaxPrice should be number")
            
            bookinglist=bookinglist.filter(totalPrice__lt=maxPrice)
        
        serializer=BookingSerializer(bookinglist, many=True)

        return Response(serializer.data, status=200)


@api_view(['PATCH',])
@authentication_classes([JWTAuthentication])

def bookingUpdate(request, pk):

    if request.method=='PATCH':

        if request.user.role.rolename.lower()!='manager':
            return Response("you dont have permission", status=400)
        
        try:
            booking=Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response("not found", status=200)
        
        serializer=BookingSerializer(booking, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
             return Response(serializer.errors, status=400)
        

@api_view(['DELETE',])
@authentication_classes([JWTAuthentication])

def bookingDelete(request, pk):
    if request.method=='DELETE':

        try:
            booking=Booking.objects.get(pk=pk)
        except Booking.DoesNotExist:
            return Response("booking not found", status=400)
        
        if request.user.role.rolename.lower()!='manager' and request.user!=booking.customerID:
            return Response("you dont have permission", status=400)
        
        booking.delete()

        return Response("deleted Successfully", status=204)
            


        








        
        