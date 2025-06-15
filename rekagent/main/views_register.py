from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from .models import Profile, Client, Employee


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # Создаём профиль с выбранной ролью
            role = form.cleaned_data['role']
            profile, created = Profile.objects.update_or_create(
                user=user, defaults={'role': role})
            # Автоматическая привязка к Client/Employee
            if role == 'client':
                client = Client.objects.create(
                    name=user.username,
                    contact_person='',
                    address='',
                    email=user.email,
                    phone=''
                )
                profile.linked_client = client
                profile.save()
            elif role == 'employee':
                employee = Employee.objects.create(
                    last_name=user.username,
                    first_name='',
                    birth_date='2000-01-01'
                )
                profile.linked_employee = employee
                profile.save()
            # Авторизуем пользователя сразу после регистрации
            user = authenticate(username=user.username,
                                password=form.cleaned_data['password'])
            login(request, user)
            return redirect('home')  # Изменено с 'dashboard' на 'home'
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})
