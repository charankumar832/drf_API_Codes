from django.shortcuts import render
from .models import User, Role, Order
from .serializers import UserSerializer, RoleSerializer, OrderSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes


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
        return Response({"access":str(refresh.access_token),"refresh":str(refresh), "status":200}, status=200)
    

@api_view(['POST',])
@authentication_classes([JWTAuthentication])

def orderCreate(request):
    if request.method=='POST':

        if request.user.role.rolename.lower()!='customer':
            return Response("You dont have permission", status=403)
        
        data=request.data.copy()
        
        quantity=request.data.get('quantity')
        unitPrice=request.data.get('unitPrice')
        discountPct=request.data.get('discountPct')
        taxPct=request.data.get('taxPct')

        if quantity is None or unitPrice is None or discountPct is None or taxPct is None:
            return Response("quantity, unitPrice, discountPct, taxPct are mandatory", status=400)
        
        try:
            quantity=int(quantity)
            unitPrice=float(unitPrice)
            discountPct=float(discountPct)
            taxPct=float(taxPct)
        except ValueError:
            return Response("quantity, unitPrice, discountPct, taxPct should be in number", status=400)
        
        discount=(quantity*unitPrice)*(discountPct/100)
        tax=((quantity*unitPrice)-discount)*(taxPct/100)
        totalPrice=(quantity*unitPrice)-discount+tax

        data['customerID']=request.user.id
        data['totalPrice']=totalPrice
        data['tax']=tax

        serializer=OrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

@api_view(['GET',])
@authentication_classes([JWTAuthentication])

def orderList(request):
    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['admin', 'customer']:
            return Response("You dont have permission", status=403)
        
        minTotal=request.query_params.get('minTotal', None)
        maxTotal=request.query_params.get('maxTotal', None)
        status=request.query_params.get('status', None)

        orderlist=Order.objects.all()

        if minTotal:
            try:
                minTotal=float(minTotal)
            except ValueError:
                return Response("minTotal should be in number", status=400)
            
            orderlist=orderlist.filter(totalPrice__gt=minTotal)
        
        if maxTotal:
            try:
                maxTotal=float(maxTotal)
            except ValueError:
                return Response("maxTotal should be in number", status=400)
            
            orderlist=orderlist.filter(totalPrice__lt=maxTotal)


        if status:

            if status not in ['pending', 'shipped', 'confirmed']:
                return Response("we have pending, shipped and confirmed as status. please select accrodingly", status=400)
            
        serializer=OrderSerializer(orderlist, many=True)
        return Response(serializer.data,status=200)
    
      
   

@api_view(['PATCH',])
@authentication_classes([JWTAuthentication])

def orderUpdate(request,pk):
    if request.method=='PATCH':

        if request.user.role.rolename.lower()!='admin':
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

def orderDelete(request,pk):
    if request.method=='DELETE':
                
        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response("order not found", status=400)
        
        if request.user.role.rolename.lower()!='admin' and request.user!=order.customerID:
            return Response("You dont have permission", status=403)
        
        order.delete()
        return Response("deleted successfully", status=204)









