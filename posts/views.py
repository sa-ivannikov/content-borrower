from django.shortcuts import render
from django.http import HttpResponse
from .services import get_posts, get_donors
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.

@cache_page(CACHE_TTL)
def index(request):
    return HttpResponse(get_donors())