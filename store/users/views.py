from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


SUCCESS_MSG_REGISTR = "Вы успешно зарегистрировались!"


def login_enter(request):
    """Контроллер входа в аккаунт."""
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password  =request.POST['password']
            user = auth.authenticate(
                username=username,
                password=password
            )
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:   
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)


def registration(request):
    """Контроллер регистрации пользователя."""
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, SUCCESS_MSG_REGISTR)
            return HttpResponseRedirect(reverse('users:login_enter'))
    else:        
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/registration.html', context)


@login_required
def profile(request):
    """Контроллер личного кабинета пользователя."""
    if request.method == 'POST':
        form = UserProfileForm(
            instance=request.user,
            data=request.POST,
            files=request.FILES
        )
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:        
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)    
    context = {
        'title': 'Store - Профиль',
        'form': form,
        'baskets': baskets
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    """Контроллер выхода из аккаунта."""
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
