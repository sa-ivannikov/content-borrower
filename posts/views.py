from django.shortcuts import render
from django.http import HttpResponse
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from django.views.decorators.cache import cache_page


# Create your views here.
def index(request):
    return HttpResponse('TEST!')