from django.urls import path
from . import views_clients

urlpatterns = [
    path('', views_clients.client_list, name='client_list'),
    path('create/', views_clients.client_create, name='client_create'),
    path('edit/<int:pk>/', views_clients.client_update, name='client_update'),
    path('delete/<int:pk>/', views_clients.client_delete, name='client_delete'),
]
