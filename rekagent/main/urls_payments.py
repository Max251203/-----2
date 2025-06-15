from django.urls import path
from . import views_payments

urlpatterns = [
    path('', views_payments.payment_list, name='payment_list'),
    path('create/', views_payments.payment_create, name='payment_create'),
    path('edit/<int:pk>/', views_payments.payment_update, name='payment_update'),
    path('delete/<int:pk>/', views_payments.payment_delete, name='payment_delete'),
]
