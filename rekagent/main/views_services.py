from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Service
from .forms import ServiceForm


def is_staff_or_admin(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'employee')


@login_required
@user_passes_test(is_staff_or_admin)
def service_list(request):
    services = Service.objects.all()
    return render(request, 'main/services/list.html', {'services': services})


@login_required
@user_passes_test(is_staff_or_admin)
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'main/services/form.html', {'form': form, 'title': 'Добавить услугу'})


@login_required
@user_passes_test(is_staff_or_admin)
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'main/services/form.html', {'form': form, 'title': 'Редактировать услугу'})


@login_required
@user_passes_test(is_staff_or_admin)
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'main/services/confirm_delete.html', {'service': service})
