from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Order, PaymentOrder, Client, Service
from decimal import Decimal
from django.db.models import Count


@login_required
def home(request):
    # Если суперпользователь - показываем встроенную админку
    if request.user.is_superuser:
        # Добавляем статистику для админ-панели
        client_count = Client.objects.count()
        order_count = Order.objects.count()
        service_count = Service.objects.count()
        payment_count = PaymentOrder.objects.count()

        return render(request, "main/admin_dashboard.html", {
            'client_count': client_count,
            'order_count': order_count,
            'service_count': service_count,
            'payment_count': payment_count
        })

    # Если клиент - показываем его дашборд
    if hasattr(request.user, 'profile') and request.user.profile.role == 'client' and request.user.profile.linked_client:
        client = request.user.profile.linked_client
        orders = Order.objects.filter(client=client)

        # Статистика
        total_orders = orders.count()
        completed_orders = orders.filter(date_executed__isnull=False).count()
        pending_orders = total_orders - completed_orders

        # Расчет сумм
        total_sum = Decimal('0.00')
        for order in orders:
            if order.service.price:
                price = order.service.price
                quantity = order.quantity
                discount = order.discount or 0
                order_sum = price * quantity * (1 - discount/100)
                total_sum += order_sum

        # Оплаченная сумма
        payments = PaymentOrder.objects.filter(order__client=client)
        total_paid = Decimal('0.00')
        for payment in payments:
            order = payment.order
            if order.service.price:
                price = order.service.price
                quantity = order.quantity
                discount = order.discount or 0
                payment_sum = price * quantity * (1 - discount/100)
                total_paid += payment_sum

        # Последние заказы
        recent_orders = orders.order_by('-date_received')[:5]

        stats = {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_sum': total_sum,
            'total_paid': total_paid
        }

        return render(request, 'main/client_dashboard.html', {
            'client': client,
            'stats': stats,
            'recent_orders': recent_orders
        })

    # Если сотрудник - показываем его дашборд
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'employee' and request.user.profile.linked_employee:
        employee = request.user.profile.linked_employee
        orders = Order.objects.all()

        # Статистика
        total_orders = orders.count()
        completed_orders = orders.filter(date_executed__isnull=False).count()
        pending_orders = total_orders - completed_orders

        # Расчет сумм
        total_sum = Decimal('0.00')
        for order in orders:
            if order.service.price:
                price = order.service.price
                quantity = order.quantity
                discount = order.discount or 0
                order_sum = price * quantity * (1 - discount/100)
                total_sum += order_sum

        # Количество клиентов
        total_clients = Client.objects.count()

        # Последние заказы и платежи
        recent_orders = orders.order_by('-date_received')[:5]
        recent_payments = PaymentOrder.objects.order_by('-date_paid')[:5]

        stats = {
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': pending_orders,
            'total_sum': total_sum,
            'total_clients': total_clients
        }

        return render(request, 'main/employee_dashboard.html', {
            'employee': employee,
            'stats': stats,
            'recent_orders': recent_orders,
            'recent_payments': recent_payments
        })

    # Для других - обычная главная
    return render(request, "main/home.html")
