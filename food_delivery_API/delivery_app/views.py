from django.shortcuts import render
from .models import Order, User,Role
from .serializers import OrderSerializer, UserSerializer, RoleSerializer

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
            user=User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)
        return Response({"refresh":str(refresh), "access":str(refresh.access_token), "status":200}, status=200)
    

@api_view(['POST',])
@authentication_classes([JWTAuthentication])

def orderCreate(request):

    if request.method=='POST':

        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        baseAmount=request.data.get('baseAmount')
        discountPct=request.data.get('discountPct')
        gstPct=request.data.get('gstPct')
        deliveryFee=request.data.get('deliveryFee')
        

        if baseAmount is None or discountPct is None or gstPct is None or deliveryFee is None:
            return Response("baseAmount, discountPct, gstPct, deliveryFee are mandatory fields", status=400)
        
        try:
            baseAmount=float(baseAmount)
            discountPct=float(discountPct)
            gstPct=float(gstPct)
            deliveryFee=float(deliveryFee)
            

        except ValueError:
            return Response("baseAmount, discountPct, gstPct, deliveryFee are number fields", status=400)
        

        
       
        discount=baseAmount*(discountPct/100)
        gst=(baseAmount-discount)*(gstPct/100)
        finalAmount=((baseAmount)-discount)+gst+deliveryFee

        data=request.data.copy()

        data['finalAmount']=finalAmount
        data['customerID']=request.user.id

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

        if request.user.role.rolename.lower() not in ['customer', 'delivery_agent']:
            return Response("you dont have permission", status=403)
        
        minAmount=request.query_params.get('minAmount',None)
        status=request.query_params.get('status',None)
        maxItems=request.query_params.get('maxItems',None)

        orderlist=Order.objects.all()

        if minAmount:
            try:
                minAmount=float(minAmount)
            except ValueError:
                return Response("minAmount should be in number", status=400)
            
            orderlist=orderlist.filter(finalAmount__gt=minAmount)

        


        if maxItems:
            try:
                maxItems=int(maxItems)
            except ValueError:
                return Response("maxItems should be in number", status=400)
            
            filtered=[]

            for o in orderlist:
                item_count=len(o.items.split(',')) if o.items else 0

                if item_count<=maxItems:
                    filtered.append(o)
            
            orderlist=filtered
        
        if status:
            if status not in['placed','accepted','delivered']:
                return Response("status should be in 'placed','accepted','delivered'", status=400)
            
            orderlist=orderlist.filter(status=status)

        

        serializer=OrderSerializer(orderlist, many=True)
        return Response(serializer.data, status=200)
    

@api_view(['PATCH',])
@authentication_classes([JWTAuthentication])

def orderUpdate(request, pk):

    if request.method=='PATCH':

        if request.user.role.rolename.lower() not in ['delivery_agent',]:
            return Response("you dont have permission", status=403)
        
        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response("order not found", status=400)
        
        serializer=OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['DELETE',])
@authentication_classes([JWTAuthentication])

def orderDelete(request, pk):

    if request.method=='DELETE':

        try:
            order=Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response("order not found", status=400)

        if request.user.role.rolename.lower()!='delivery_agent' and request.user!=order.customerID:
            return Response("you dont have permission", status=403)
        
        order.delete()
        return Response("deleted Successfully", status=204)
        
    
    
        


        
            
        
        



