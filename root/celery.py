import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

# Указывает Celery, где искать настройки Django.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")

# Создает экземпляр Celery.
app = Celery("root")

# Загружает настройки из файла settings.py проекта Django.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.beat_schedule = {
    "add_debt_every_three_hours": {"task": "manufacturer.tasks.edit_debt", "schedule": crontab(hour="*/3")},
    "decrease-debt": {"task": "manufacturer.tasks.decrease_debt", "schedule": crontab(hour=6, minute=30)},
}

# Автоматически обнаруживает и регистрирует задачи в файлах tasks.py в приложениях Django.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
