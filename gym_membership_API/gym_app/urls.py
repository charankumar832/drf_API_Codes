from django.urls import path, include
from .views import login, membershipCreate, membershipList, membershipRetrieveUpdateDestroy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('login/',login, name='login'),
    path('membership/create/', membershipCreate, name='membership-create'),
    path('membership/list/',membershipList, name='membership-list'),
    path('membership/list/<int:pk>/',membershipRetrieveUpdateDestroy,name='membership-list-ind'),
    path('membership/update/<int:pk>/',membershipRetrieveUpdateDestroy,name='membership-update'),
    path('membership/delete/<int:pk>/',membershipRetrieveUpdateDestroy,name='membership-delete'),
    path('api/token/', TokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', TokenObtainPairView.as_view(), name='api-token-refresh'),
]