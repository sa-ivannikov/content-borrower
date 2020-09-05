from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroupRunner.settings')

app = Celery('GroupRunner',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379',
             include=[
                      'posts.tasks'],
             timezone='Europe/Moscow')


@app.task
def test(arg):
    print(arg)

app.conf.beat_schedule = {
    'Write posts to DB every 1 minute': {
        'task': 'posts.tasks.writePostsToDB',
        'schedule':crontab(),
    }
}

if __name__ == "__main__":
    app.start()