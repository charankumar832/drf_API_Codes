from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import User, Role, Ticket
from .serializers import UserSerializer, RoleSerializer, TicketSerializer

@api_view(['POST',])
@authentication_classes([])
@permission_classes([])

def login(request):
    if request.method=='POST':

        email=request.data.get('email')
        password=request.data.get('password')

        # user=authenticate(email=email, password=password)

        # if not user:
        #     return Response("Invalid Credentials", status=400)
        
        try:
            # user=User.objects.get(email=email)
            user=User.objects.get(email=email, password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # if not user.check_password(user):
        #     return Response("Invalid Credentials", status=400)
        
        refresh=RefreshToken.for_user(user)
        return Response({"email":email, "access":str(refresh.access_token), "refresh":str(refresh), "status":200},status=200)
    

@api_view(['POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def ticketsCreate(request):
    if request.method=='POST':
        if request.user.role.rolename.lower()!='customer':
            return Response("you dont have permission", status=403)
        
        category=request.data.get('category')
        quantity=request.data.get('quantity')
        discountPct=request.data.get('discountPct')
        gstPct=request.data.get('gstPct')
        serviceFee=request.data.get('serviceFee')


        if serviceFee is None:
            serviceFee=100
        if gstPct is None:
            gstPct=12

        if not category or not quantity or not discountPct:
            return Response("category, quantity and discountPct are mandatory fields", status=400)
        
        if category not in['VIP', 'Regular','Student']:
            return Response("we have only VIP, Regular, Student category", status=400)
        
        if category =='VIP':
            basePrice=5000
        elif category=='Regular':
            basePrice=2500
        else:
            basePrice=1000

        try:
            quantity=int(quantity)
            discountPct=float(discountPct)
            gstPct=float(gstPct)
            serviceFee=float(serviceFee)
        except ValueError:
            return Response("quantity ,serviceFee , gstPct and discountPct should be number", status=400)
        
        discount=(quantity*basePrice)*(discountPct/100)
        gst=((quantity*basePrice)-discount)*(gstPct/100)
        totalAmount=(quantity*basePrice)-discount+gst+serviceFee

        data=request.data.copy()
        # data['customerId']=request.user.id
        data['basePrice']=basePrice
        data['totalAmount']=totalAmount

        serializer=TicketSerializer(data=data)
        if serializer.is_valid():
            serializer.save(customerId=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['GET',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def ticketsList(request):
    if request.method=='GET':
        if request.user.role.rolename.lower() not in ['customer','admin']:
            return Response("you dont have permission", status=403)
        
        category=request.query_params.get('category', None)
        minAmount=request.query_params.get('minAmount', None)
        maxAmount=request.query_params.get('maxAmount', None)
        status=request.query_params.get('status', None)

        ticketlist=Ticket.objects.all().order_by('-totalAmount')

        if category:
            ticketlist=ticketlist.filter(category=category)
        if minAmount:
            try:
                minAmount=float(minAmount)
            except ValueError:
                return Response("minAmount should be a number")
            ticketlist=ticketlist.filter(totalAmount__gt=minAmount)
        

        if maxAmount:
            try:
                maxAmount=float(maxAmount)
            except ValueError:
                return Response("minAmount should be a number")
            ticketlist=ticketlist.filter(totalAmount__lt=maxAmount)

        if status:
            ticketlist=ticketlist.filter(status=status)

        serializer=TicketSerializer(ticketlist, many=True)
        return Response(serializer.data, status=200)
    

        
@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def ticketsRetrieveUpdateDestroy(request,pk):

    try:
        ticket=Ticket.objects.get(pk=pk)
    except Ticket.DoesNotExist:
        return Response("ticket not found",status=400)
    
    if request.method=='GET':
        if request.user.role.rolename.lower()!='admin' and request.user!=ticket.customerId:
            return Response("you dont have permission", status=403)  

        serializer=TicketSerializer(ticket)
        return Response(serializer.data, status=200)
    
    
    if request.method in ['PUT', 'PATCH']:
        if request.user.role.rolename.lower() !='admin':
            return Response("you dont have permission", status=403) 
        
        partial=request.method=='PATCH'

        serializer=TicketSerializer(ticket,data=request.data,partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':
        if request.user.role.rolename.lower() !='admin' and request.user!=ticket.customerId:
            return Response("you dont have permission", status=403) 
        
        ticket.delete()
        return Response("deleted successfully", status=204)
    
        





