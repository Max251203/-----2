from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order, PaymentOrder
from datetime import date, timedelta


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def orders_by_period(request):
    # Значения по умолчанию
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    # Здесь должна быть обработка формы, но пока упрощаем

    orders = Order.objects.filter(
        date_received__gte=start_date,
        date_received__lte=end_date
    ).order_by('-date_received')

    # Расчет итоговой суммы для каждого заказа
    total_sum = 0
    for order in orders:
        if order.service.price:
            price = order.service.price
            quantity = order.quantity
            discount = order.discount or 0
            order_total = price * quantity * (1 - discount/100)
            order.total = order_total
            total_sum += order_total
        else:
            order.total = 0

    return render(request, 'main/filters/orders_by_period.html', {
        'orders': orders,
        'total_sum': total_sum,
        'start_date': start_date,
        'end_date': end_date,
    })


@login_required
@user_passes_test(is_staff_or_admin)
def payments_by_period(request):
    # Значения по умолчанию
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    # Здесь должна быть обработка формы, но пока упрощаем

    payments = PaymentOrder.objects.filter(
        date_paid__gte=start_date,
        date_paid__lte=end_date
    ).order_by('-date_paid')

    # Расчет итоговой суммы для каждого платежа
    total_sum = 0
    for payment in payments:
        order = payment.order
        if order.service.price:
            price = order.service.price
            quantity = order.quantity
            discount = order.discount or 0
            payment_total = price * quantity * (1 - discount/100)
            payment.total = payment_total
            total_sum += payment_total
        else:
            payment.total = 0

    return render(request, 'main/filters/payments_by_period.html', {
        'payments': payments,
        'total_sum': total_sum,
        'start_date': start_date,
        'end_date': end_date,
    })
