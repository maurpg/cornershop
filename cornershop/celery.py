import os
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cornershop.settings')

app = Celery('cornershop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_slack_reminder_menu': {
        'task': 'nora.tasks.send_reminder_menu',
        'schedule': crontab(hour=11, minute=00),
        'args': (),
    }
}

