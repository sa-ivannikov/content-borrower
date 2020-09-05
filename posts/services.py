from .models import Post, Recipient, Donor


def storePosts():
    recipients = Recipient.objects.all()
    for recipient in recipients:
        recipient.writeAll()
    