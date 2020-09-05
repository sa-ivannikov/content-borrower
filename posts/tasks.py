from celery import shared_task, task 
from .services import storePosts

@shared_task
def test_task():
    return "test"

@shared_task
def writePostsToDB():
    storePosts()
    print('Posts written sucessfully!')
