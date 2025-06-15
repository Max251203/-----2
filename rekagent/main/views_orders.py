from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
from .forms import OrderForm


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
def order_list(request):
    # Если сотрудник или админ - показываем все заказы
    if request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'employee'):
        orders = Order.objects.select_related(
            'client', 'employee', 'service').all()
    # Если клиент - показываем только его заказы
    elif hasattr(request.user, 'profile') and request.user.profile.role == 'client' and request.user.profile.linked_client:
        orders = Order.objects.select_related('client', 'employee', 'service').filter(
            client=request.user.profile.linked_client
        )
    else:
        orders = Order.objects.none()

    return render(request, 'main/orders/list.html', {'orders': orders})


@login_required
@user_passes_test(is_staff_or_admin)
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'main/orders/form.html', {'form': form, 'title': 'Добавить заказ'})


@login_required
@user_passes_test(is_staff_or_admin)
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    return render(request, 'main/orders/form.html', {'form': form, 'title': 'Редактировать заказ'})


@login_required
@user_passes_test(is_staff_or_admin)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'main/orders/confirm_delete.html', {'order': order})
