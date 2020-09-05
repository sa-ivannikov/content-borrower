
from celery import shared_task, task 



@shared_task
def test_task():
    return "test"

