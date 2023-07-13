# Садовый магазин "6 Соток"

### Описание
Сайт садового магазина "6 Соток".

### Запуск проекта в dev-режиме
- Установите и активируйте виртуальное окружение
```
python -m venv venv
source venv/Scripts/activate
``` 
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Создать файл .env:
```
DEBUG = 'Режим "Отладка/Продакшен"'
SECRET_KEY = 'Секретный ключ приложения'
DOMAIN_NAME = 'Доменное имя'

# Email
EMAIL_HOST = 'Хост почтового сервиса для отправки сообщений'
EMAIL_PORT = 'Порт почтового сервиса'
EMAIL_PASSWORD = 'Пароль от почтового ящика'
EMAIL_HOST_USER = 'Адрес почтового ящика'
EMAIL_USE_SSL = 'Испоьзовать ли SSL: True/False'

# DB
ENGINE_DB = 'Движок БД'
NAME_DB= 'Имя БД'
USER_DB= 'Пользователь БД'
PASSWORD_DB = 'Пароль БД'
HOST_DB = 'Хост Бд'
PORT_DB = 'Порт БД'

# Stripe
STRIPE_PUBLIC_KEY = 'Публичный ключ Stripe'
STRIPE_SECRET_KEY = 'Секретный ключ Stripe'
STRIPE_WEBHOOK_SECRET = 'Секретный ключ вебхука Stripe'

# Redis
REDIS_HOST = 'Хост Redis'
REDIS_PORT = 'Порт Redis'
```

- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```
### Технологии
```
Python 3.9.6
Django 3.2.15
Stripe
Redis
PostgreSQL
Celery
```
### Сайт
```
http://31.184.253.113/
```
### Авторы
Николай Данилов
