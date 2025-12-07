from django.urls import path, include
from .views import login, borrowCreate, borrowList, borrowRetrieveUpdateDestroy

urlpatterns = [
    path('login/', login, name='login'),
    path('borrow/create/', borrowCreate, name='borrow-create'),
    path('borrow/list/', borrowList, name='borrow-list'),
    path('borrow/update/<int:pk>/', borrowRetrieveUpdateDestroy, name='borrow-update'),
    path('borrow/delete/<int:pk>/', borrowRetrieveUpdateDestroy, name='borrow-delete'),
]
