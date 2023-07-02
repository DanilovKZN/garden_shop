from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.mixins import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


SUCCESS_MSG_REGISTR = "Вы успешно зарегистрировались!"


class UserLoginView(TitleMixin, LoginView):
    """Классовое представление входа в аккаунт."""
    title = 'Авторизация'
    template_name = 'users/login.html'
    form_class = UserLoginForm


class RegistrationCreateView(SuccessMessageMixin, TitleMixin, CreateView):
    """Классовое представление регистрации пользователя."""
    model = User
    form_class = UserRegistrationForm   # Используется ссылка на форму, все данные идут уже под капотом
    title = 'Регистрация'
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login_enter')
    success_message = SUCCESS_MSG_REGISTR


# @login_required теперь используется в urls
class ProfileUpdateView(TitleMixin, UpdateView):
    """Классовое представление личного кабинета пользователя
    с возможностью редактирования данных и отображением корзины."""
    model = User
    form_class = UserProfileForm
    title = 'Личный кабинет'
    template_name = 'users/profile.html'

    # Переопределяем success_url, так как нам нужно ещё добавить id пользователя
    def get_success_url(self) -> str:
        return reverse_lazy('users:profile', args=(self.object.id, ))


class EmailVerificationView(TitleMixin, TemplateView):
    """Классовое представление контроллера подтверждения
    пользователя через email."""
    title = 'Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # Если есть такой обьект и срок жизни не истёк. Так как обьект только один в списке будет, то first
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
