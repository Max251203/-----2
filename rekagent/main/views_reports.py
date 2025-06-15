from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Client, Order, Service, PaymentOrder


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def reports(request):
    # Пример: список клиентов с суммой заказов и оплат
    clients = Client.objects.all()
    client_stats = []
    for client in clients:
        orders = Order.objects.filter(client=client)
        total_orders = orders.count()
        total_sum = sum(
            (o.service.price or 0) * o.quantity * (1 - (o.discount or 0)/100)
            for o in orders
        )
        payments = PaymentOrder.objects.filter(order__client=client)
        total_payments = payments.count()
        client_stats.append({
            'client': client,
            'total_orders': total_orders,
            'total_sum': total_sum,
            'total_payments': total_payments,
        })

    # Пример: рейтинг услуг
    service_stats = []
    for service in Service.objects.all():
        count = Order.objects.filter(service=service).count()
        service_stats.append({'service': service, 'count': count})

    # Заказы с расчетом оплаты
    # Ограничиваем 20 последними заказами
    orders = Order.objects.all().order_by('-date_received')[:20]

    return render(request, 'main/reports/index.html', {
        'client_stats': client_stats,
        'service_stats': service_stats,
        'orders': orders,
    })
