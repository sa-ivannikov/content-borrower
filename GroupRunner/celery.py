from celery import Celery
from celery.schedules import crontab


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
    'Test every 2 secs': {
        'task': 'GroupRunner.celery.test',
        'schedule':crontab(),
        'args': ('hello',)
    }
}

if __name__ == "__main__":
    app.start()