# Работает только на сервере, так как нужна привязка к Redis
import os

from celery import Celery

# Указываем наш проект store
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

app = Celery('store')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
