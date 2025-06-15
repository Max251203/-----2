from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile


def user_login(request):
    # Удаляем проверку на is_authenticated, чтобы всегда показывать окно входа
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            profile, created = Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect("home")
        else:
            return render(request, "main/login.html", {"error": "Неверный логин или пароль"})
    return render(request, "main/login.html")


def user_logout(request):
    logout(request)
    return redirect('login')
