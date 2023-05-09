from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределённый класс пользователя от
    стандартного AbstractUser."""
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    

