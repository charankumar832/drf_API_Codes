from django.urls import path, include
from .views import login, cartAdd,cartList, cartRetrieveUpdateDestroy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login, name='login'),
    path('cart/add/', cartAdd, name='cart-add'),
    path('cart/list/', cartList, name='cart-list'),
    path('cart/list/<int:pk>/', cartRetrieveUpdateDestroy,name='cart-list-ind'),
    path('cart/update/<int:pk>/', cartRetrieveUpdateDestroy,name='cart-update'),
    path('cart/delete/<int:pk>/', cartRetrieveUpdateDestroy,name='cart-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='api-token-refresh'),
]
