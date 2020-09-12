from celery import shared_task
from .services import store_posts, repost_top_post, repost_for_recipient, delete_recipients_post
from .models import Recipient


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

@shared_task
def repost_for_rec(rec_id):
    recipient = Recipient.objects.get(id=rec_id)
    repost_for_recipient(recipient)
    print('Reposted a post for {0}'.format(recipient))

@shared_task
def delete_posts_of_recipient(rec_id):
    delete_recipients_post(rec_id)
