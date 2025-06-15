from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import Profile, Client, Employee, Position, Department
from .forms import UserForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def admin_users(request):
    users = User.objects.all().order_by('-is_superuser', 'username')
    return render(request, "main/admin/users.html", {"users": users})


@user_passes_test(is_superuser)
def admin_user_create(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if 'password' in request.POST and request.POST['password']:
                user.password = make_password(request.POST['password'])
            user.save()
            messages.success(
                request, f"Пользователь {user.username} успешно создан.")
            return redirect('admin_users')
    else:
        form = UserForm()
    return render(request, "main/admin/user_form.html", {"form": form, "title": "Создать пользователя"})


@user_passes_test(is_superuser)
def admin_user_edit(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            user = form.save(commit=False)
            if 'password' in request.POST and request.POST['password']:
                user.password = make_password(request.POST['password'])
            user.save()
            messages.success(
                request, f"Пользователь {user_obj.username} успешно обновлен.")
            return redirect('admin_users')
    else:
        form = UserForm(instance=user_obj)
    return render(request, "main/admin/user_form.html", {"form": form, "user_obj": user_obj, "title": "Редактировать пользователя"})


@user_passes_test(is_superuser)
def admin_user_delete(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        username = user_obj.username
        user_obj.delete()
        messages.success(request, f"Пользователь {username} успешно удален.")
        return redirect('admin_users')
    return render(request, "main/admin/user_confirm_delete.html", {"user_obj": user_obj})


@user_passes_test(is_superuser)
def admin_profiles(request):
    profiles = Profile.objects.all().select_related('user')
    return render(request, "main/admin/profiles.html", {"profiles": profiles})


@user_passes_test(is_superuser)
def admin_profile_create(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно создан.")
            return redirect('admin_profiles')
    else:
        form = ProfileForm()
    return render(request, "main/admin/profile_form.html", {"form": form, "title": "Создать профиль"})


@user_passes_test(is_superuser)
def admin_profile_edit(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Профиль пользователя {profile.user.username} успешно обновлен.")
            return redirect('admin_profiles')
    else:
        form = ProfileForm(instance=profile)
    return render(request, "main/admin/profile_form.html", {"form": form, "profile": profile, "title": "Редактировать профиль"})


@user_passes_test(is_superuser)
def admin_profile_delete(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if request.method == "POST":
        username = profile.user.username
        profile.delete()
        messages.success(
            request, f"Профиль пользователя {username} успешно удален.")
        return redirect('admin_profiles')
    return render(request, "main/admin/profile_confirm_delete.html", {"profile": profile})
