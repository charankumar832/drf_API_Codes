from django.urls import path
from .views import login, reservationCreate, reservationList,reservationRetrieveUpdateDestroy
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/',login, name='login'),
    path('reservation/create/', reservationCreate, name='reservation-create'),
    path('reservation/list/', reservationList, name='reservation-list'),
    path('reservation/list/<int:pk>/', reservationRetrieveUpdateDestroy, name='reservation-list-ind'),
    path('reservation/update/<int:pk>/', reservationRetrieveUpdateDestroy, name='reservation-update'),
    path('reservation/delete/<int:pk>/', reservationRetrieveUpdateDestroy, name='reservation-delete'),
    path('api/token/', TokenObtainPairView.as_view(),name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('login2/', obtain_auth_token, name='login2'),
]
