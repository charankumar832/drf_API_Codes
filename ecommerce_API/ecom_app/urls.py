from django.urls import path, include
from .views import login, productList, productsAdd, orderCreate, orderDelete, orderUpdate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('login/', login, name='login'),
    path('product/add/', productsAdd, name='product-add'),
    path('product/list/', productList, name='product-list'),
    path('order/create/', orderCreate, name='order-create'),
    path('order/update/<int:pk>/', orderUpdate, name='order-update'),
    path('order/delete/<int:pk>/', orderDelete, name='order-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='api-token-refresh'),
]