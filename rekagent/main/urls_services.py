from django.urls import path
from . import views_services

urlpatterns = [
    path('', views_services.service_list, name='service_list'),
    path('create/', views_services.service_create, name='service_create'),
    path('edit/<int:pk>/', views_services.service_update, name='service_update'),
    path('delete/<int:pk>/', views_services.service_delete, name='service_delete'),
]
