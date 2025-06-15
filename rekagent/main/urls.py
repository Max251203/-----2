from django.urls import path, include
from . import views_auth
from . import views_register
from . import views_main
from . import views_profile
from . import views_admin
from . import views_filters

urlpatterns = [
    # Аутентификация
    path('', views_auth.user_login, name='login_root'),
    path('login/', views_auth.user_login, name='login'),
    path('logout/', views_auth.user_logout, name='logout'),
    path('register/', views_register.register, name='register'),

    # Основные страницы
    path('home/', views_main.home, name='home'),
    path('profile/', views_profile.profile_view, name='profile'),
    path('profile/edit/', views_profile.profile_edit, name='profile_edit'),

    # Модули
    path('clients/', include('main.urls_clients')),
    path('services/', include('main.urls_services')),
    path('orders/', include('main.urls_orders')),
    path('payments/', include('main.urls_payments')),
    path('reports/', include('main.urls_reports')),
    path('export/', include('main.urls_export')),

    # Фильтры
    path('orders-by-period/', views_filters.orders_by_period,
         name='orders_by_period'),
    path('payments-by-period/', views_filters.payments_by_period,
         name='payments_by_period'),

    # Админка
    path('admin-users/', views_admin.admin_users, name='admin_users'),
    path('admin-users/create/', views_admin.admin_user_create,
         name='admin_user_create'),
    path('admin-users/<int:user_id>/edit/',
         views_admin.admin_user_edit, name='admin_user_edit'),
    path('admin-users/<int:user_id>/delete/',
         views_admin.admin_user_delete, name='admin_user_delete'),
    path('admin-profiles/', views_admin.admin_profiles, name='admin_profiles'),
    path('admin-profiles/create/', views_admin.admin_profile_create,
         name='admin_profile_create'),
    path('admin-profiles/<int:profile_id>/edit/',
         views_admin.admin_profile_edit, name='admin_profile_edit'),
    path('admin-profiles/<int:profile_id>/delete/',
         views_admin.admin_profile_delete, name='admin_profile_delete'),
]
