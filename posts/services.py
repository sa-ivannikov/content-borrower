from .models import Post, Recipient, Donor


def storePosts():
    recipients = Recipient.objects.all()
    for recipient in recipients:
        recipient.writeAll()

def post_to_group(post):
    pass

def repost_top_post():
    recipients = Recipient.objects.all()
    for recipient in recipients:
        posts = recipient.makePostsList()
        if posts:
            best_post = posts[0]
            #print(best_post)
            post_to_group(best_post)
            best_post.posted = True
            best_post.save()
