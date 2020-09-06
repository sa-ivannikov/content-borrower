from celery import shared_task 
from .services import storePosts

@shared_task
def test_task():
    print("test")

@shared_task
def writePostsToDB():
    storePosts()
    print('Posts written sucessfully!')
