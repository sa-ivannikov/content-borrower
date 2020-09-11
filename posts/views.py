from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page
from .models import Recipient, Donor, Post
#from .services import repost_for_recipient
from .tasks import repost_for_rec


# Create your views here.
def index(request):
    recipients = Recipient.objects.all()
    context = {
        'recipients': recipients,
    }
    return render(request, 'posts/home.html', context)

def repost(request, rec_id):
    repost_for_rec.delay(rec_id)
    return redirect('/')

def store(request, rec_id):
    rec = Recipient.objects.get(id=rec_id)
    rec.write_all()
    return redirect('/')
