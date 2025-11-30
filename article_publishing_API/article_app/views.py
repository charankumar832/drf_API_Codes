from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .models import Role, User, Article
from .serializers import RoleSerializer, UserSerializer, ArticleSerializer

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

def articleAdd(request):
    if request.method=='POST':

        if request.user.role.rolename.lower()!='author':
            return Response("You dont have permission", status=403)
        
        data=request.data.copy()
        content=request.data.get('content')

        wordCount=len(content.split())
        
        data['authorID']=request.user.id
        data['wordCount']=wordCount

        serializer=ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        
@api_view(['GET',])
@authentication_classes([JWTAuthentication])

def articleList(request):
    if request.method=='GET':

        user=request.user.role.rolename.lower()

        if user not in['author', 'editor']:
            return Response("you dont have permission", status=403)
        
        category=request.query_params.get('category', None)
        minWords=request.query_params.get('minWords',None)

        articlelist=Article.objects.all()

        if category:
            articlelist=articlelist.filter(category=category)
        
        if minWords:
            try:
                minWords=int(minWords)
            except ValueError:
                return Response("minWords should be a number")
            
            articlelist=articlelist.filter(wordCount__gt=minWords)
        serializers=ArticleSerializer(articlelist, many=True)

        return Response(serializers.data, status=200)
    
@api_view(['PATCH',])
@authentication_classes([JWTAuthentication])

def articleUpdate(request, pk):
    if request.method=='PATCH':

        try:
            article=Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("article not found", status=400)

        if request.user.role.rolename.lower()!='editor':
            return Response("you dont have permission", status=403)
        
        serializer=ArticleSerializer(article, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else: 
            return Response(serializer.errors, status=400)

@api_view(['DELETE',])
@authentication_classes([JWTAuthentication])

def articleDelete(request, pk):

    if request.method=='DELETE':
        
        try: 
            article=Article.objects.get(pk=pk)

        except Article.DoesNotExist:
            return Response("article not found", status=400)
        
        if request.user.role.rolename.lower()!='editor' and request.user!=article.authorID:
            return Response("you dont have permission", status=403)
        
        article.delete()
        return Response("deleted successfully", status=204)


