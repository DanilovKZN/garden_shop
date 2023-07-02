from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    """Переопределённый класс пользователя от
    стандартного AbstractUser."""
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class EmailVerification(models.Model):
    """Модель для проверки подтверждения пользователем своего email."""
    # Уникальный код для пользователя
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)  # Автоматически ставить время создания
    expiration = models.DateTimeField()  # Время жизни ссылки, дата конца действия ссылки

    def __str__(self) -> str:
        return f"EmailVerification for user {self.user.email}."

    def send_verification_email(self):
        """Функция отправки письма для подтверждения ссылки."""
        # Формируем ссылку с данными
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учётной записи для {self.user.username}'
        message = 'Для подтверждения учётной записи для {} перейдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
        )

    def is_expired(self):
        """Проверка срока жизни ссылки."""
        return True if now() >= self.expiration else False
