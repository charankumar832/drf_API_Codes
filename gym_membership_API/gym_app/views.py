from django.shortcuts import render
from django.contrib.auth  import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import User, Role, Membership
from .serializers import UserSerializer, RoleSerializer, MembershipSerializer
from datetime import datetime,timedelta


@api_view(['POST',])
def login(request):
    email=request.data.get('email')
    password=request.data.get('password')

    # user=authenticate(request, email=email, password=password)
    # if not user:
    #     return Response("Invalid Credentials", status=400)
    
    try:
        # user=User.objects.get(email=email)
        user=User.objects.get(email=email, password=password)
    except User.DoesNotExist:
        return Response("Invalid Credentials", status=400)
    
    # if not user.check_password(password):
    #     return Response("Invalid Credentials", status=400)
    
    refresh=RefreshToken.for_user(user)
    return Response({"email":email, "access":str(refresh.access_token), "refresh":str(refresh),"status":200}, status=200)

@api_view(['POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def membershipCreate(request):
    if request.user.role.rolename.lower()!='member':
        return Response("You dont have permission", status=403)
    
    planType=request.data.get('planType')
    discountPct=request.data.get('discountPct')

    if not planType:
        return Response('planType is mandatory', status=400)
    
    if planType not in ['Monthly','Quaterly', 'Yearly']:
        return Response('we have only monthly,quaterly, yearly plans', status=400)
    
    if discountPct:
        try:
            discountPct=float(discountPct)
        except ValueError:
            return Response('discountPct should be a number', status=400)
    else:
        discountPct=0
    
    startDate=datetime.now().date()
        
    if planType=='Monthly':
        baseFee=1000
        endDate=startDate+timedelta(days=30)
    
    elif planType=='Quaterly':
        baseFee=2500
        endDate=startDate+timedelta(days=90)
    
    else:
        baseFee=9000
        endDate=startDate+timedelta(days=365)
    
    taxPct=18

    discount=baseFee*(discountPct/100)
    tax=(baseFee-discountPct)*(taxPct/100)
    totalFee=(baseFee-discount)+tax

    data=request.data.copy()
    data['memberId']=request.user.id
    data['baseFee']=baseFee
    data['discountPct']=discountPct
    data['taxPct']=taxPct
    data['totalFee']=totalFee
    data['endDate']=endDate

    serializer=MembershipSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)


@api_view(['GET',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def membershipList(request):
    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['member','admin']:
            return Response("You dont have permission", status=403) 
        
        planType=request.query_params.get('planType',None)
        minFee=request.query_params.get('minFee', None)
        status=request.query_params.get('status',None)

        membershiplist=Membership.objects.all().order_by('-totalFee')

        if planType:
            membershiplist=membershiplist.filter(planType=planType)
        if status:
            membershiplist=membershiplist.filter(status=status)

        if minFee:
            try:
                minFee=float(minFee)
            except ValueError:
                return Response("minfee should be in number", status=400)
            
            membershiplist=membershiplist.filter(totalFee__gt=minFee)
        
        serializer=MembershipSerializer(membershiplist, many=True)
        return Response(serializer.data, status=200)


@api_view(['GET','PUT','PATCH','DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def membershipRetrieveUpdateDestroy(request,pk):

    try:
        membership=Membership.objects.get(pk=pk)
    except Membership.DoesNotExist:
        return Response("not found",status=400)
    
    if request.method=='GET':
        
        if request.user.role.rolename.lower()!='admin' and request.user!=membership.memberId:
            return Response("You dont have permission", status=403) 
        
        serializer=MembershipSerializer(membership)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT','PATCH']:
        
        if request.user.role.rolename.lower()!='admin':
            return Response("You dont have permission", status=403) 
        
        partial=request.method=='PATCH'

        serializer=MembershipSerializer(membership,data=request.data,partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':
        
        if request.user.role.rolename.lower()!='admin' and request.user!=membership.memberId:
            return Response("You dont have permission", status=403) 
        
        membership.delete()
        return Response("deleted successfully", status=204)
        
    



        


  
    

        

    

