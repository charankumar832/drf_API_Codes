from django.shortcuts import render
from .models import User, Reservation, Role, Movie
from .serializers import UserSerializer, ReservationSerializer, RoleSerializer, MovieSerializer

from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['POST'])
def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        if not email or not password:
            return Response("email and password are mandatory", status=400)
        
        try:
            # user=User.objects.get(email=email)
            user=User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # user=authenticate(request,username=user.username, password=password)

        # if not user:
        #     return Response("Invalid Credentials", status=400)
        # if not user.check_password(password):
        #     return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)
        # token,created=Token.get_or_create(user=user)
        # return Response({"email":email, "token":token.key,"status":200}, status=200)
        return Response({"email":email, "access":str(refresh.access_token),"refresh":str(refresh), "status":200}, status=200)
        
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reservationCreate(request):
    if request.method=='POST':

        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        movieId=request.data.get('movieId')
        quantity=request.data.get('quantity')
        discountPct=request.data.get('discountPct')

        if not movieId or not quantity:
            return Response("movieId and quantity are mandatory", status=400)
        
        try:
            movie=Movie.objects.get(id=movieId)
        except Movie.DoesNotExist:
            return Response("not found", status=400)
        
        try:
            quantity=int(quantity)

        except ValueError:
            return Response("quantity should be a number", status=400)
        
        if discountPct:
            try:
                discountPct=float(discountPct)
            except ValueError:
                return Response("discountPct should be a number", status=400)
            
        else:
            discountPct=0
        
        gstPct=18
        serviceFee=50

        basePrice=movie.basePrice
        discount=(quantity*basePrice)*(discountPct/100)
        gst=((quantity*basePrice)-discount)*(gstPct/100)
        totalAmount=((quantity*basePrice)-discount)+gst+serviceFee

        data=request.data.copy()
        data['customerId']=request.user.id
        data['discountPct']=discountPct
        data['gstPct']=gstPct
        data['serviceFee']=serviceFee
        data['totalAmount']=totalAmount

        serializer=ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reservationList(request):
    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['customer','admin']:
            return Response("you dont have permission", status=403)
        
        category=request.query_params.get('category',None)
        minAmount=request.query_params.get('minAmount',None)
        maxAmount=request.query_params.get('maxAmount',None)
        status=request.query_params.get('status',None)

        reservationlist=Reservation.objects.all().order_by('-totalAmount')

        if category:
            reservationlist=reservationlist.filter(movieId__category=category)
        if status:
            reservationlist=reservationlist.filter(status=status)
        if minAmount:
            try:
                minAmount=float(minAmount)
            except ValueError:
                return Response("minAmount should be a number", status=400)
            
            reservationlist=reservationlist.filter(totalAmount__gt=minAmount)
        
        if maxAmount:
            try:
                maxAmount=float(maxAmount)
            except ValueError:
                return Response("maxAmount should be a number", status=400)
            
            reservationlist=reservationlist.filter(totalAmount__lt=maxAmount)

        serializer=ReservationSerializer(reservationlist, many=True)
        return Response(serializer.data, status=200)
    
@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reservationRetrieveUpdateDestroy(request,pk):
    try:
        reservation=Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return Response("reservation not found", status=400)

    if request.method=='GET':

        if request.user.role.rolename.lower()!='admin' and request.user!=reservation.customerId:
            return Response("you dont have permission", status=403)
        serializer=ReservationSerializer(reservation)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT', 'PATCH']:

        if request.user.role.rolename.lower()!='admin':
            return Response("you dont have permission", status=403)
        partial=request.method=='PATCH'

        serializer=ReservationSerializer(reservation, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':

        if request.user.role.rolename.lower()!='admin' and request.user!=reservation.customerId:
            return Response("you dont have permission", status=403)
        
        reservation.delete()
        return Response("deleted successfully", status=204)


 
        


        







