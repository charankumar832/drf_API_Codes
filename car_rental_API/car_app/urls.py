from django.urls import path, include
from .views import login, rentalCreate, rentalList, rentalRetrieveUpdateDestroy

urlpatterns = [
    path('login/', login, name='login'),
    path('rental/create/', rentalCreate, name='rental-create'),
    path('rental/list/', rentalList, name='rental-list'),
    path('rental/update/<int:pk>/', rentalRetrieveUpdateDestroy, name='rental-update'),
    path('rental/delete/<int:pk>/', rentalRetrieveUpdateDestroy, name='rental-delete'),
    path('rental/list/<int:pk>/', rentalRetrieveUpdateDestroy, name='rental-list-ind'),
]
