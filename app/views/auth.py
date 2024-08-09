from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse

from app.forms import LoginForm, RegisterForm
from app.models import User


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('product_list')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

    return render(request, 'app/auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('product_list'))
    return render(request, 'app/auth/logout.html')


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return redirect('login')
    return render(request, 'app/auth/register.html', {'form': form})







