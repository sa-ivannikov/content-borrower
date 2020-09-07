from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroupRunner.settings')

app = Celery('GroupRunner',
             broker='redis://redis:6379',
             backend='redis://redis:6379',
             include=['posts.tasks'],
             timezone='Europe/Moscow')

app.conf.beat_schedule = {
    'Write all posts daily at 01:00 am': {
        'task': 'posts.tasks.write_posts_to_db',
        'schedule':crontab(minute=0, hour=1),
    },
    'Repost every 30 mins from 9 AM to 9 PM': {
        'task': 'posts.tasks.repost',
        'schedule': crontab(minute='*/5')
        #'schedule': crontab(minute='*/30', hour='9-21')
    }
}

if __name__ == "__main__":
    app.start()
    