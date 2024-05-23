from celery import Celery
from celery.schedules import crontab

app = Celery('expense_share')

app.conf.beat_schedule = {
    'export-balances-every-week': {
        'task': 'core.tasks.export_balances_to_s3',
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
    },
}
