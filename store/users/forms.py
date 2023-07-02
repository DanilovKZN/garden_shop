import uuid
from datetime import timedelta

from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm
)
from django.utils.timezone import now

from users.models import EmailVerification, User


# Время жизни ссылки в часах
LIVE_TIME_UUID = 48


class UserLoginForm(AuthenticationForm):
    """Форма аутентификации пользователя с кастомизацией (login.html)."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя с кастомизацией (registration.html)."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите адрес электронной почты'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        """Переопределяем сохранение пользователя для
        добавления функции отправки сообщения на email."""
        user = super(UserRegistrationForm, self).save(commit=True)
        expiration = now() + timedelta(hours=LIVE_TIME_UUID)  # Получение даты сгорания ссылки
        # uuid.uuid4() формирует уникальный код
        record = EmailVerification.objects.create(
            code=uuid.uuid4(),
            user=user,
            expiration=expiration
        )
        # Метод send_verification_email мы определили в models.py
        record.send_verification_email()

        return user


class UserProfileForm(UserChangeForm):
    """Форма личного кабинета пользователя с кастомизацией (profile.html)."""
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4'
    }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-input'
    }), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'readonly': True
    }))

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'image',
            'username',
            'email'
        )
