from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page
from .models import Recipient, Donor, Post
from .tasks import repost_for_rec, delete_posts_of_recipient
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def index(request):
    recipients = Recipient.objects.all()
    context = {
        'recipients': recipients,
    }
    return render(request, 'posts/home.html', context)

@login_required
def repost(request, rec_id):
    repost_for_rec.delay(rec_id)
    return redirect('/')

@login_required
def store(request, rec_id):
    rec = Recipient.objects.get(id=rec_id)
    rec.write_all()
    return redirect('/')

@login_required
def delete_posts(request, rec_id):
    delete_posts_of_recipient.delay(rec_id)
    return redirect('/')
