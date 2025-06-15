from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Client, Order, Service, PaymentOrder
from xhtml2pdf import pisa
from io import BytesIO
from decimal import Decimal


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    # Добавляем кодировку UTF-8 для корректного отображения кириллицы
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


@login_required
@user_passes_test(is_staff_or_admin)
def export_clients_pdf(request):
    clients = Client.objects.all()

    # Добавляем статистику для каждого клиента
    client_stats = []
    for client in clients:
        orders = Order.objects.filter(client=client)
        total_orders = orders.count()
        total_sum = Decimal('0.00')
        for order in orders:
            if order.service.price:
                price = order.service.price
                quantity = order.quantity
                discount = order.discount or 0
                order_sum = price * quantity * (1 - discount/100)
                total_sum += order_sum

        payments = PaymentOrder.objects.filter(order__client=client)
        total_payments = payments.count()

        client_stats.append({
            'client': client,
            'total_orders': total_orders,
            'total_sum': total_sum,
            'total_payments': total_payments,
        })

    context = {
        'client_stats': client_stats,
        'title': 'Отчет по клиентам'
    }

    pdf = render_to_pdf('main/exports/clients_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "clients_report.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Ошибка при создании PDF")


@login_required
@user_passes_test(is_staff_or_admin)
def export_services_pdf(request):
    services = Service.objects.all()

    # Добавляем статистику для каждой услуги
    service_stats = []
    for service in services:
        count = Order.objects.filter(service=service).count()
        total_sum = Decimal('0.00')
        orders = Order.objects.filter(service=service)
        for order in orders:
            if service.price:
                price = service.price
                quantity = order.quantity
                discount = order.discount or 0
                order_sum = price * quantity * (1 - discount/100)
                total_sum += order_sum

        service_stats.append({
            'service': service,
            'count': count,
            'total_sum': total_sum
        })

    context = {
        'service_stats': service_stats,
        'title': 'Рейтинг услуг'
    }

    pdf = render_to_pdf('main/exports/services_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "services_report.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Ошибка при создании PDF")


@login_required
@user_passes_test(is_staff_or_admin)
def export_orders_pdf(request):
    orders = Order.objects.all().order_by('-date_received')

    # Расчет итоговой суммы для каждого заказа
    for order in orders:
        if order.service.price:
            price = order.service.price
            quantity = order.quantity
            discount = order.discount or 0
            order.total = price * quantity * (1 - discount/100)
        else:
            order.total = Decimal('0.00')

    context = {
        'orders': orders,
        'title': 'Отчет по заказам'
    }

    pdf = render_to_pdf('main/exports/orders_pdf.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "orders_report.pdf"
        content = f"attachment; filename={filename}"
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Ошибка при создании PDF")
