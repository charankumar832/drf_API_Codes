from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Order, Product, User
from .serializers import OrderSerializer, ProductSerializer, UserSerializer

@api_view(['POST',])
@authentication_classes([])

def login(request):

    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        try:
            user=User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)

        return Response({"access":str(refresh.access_token), "refresh":str(refresh), "status":200}, status=200)

@api_view(['POST',])
@authentication_classes([JWTAuthentication])

def productsAdd(request):
    if request.method=='POST':

        if request.user.role.lower()!='admin':
            return Response("you dont have permission", status=403)
        
        serializer=ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['GET',])
@authentication_classes([JWTAuthentication])

def productList(request):

    if request.method=='GET':

        user=request.user.role.lower()

        if user not in ['admin', 'customer']:
            return Response("you dont have permission", status=400)
        
        category=request.query_params.get('category', None)
        minPrice=request.query_params.get('minPrice', None)

        productlist=Product.objects.all()

        if category:
            productlist=productlist.filter(category=category)

        if minPrice:
            try:
                minPrice=float(minPrice)
            except ValueError:
                return Response("minPrice should be a number")
            productlist=productlist.filter(price__gt=minPrice)

        serializer=ProductSerializer(productlist, many=True)
        
        return Response (serializer.data, status=200)
    
@api_view(['POST',])
@authentication_classes([JWTAuthentication])

def orderCreate(request):
    if request.method=='POST':

        if request.user.role.lower()!='customer':
            return Response("you dont have permission", status=400)
        
        productID=request.data.get('productID')
        quantity=request.data.get('quantity')
        data=request.data.copy()

        if quantity:
            try:
                quantity=int(quantity)
            except ValueError:
                return Response("quantity should be a integer", status=400)
        
        try:
            product=Product.objects.get(id=productID)
        except Product.DoesNotExist:
            return Response("Product not found", status=400)
        
        totalPrice=quantity*product.price

        data['totalPrice']=totalPrice
        data['customerID']=request.user.id

        serializer=OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['PATCH',])
@authentication_classes([JWTAuthentication])

def orderUpdate(request, pk):

    if request.method=='PATCH':
        
        if request.user.role.lower()!='admin':
            return Response("You dont have permission", status=403)
        
        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response("order not found", status=400)
        
        serializer=OrderSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

@api_view(['DELETE',])
@authentication_classes([JWTAuthentication])

def orderDelete(request, pk):

    if request.method=='DELETE':

        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response("order not found")
        
        if request.user.role.lower()!='admin' and request.user!=order.customerID:
            return Response("you dont have permission", status=403)
        
        order.delete()
        return Response("deleted successfully", status=204)


