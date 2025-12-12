from django.urls import path, include
from .views import login, bookingCreate, bookingList, bookingRetrieveUpdateDestroy
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('login/',login, name='login'),
    path('booking/create/', bookingCreate, name='booking-create'),
    path('booking/list/', bookingList, name='booking-list'),
    path('booking/list/<int:pk>/', bookingRetrieveUpdateDestroy, name='booking-list-ind'),
    path('booking/update/<int:pk>/', bookingRetrieveUpdateDestroy, name='booking-update'),
    path('booking/delete/<int:pk>/', bookingRetrieveUpdateDestroy, name='booking-delete'),
    path('login2/', obtain_auth_token, name='login2-auth-token'),
    path('api/token/',TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='api-token-refresh'),
]