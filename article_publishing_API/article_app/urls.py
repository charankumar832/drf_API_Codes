from django.urls import path, include
from .views import login, articleAdd, articleList, articleDelete, articleUpdate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('login/', login, name='login'),
    path('article/add/', articleAdd, name='article-add'),
    path('article/list/', articleList, name='article-list'),
    path('article/update/<int:pk>/', articleUpdate, name='article-update'),
    path('article/delete/<int:pk>/', articleDelete, name='article-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),

]