from django.urls import path
from . import views_reports

urlpatterns = [
    path('', views_reports.reports, name='reports'),
]
