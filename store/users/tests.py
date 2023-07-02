from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from users.models import EmailVerification, User

ERROR_USER_IN_BD = "Пользователь с таким именем уже существует."


class UserRegistrationViewTestCase(TestCase):
    """Тестирование регистрации пользователя."""

    def setUp(self) -> None:
        """Общие данные для тестов."""
        self.data = {
            'first_name': 'Nikola',
            'last_name': 'Dan',
            'username': 'DanNik',
            'email': 'NikOmOr67@yandex.ru',
            'password1': 'JacK3mRoseB9',
            'password2': 'JacK3mRoseB9',
        }
        self.path = reverse('users:registration')

    # Тест get запроса
    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    # Тест post запроса
    def test_user_registration_post(self):
        username = self.data['username']
        # Пользователь не создан до запроса
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)
        # Пришёл ответ 302 о создании и переход на страницу входа
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login_enter'))

        # Создался ли в БД новый пользователь
        self.assertTrue(User.objects.filter(username=username).exists())

        # Проверка верификаци по email
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())

    # Тест на ошибки при создании пользователя
    def test_user_registration_post_errors(self):
        username = self.data['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        # Пришёл ответ 200, Остались на той же странице, так как пользователь с таким username уже есть в БД
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, ERROR_USER_IN_BD, html=True)
