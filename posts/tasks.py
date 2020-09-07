from celery import shared_task
from .services import store_posts, repost_top_post


@shared_task
def write_posts_to_db():
    """ Run this daily at 01:00 AM.
    Stores all posts from yesterday
    in DB """
    store_posts()
    print('Posts written sucessfully!')

@shared_task
def repost():
    """ Run this task to repost into all
    target groups """
    repost_top_post()
    print('Photo posted sucessfully')
