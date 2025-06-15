from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile, Client, Employee
from .forms import ClientForm, EmployeeForm  # Добавляем импорт EmployeeForm
from django.contrib import messages
from django.contrib.auth.models import User


@login_required
def profile_view(request):
    if request.user.is_superuser:
        # Для суперпользователя показываем специальный профиль
        return render(request, "main/profile_superuser.html")

    # Для обычных пользователей
    try:
        profile = request.user.profile
        if profile.role == "client":
            client = profile.linked_client
            return render(request, "main/profile_client.html", {"client": client})
        elif profile.role == "employee":
            employee = profile.linked_employee
            return render(request, "main/profile_employee.html", {"employee": employee})
    except Profile.DoesNotExist:
        messages.warning(
            request, "У вас не создан профиль. Пожалуйста, обратитесь к администратору.")
        return redirect("home")

    return redirect("home")


@login_required
def profile_edit(request):
    if request.user.is_superuser:
        # Для суперпользователя редактирование не требуется
        messages.info(
            request, "Суперпользователь не требует редактирования профиля.")
        return redirect("profile")

    try:
        profile = request.user.profile
        if profile.role == "client":
            # Если профиль клиента не привязан, создаем новый
            if not profile.linked_client:
                client = Client.objects.create(
                    name=request.user.username,
                    contact_person='',
                    email=request.user.email,
                    phone=''
                )
                profile.linked_client = client
                profile.save()
                messages.success(
                    request, "Профиль клиента создан. Пожалуйста, заполните информацию.")

            client = profile.linked_client
            if request.method == "POST":
                form = ClientForm(request.POST, instance=client)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Профиль обновлён.")
                    return redirect("profile")
            else:
                form = ClientForm(instance=client)
            return render(request, "main/profile_edit_client.html", {"form": form})

        elif profile.role == "employee":
            # Если профиль сотрудника не привязан, создаем новый
            if not profile.linked_employee:
                employee = Employee.objects.create(
                    last_name=request.user.username,
                    first_name='',
                    birth_date='2000-01-01'
                )
                profile.linked_employee = employee
                profile.save()
                messages.success(
                    request, "Профиль сотрудника создан. Пожалуйста, заполните информацию.")

            employee = profile.linked_employee
            if request.method == "POST":
                form = EmployeeForm(request.POST, instance=employee)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Профиль обновлён.")
                    return redirect("profile")
            else:
                form = EmployeeForm(instance=employee)
            return render(request, "main/profile_edit_employee.html", {"form": form})

    except Profile.DoesNotExist:
        messages.warning(
            request, "У вас не создан профиль. Пожалуйста, обратитесь к администратору.")
        return redirect("home")

    return redirect("home")
