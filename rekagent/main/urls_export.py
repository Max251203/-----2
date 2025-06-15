from django.urls import path
from . import views_export

urlpatterns = [
    path('clients-pdf/', views_export.export_clients_pdf,
         name='export_clients_pdf'),
    path('services-pdf/', views_export.export_services_pdf,
         name='export_services_pdf'),
    path('orders-pdf/', views_export.export_orders_pdf, name='export_orders_pdf'),
]
