from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages


def user_login(request):
    # Если пользователь уже авторизован, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            profile, created = Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Неверный логин или пароль")
            return render(request, "main/login.html", {"error": "Неверный логин или пароль"})
    return render(request, "main/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы")
    return redirect('login')
