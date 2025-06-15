from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Client, Order, Service, PaymentOrder


@login_required
def home(request):
    """Главная страница с общей статистикой"""
    context = {
        'total_clients': Client.objects.count(),
        'total_orders': Order.objects.count(),
        'total_services': Service.objects.count(),
        'total_payments': PaymentOrder.objects.count(),
    }

    # Если пользователь - клиент, показываем его статистику
    if hasattr(request.user, 'profile') and request.user.profile.role == 'client' and request.user.profile.linked_client:
        client = request.user.profile.linked_client
        client_orders = Order.objects.filter(client=client)
        context.update({
            'client': client,
            'client_orders': client_orders,
            'client_orders_count': client_orders.count(),
            'client_payments': PaymentOrder.objects.filter(order__client=client).count(),
        })
        return render(request, 'main/home_client.html', context)

    # Если пользователь - сотрудник или админ, показываем общую статистику
    return render(request, 'main/home.html', context)
