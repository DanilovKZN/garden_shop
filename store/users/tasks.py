# Задачи для Celery. Работает только на сервере
import uuid
from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


LIVE_TIME_UUID = 48


@shared_task
def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(hours=LIVE_TIME_UUID)  # Получение даты сгорания ссылки
    # uuid.uuid4() формирует уникальный код
    record = EmailVerification.objects.create(
        code=uuid.uuid4(),
        user=user,
        expiration=expiration
    )
    # Метод send_verification_email мы определили в models.py
    record.send_verification_email()
