from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth import authenticate
from .models import Role,User, Cart, Product
from .serializers import RoleSerializer, UserSerializer, CartSerializer, ProductSerializer

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])

def login(request):

    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        # user=authenticate(request, email=email, password=password)

        # if not user:
        #     return Response("Invalid Credentials", status=400)
        
        try: 
            user=User.objects.get(email=email, password=password)
            # user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # if not user.check_password(password):
        #     return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)
        return Response({"email":email,"access":str(refresh.access_token), "refresh":str(refresh), "status":200}, status=200)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def cartAdd(request):

    if request.method=='POST':

        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        quantity=request.data.get('quantity')
        discountPct=request.data.get('discountPct')
        productId=request.data.get('productId')
        taxPct=request.data.get('taxPct')

        if not quantity or not productId:
            return Response("these are mandatory", status=400)
        
        if taxPct:
            try:
                taxPct=float(taxPct)
            except ValueError:
                return Response("these should be number", status=400)
        else:
            taxPct=12

        try:
            productId=int(productId)
            quantity=int(quantity)
            
        except ValueError:
            return Response("these should be number", status=400)
            
        try:
            product=Product.objects.get(id=productId)
        except Product.DoesNotExist:
            return Response("Not found", status=400)
        
        if discountPct:
            try:
                discountPct=float(discountPct)
            except ValueError:
                return Response("these should be number", status=400)
        else:
            discountPct=0

        
        price=product.price

        discount=(quantity*price)*(discountPct/100)
        tax=((quantity*price)-discount)*(taxPct/100)
        totalPrice=((quantity*price)-discount)+tax

        data=request.data.copy()
        data['customerId']=request.user.id
        data['productId']=productId
        data['taxPct']=taxPct
        data['totalPrice']=totalPrice

        serializer=CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        else:
            return Response(serializer.errors,status=400)
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def cartList(request):

    if request.method=='GET':
        if request.user.role.rolename.lower() not in['customer','admin']:
            return Response("you dont have permission", status=403)
        
        category=request.query_params.get('category', None)
        minPrice=request.query_params.get('minPrice', None)
        maxPrice=request.query_params.get('maxPrice', None)
        status=request.query_params.get('status', None)

        cartlist=Cart.objects.all().order_by('totalPrice')


        if category:
            cartlist=cartlist.filter(productId__category=category)
        
        if minPrice:
            try:
                minPrice=float(minPrice)
            except ValueError:
                return Response("minPrice should be a number", status=400)
            
            cartlist=cartlist.filter(totalPrice__gt=minPrice)
            
        if maxPrice:
            try:
                maxPrice=float(maxPrice)
            except ValueError:
                return Response("maxPrice should be a number", status=400)
            cartlist=cartlist.filter(totalPrice__lt=maxPrice)

        if status:
            cartlist=cartlist.filter(status=status)

        serializer=CartSerializer(cartlist, many=True)
        return Response(serializer.data, status=200)

            
@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def cartRetrieveUpdateDestroy(request,pk):

    try:
        cartitem=Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response("not found", status=400)

    if request.method=='GET':
        if request.user.role.rolename.lower()!='admin' and request.user!=cartitem.customerId:
            return Response("you dont have permission", status=403)
        
        serializer=CartSerializer(cartitem)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT', 'PATCH']:
        if request.user.role.rolename.lower()!='admin':
            return Response("you dont have permission", status=403)
        
        partial=request.method=='PATCH'

        serializer=CartSerializer(cartitem, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        else:
            return Response(serializer.errors,status=400)
    

    if request.method=='DELETE':
        if request.user.role.rolename.lower()!='admin' and request.user!=cartitem.customerId:
            return Response("you dont have permission", status=403)
        
        cartitem.delete()
        return Response("deleted successfully", status=204)

        
        



