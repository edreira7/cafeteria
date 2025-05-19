# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Endpoints para Cafeterias
    path('cafeterias/', views.cafeteria_list_create, name='cafeteria-list-create'),
    path('cafeterias/<int:id>/', views.cafeteria_detail, name='cafeteria-detail'),

    # Endpoints para Empleados
    path('empleados/', views.empleado_list_create, name='empleado-list-create'),
    path('empleados/<int:id>/', views.empleado_detail, name='empleado-detail'),

    # Endpoints para Productos
    path('productos/', views.producto_list_create, name='producto-list-create'),
    path('productos/<int:id>/', views.producto_detail, name='producto-detail'),

    # Endpoints para Pedidos
    path('pedidos/', views.pedido_list_create, name='pedido-list-create'),

    # Endpoints para Clientes
    path('clientes/', views.cliente_create, name='cliente-create'),

    # Endpoints para Reservas
    path('reservas/', views.reserva_list_create, name='reserva-list-create'),
    path('reservas/<int:id>/', views.reserva_detail, name='reserva-detail'),
]
