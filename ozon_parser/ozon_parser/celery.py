from __future__ import absolute_import
import os
from celery import Celery

from .settings import INSTALLED_APPS


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ozon_parser.settings')


app = Celery("ozon_parser")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: INSTALLED_APPS)
