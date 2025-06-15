from django.urls import path
from . import views_orders

urlpatterns = [
    path('', views_orders.order_list, name='order_list'),
    path('create/', views_orders.order_create, name='order_create'),
    path('edit/<int:pk>/', views_orders.order_update, name='order_update'),
    path('delete/<int:pk>/', views_orders.order_delete, name='order_delete'),
]
