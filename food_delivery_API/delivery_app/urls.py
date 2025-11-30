from django.urls import path, include
from .views import login, orderCreate, orderList, orderUpdate, orderDelete
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('login/', login, name='login'),
    path('order/create/', orderCreate, name='order-create'),
    path('order/list/', orderList, name='order-list'),
    path('order/update/<int:pk>/', orderUpdate, name='order-update'),
    path('order/delete/<int:pk>/', orderDelete, name='order-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    
]