from django.urls import path, include
from .views import login, shipmentAdd, shipmentList, shipmentRetrieveUpdateDestroy

urlpatterns = [
    path('login/', login, name='login'),
    path('shipment/list/', shipmentList,name='shipment-list'),
    path('shipment/add/', shipmentAdd,name='shipment-add'),
    path('shipment/update/<int:pk>/', shipmentRetrieveUpdateDestroy,name='shipment-update'),
    path('shipment/delete/<int:pk>/', shipmentRetrieveUpdateDestroy,name='shipment-delete'),
    path('shipment/list/<int:pk>/', shipmentRetrieveUpdateDestroy,name='shipment-list-ind'),
]
