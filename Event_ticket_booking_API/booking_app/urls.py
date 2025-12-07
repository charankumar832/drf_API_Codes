from django.urls import path, include
from .views import login, ticketsCreate, ticketsList, ticketsRetrieveUpdateDestroy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', login, name='login'),
    path('ticket/create/', ticketsCreate, name='ticket-create'),
    path('ticket/list/', ticketsList, name='ticket-list'),
    path('ticket/list/<int:pk>/', ticketsRetrieveUpdateDestroy, name='ticket-list-ind'),
    path('ticket/update/<int:pk>/', ticketsRetrieveUpdateDestroy, name='ticket-update'),
    path('ticket/delete/<int:pk>/', ticketsRetrieveUpdateDestroy, name='ticket-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(),name='api-token-refresh'),
]
