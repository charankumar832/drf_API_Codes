from django.shortcuts import render
from .models import User, Role, Room,Booking
from .serializers import UserSerializer, RoleSerializer, RoomSerializer, BookingSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['POST',])
def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        try:
            # user_obj=User.objects.get(email=email)
            user_obj=User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # user=authenticate(request, user=user_obj.username, password=password)

        # if not user:
        #     return Response("Invalid Credentials", status=400)
        # if not user_obj.check_password(password):
        #     return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user_obj)
        return Response({"email":email,"access":str(refresh.access_token), "refresh":str(refresh), "status":200},status=200)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def bookingCreate(request):
    if request.method=='POST':
        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        roomId=request.data.get('roomId')
        nights=request.data.get('nights')
        discountPct=request.data.get('discountPct')
        taxPct=request.data.get('taxPct')

        if not roomId or not nights:
            return Response("roomId and nights are mandatory", status=400)
        
        try:
            nights=int(nights)
            roomId=int(roomId)
        except ValueError:
            return Response("nights and roomId should be number", status=400)
        
        if discountPct:
            try:
                discountPct=float(discountPct)
            except ValueError:
                return Response("discountPct should be number", status=400)
        else:
            discountPct=0

        if taxPct:
            try:
                taxPct=float(taxPct)
            except ValueError:
                return Response("taxPct should be number", status=400)   
        else:
            taxPct=12
            
        try:
            roomId=Room.objects.get(id=roomId)
        except Room.DoesNotExist:
            return Response("room not found", status=400)
        
        serviceFee=200        
            
        discount=(nights*roomId.baseRate)*(discountPct/100)
        tax=((nights*roomId.baseRate)-discount)*(taxPct/100)
        totalCost=((nights*roomId.baseRate)-discount)+tax+serviceFee
        
        data=request.data.copy()
        data['discountPct']=discountPct
        data['customerId']=request.user.id
        data['taxPct']=taxPct
        data['serviceFee']=serviceFee
        data['totalCost']=totalCost
        
        serializer=BookingSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def bookingList(request):
    if request.method=='GET':
        if request.user.role.rolename.lower() not in ['customer','admin']:
            return Response("you dont have permission", status=403)         

        roomType=request.query_params.get('roomType',None)
        minCost=request.query_params.get('minCost',None)
        maxCost=request.query_params.get('maxCost',None)
        status=request.query_params.get('status',None)

        bookinglist=Booking.objects.all().order_by('totalCost')

        if roomType:
            bookinglist=bookinglist.filter(roomId__roomType=roomType)
        if minCost:
            try:
                minCost=float(minCost)
            except ValueError:
                return Response("minCost should be number", status=400)
            bookinglist=bookinglist.filter(totalCost__gt=minCost)
        if maxCost:
            try:
                maxCost=float(maxCost)
            except ValueError:
                return Response("maxCost should be number", status=400)
            bookinglist=bookinglist.filter(totalCost__lt=maxCost)

        if status:
            bookinglist=bookinglist.filter(status=status)

        serializer=BookingSerializer(bookinglist, many=True)
        return Response(serializer.data, status=200)



@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def bookingRetrieveUpdateDestroy(request,pk):
    try:
        booking=Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response("booking not found", status=400)
    
    if request.method=='GET':
        if request.user.role.rolename.lower()!='admin'and request.user!=booking.customerId:
            return Response("you dont have permission", status=403)   
        serializer=BookingSerializer(booking)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT', 'PATCH']:
        if request.user.role.rolename.lower()!='admin':
            return Response("you dont have permission", status=403) 

        partial=request.method=='PATCH'
        serializer=BookingSerializer(booking,data=request.data,partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':
        if request.user.role.rolename.lower()!='admin'and request.user!=booking.customerId:
            return Response("you dont have permission", status=403) 
        booking.delete()
        return Response("deleted successfully", status=204)

        







