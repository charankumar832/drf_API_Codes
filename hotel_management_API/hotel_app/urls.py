from django.urls import path, include
from .views import login, bookingCreate, bookingList, bookingDelete, bookingUpdate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login, name='login'),
    path('booking/add/', bookingCreate, name='booking-create'),
    path('booking/list/', bookingList, name='booking-list'),
    path('booking/update/<int:pk>/', bookingUpdate, name='booking-update'),
    path('booking/delete/<int:pk>/', bookingDelete, name='booking-delete'),
    path('api/token/',TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
]
