from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Client
from .forms import ClientForm

# Проверка роли: доступ для сотрудников и админов


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')

# Список клиентов


@login_required
@user_passes_test(is_staff_or_admin)
def client_list(request):
    search_query = request.GET.get("q")

    clients = Client.objects.all()
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    context = {'clients': clients}
    return render(request, 'main/clients/list.html', context)

# Добавить клиента


@login_required
@user_passes_test(is_staff_or_admin)
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'main/clients/form.html', {'form': form, 'title': 'Добавить клиента'})

# Редактировать клиента


@login_required
@user_passes_test(is_staff_or_admin)
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ClientForm(instance=client)
    return render(request, 'main/clients/form.html', {'form': form, 'title': 'Редактировать клиента'})

# Удалить клиента


@login_required
@user_passes_test(is_staff_or_admin)
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'main/clients/confirm_delete.html', {'client': client})
