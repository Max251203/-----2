from django.urls import path
from . import views_filters

app_name = 'filters'  # Добавляем пространство имен

urlpatterns = [
    path('orders-by-period/', views_filters.orders_by_period,
         name='orders_by_period'),
    path('payments-by-period/', views_filters.payments_by_period,
         name='payments_by_period'),
]
