from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

import datetime
from .models import User, Role, Book,Borrow
from .serializers import UserSerializer, RoleSerializer, BookSerializer, BorrowSerializer

@api_view(['POST',])

def login(request):
    if request.method=='POST':
        email=request.data.get('email')
        password=request.data.get('password')

        #user=authenticate(email=email, password=password)

        try:
            user=User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return Response("Invalid Credentials", status=400)
        
        # if not user.check_password(password):
        #     return Response("Invalid Credentials",status=400)
        
        refresh=RefreshToken.for_user(user)

        return Response({"email":email,"access":str(refresh.access_token),"refresh":str(refresh), "status":200}, status=200)
    
@api_view(['POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def borrowCreate(request):
    if request.method=='POST':

        if request.user.role.rolename.lower()!='member':
            return Response("You dont have permission", status=403)
        
        bookId=request.data.get('bookId')
        returnDate_str=request.data.get('returnDate')

        if not bookId or not returnDate_str:
            return Response("bookId and returnDate are mandatory feilds", status=400)
        
        borrowDate=datetime.datetime.now().date()
        try:
            returnDate=datetime.datetime.fromisoformat(returnDate_str).date()
        except ValueError:
            return Response("please enter returndate in ISO format YYYY-MM-DD", status=400)
        

        days_diff=(returnDate-borrowDate).days

        if days_diff>14:
            extra_days=days_diff-14
            fine=extra_days*10
        else:
            fine=0

        data=request.data.copy()

        data['fine']=fine
        data['bookId']=bookId
        data['memberId']=request.user.id
        
        serialiazer=BorrowSerializer(data=data)
        if serialiazer.is_valid():
            serialiazer.save()
            return Response(serialiazer.data, status=201)
        return Response(serialiazer.errors, status=400)
    

@api_view(['GET',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def borrowList(request):
    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['member','librarian']:
            return Response("You dont have permission", status=403)

        category=request.query_params.get('category', None)

        borrowlist=Borrow.objects.all()

        if category:
            borrowlist=borrowlist.filter(bookId__category=category)
        
        if not borrowlist.exists():
            return Response("no data available", status=400)
        
        serialiazer=BorrowSerializer(borrowlist, many=True)
        return Response(serialiazer.data, status=200)
    
@api_view(['GET','PATCH', 'PUT','DELETE',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])

def borrowRetrieveUpdateDestroy(request,pk):
    try: 
        borrow=Borrow.objects.get(pk=pk)
    except Borrow.DoesNotExist:
        return Response("borrow not found", status=400)
    
    if request.method=='GET':

        if request.user.role.rolename.lower() not in ['member', 'librarian']:
            return Response("you dont have permission", status=403)
        
        serializer=BorrowSerializer(borrow)
        return Response(serializer.data, status=200)
    
    if request.method in ['PUT', 'PATCH']:

        if request.user.role.rolename.lower() not in ['librarian',]:
            return Response("you dont have permission", status=403)
        
        partial=True if request.method=='PATCH' else False

        # data=request.data.copy()
        # data['bookId']=borrow.bookId.id
        # data['memberId']=request.user.id

        serializer=BorrowSerializer(borrow, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)
        
    if request.method=='DELETE':

        if request.user.role.rolename.lower() not in ['librarian',] and request.user!=borrow.memberId:
            return Response("you dont have permission", status=403)
        
        borrow.delete()
        return Response("deleted Successfully", status=204)

        

