from django.shortcuts import render
from .models import Role, User, Rental
from .serializers import RoleSerializer, UserSerializer, RentalSerializer
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST',])
@authentication_classes([])
@permission_classes([])

def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        # user=authenticate(request, email=email, password=password)

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
        return Response({"email":email,"access":str(refresh.access_token),"refresh":str(refresh), "status":200}, status=200)

@api_view(['POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def rentalCreate(request):
    if request.method=='POST':  
        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        carType=request.data.get('carType')
        days=request.data.get('days')
        discountPct=request.data.get('discountPct')

        if not carType or not days or not discountPct:
            return Response("carType, days, discountPct are mandatory fields", status=400)
        
        if carType not in ['SUV','Sedan','Hatchback']:
            return Response("'SUV','Sedan','Hatchback' we only have these options. select appropiatley", status=400)
        
        if carType=='SUV':
            baseRate=3000
        elif carType=='Sedan':
            baseRate=2000
        else:
            baseRate=1500

        try:
            days=int(days)
            discountPct=float(discountPct)
        except ValueError:
            return Response("days and discount should be in numbers", status=400)
        
        insuranceFee=500#default
        discount=(days*baseRate)*(discountPct/100)
        totalCost=(days*baseRate)-discount+insuranceFee

        data=request.data.copy()
        data['customerId']=request.user.id
        data['baseRate']=baseRate
        data['totalCost']=totalCost

        serializer=RentalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@api_view(['GET',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def rentalList(request):
    if request.method=='GET':  
        if request.user.role.rolename.lower() not in ['customer','manager']:
            return Response("you dont have permission", status=403)
        
        carType=request.query_params.get('carType',None)
        minDays=request.query_params.get('minDays',None)
        maxCost=request.query_params.get('maxCost',None)
        status=request.query_params.get('status',None)

        carlist=Rental.objects.all()

        if carType:
            carlist=carlist.filter(carType=carType)
        if minDays:
            try:
                minDays=int(minDays)
            except ValueError:
                return Response("minDays should be a number", status=400)
            carlist=carlist.filter(days__gt=minDays)
        if maxCost:
            try:
                maxCost=int(maxCost)
            except ValueError:
                return Response("maxCost should be a number", status=400)
            carlist=carlist.filter(totalCost__lt=maxCost)
        if status:
            carlist=carlist.filter(status=status)

        serializer=RentalSerializer(carlist,many=True)
        return Response(serializer.data, status=200)
    

@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def rentalRetrieveUpdateDestroy(request,pk):

    try:
        rental=Rental.objects.get(pk=pk)
    except Rental.DoesNotExist:
        return Response("rental not found",status=400)
    
    if request.method=='GET':  
        
        if request.user.role.rolename.lower() not in ['customer','manager']:
            return Response("you dont have permission", status=403)
        
        
        serializer=RentalSerializer(rental)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT', 'PATCH']:  
        if request.user.role.rolename.lower()!='manager':
            return Response("you dont have permission", status=403)
        
        partial=request.method=='PATCH'

        serializer=RentalSerializer(rental, data=request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        

    if request.method=='DELETE':  
        if request.user.role.rolename.lower()!='manager' and request.user!=rental.customerId:
            return Response("you dont have permission", status=403)
        
        rental.delete()
        return Response("deleted successfully", status=204)
    
        
        
        







